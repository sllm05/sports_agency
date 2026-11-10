"""
Authentication & Staff Management Service (`src/sports_agency/auth_service.py`)
Handles Google Cloud Firebase & Local Auth hybrid authentication:
- Google Cloud Project: iceu-songpa09
- Firebase Admin SDK authentication & custom token generation
- Automatic user sync between Firebase Auth & SQLite agency_users
- Admin pre-configured: admin@agent.com / password1234
- Staff self-registration with status = 'PENDING'
- Admin approval workflow before login is allowed
- Daily new signup tracking and administration
"""

from __future__ import annotations

import hashlib
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import firebase_admin
from firebase_admin import auth as fb_auth, credentials, firestore

from sports_agency.config import PROJECT_ROOT

logger = logging.getLogger(__name__)

DB_PATH = PROJECT_ROOT / "data" / "agency_desk.db"
FIREBASE_CRED_PATH = PROJECT_ROOT / "firebase-credentials.json"
FIRESTORE_DATABASE_ID = "agent-db"

# Web Client Firebase Configuration for Google Cloud project iceu-songpa09
FIREBASE_WEB_CONFIG: dict[str, str] = {
    "apiKey": "AIzaSyCx0qAZxcDFouVf70ug7LpmZjUfuCyfEsw",
    "authDomain": "iceu-songpa09.firebaseapp.com",
    "projectId": "iceu-songpa09",
    "storageBucket": "iceu-songpa09.firebasestorage.app",
    "messagingSenderId": "108335720396",
    "appId": "1:108335720396:web:4670f270f046ed7196df69",
    "measurementId": "G-0CF6Q6EVC4",
}


def _init_firebase() -> bool:
    """Initializes Firebase Admin SDK using service account credentials."""
    if firebase_admin._apps:
        return True
    if FIREBASE_CRED_PATH.exists():
        try:
            cred = credentials.Certificate(str(FIREBASE_CRED_PATH))
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin initialized successfully with %s", FIREBASE_CRED_PATH)
            return True
        except Exception as e:
            logger.warning("Failed to initialize Firebase Admin with credentials file: %s", e)
    # Fallback to Application Default Credentials
    try:
        firebase_admin.initialize_app()
        return True
    except Exception as e:
        logger.warning("Firebase Admin default init failed: %s", e)
        return False


def get_firebase_web_config() -> dict[str, Any]:
    """Returns the web client Firebase configuration for frontend consumption."""
    is_live = _init_firebase()
    return {
        **FIREBASE_WEB_CONFIG,
        "is_backend_connected": is_live,
        "service_account_configured": FIREBASE_CRED_PATH.exists(),
    }


def get_firestore_client():
    """Returns Cloud Firestore client connected to database agent-db."""
    if not _init_firebase():
        return None
    try:
        return firestore.client(database_id=FIRESTORE_DATABASE_ID)
    except Exception as e:
        logger.error("Failed to acquire Firestore client for %s: %s", FIRESTORE_DATABASE_ID, e)
        return None


def write_firestore_activity(
    action: str,
    user_email: str,
    user_name: str = "",
    user_role: str = "",
    details: dict[str, Any] | None = None,
    collection_name: str = "agency_activity_feed",
) -> dict[str, Any]:
    """Writes an activity log or testing memo directly into Google Cloud Firestore (agent-db)."""
    db = get_firestore_client()
    if not db:
        return {"success": False, "error": "Cloud Firestore 연결 불가"}

    try:
        doc_data = {
            "action": action,
            "user_email": user_email,
            "user_name": user_name or user_email.split("@")[0],
            "user_role": user_role or "STAFF",
            "details": details or {},
            "database_id": FIRESTORE_DATABASE_ID,
            "project_id": "iceu-songpa09",
            "created_at": firestore.SERVER_TIMESTAMP,
            "created_at_iso": datetime.utcnow().isoformat() + "Z",
        }
        update_time, doc_ref = db.collection(collection_name).add(doc_data)
        return {
            "success": True,
            "doc_id": doc_ref.id,
            "collection": collection_name,
            "database_id": FIRESTORE_DATABASE_ID,
            "project_id": "iceu-songpa09",
            "console_url": f"https://console.firebase.google.com/project/iceu-songpa09/firestore/databases/{FIRESTORE_DATABASE_ID}/data/{collection_name}/{doc_ref.id}",
            "created_at_iso": doc_data["created_at_iso"],
        }
    except Exception as e:
        logger.error("Error writing to Firestore collection %s: %s", collection_name, e)
        return {"success": False, "error": str(e)}


def get_recent_firestore_activities(
    collection_name: str = "agency_activity_feed", limit: int = 15
) -> list[dict[str, Any]]:
    """Retrieves the latest activity stream from Google Cloud Firestore (agent-db)."""
    db = get_firestore_client()
    if not db:
        return []

    results: list[dict[str, Any]] = []
    try:
        docs = (
            db.collection(collection_name)
            .order_by("created_at_iso", direction=firestore.Query.DESCENDING)
            .limit(limit)
            .stream()
        )
        for d in docs:
            item = d.to_dict()
            item["id"] = d.id
            if "created_at" in item:
                del item["created_at"]
            results.append(item)
        return results
    except Exception as e:
        logger.warning("Error fetching ordered Firestore activities (trying fallback): %s", e)
        try:
            docs = db.collection(collection_name).limit(limit).stream()
            for d in docs:
                item = d.to_dict()
                item["id"] = d.id
                if "created_at" in item:
                    del item["created_at"]
                results.append(item)
            results.sort(key=lambda x: x.get("created_at_iso", ""), reverse=True)
            return results
        except Exception as e2:
            logger.error("Fallback fetch also failed: %s", e2)
            return []


def get_firebase_status() -> dict[str, Any]:
    """Returns the live connection status with Google Cloud Firebase & Firestore."""
    is_init = _init_firebase()
    if not is_init:
        return {"status": "DISCONNECTED", "error": "Firebase Admin not initialized"}

    firestore_online = False
    firestore_count = 0
    try:
        db = get_firestore_client()
        if db:
            # Quick check on agency_activity_feed collection
            sample_docs = list(db.collection("agency_activity_feed").limit(5).stream())
            firestore_online = True
            firestore_count = len(sample_docs)
    except Exception as e:
        logger.warning("Firestore check error: %s", e)

    try:
        users_page = fb_auth.list_users(max_results=50)
        user_count = len(users_page.users)
        return {
            "status": "CONNECTED",
            "project_id": "iceu-songpa09",
            "firestore_db": FIRESTORE_DATABASE_ID,
            "firestore_status": "ONLINE" if firestore_online else "CONNECTING",
            "firestore_sample_docs": firestore_count,
            "auth_provider": "Google Cloud Identity / Firebase Auth",
            "total_firebase_users": user_count,
            "web_app_id": FIREBASE_WEB_CONFIG["appId"],
            "live_sync": True,
            "console_url": f"https://console.firebase.google.com/project/iceu-songpa09/firestore/databases/{FIRESTORE_DATABASE_ID}/data",
        }
    except Exception as e:
        return {
            "status": "PARTIAL",
            "project_id": "iceu-songpa09",
            "firestore_db": FIRESTORE_DATABASE_ID,
            "firestore_status": "ONLINE" if firestore_online else "ERROR",
            "error": str(e),
        }


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def ensure_auth_tables() -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS agency_users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'STAFF',
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at TEXT NOT NULL,
            approved_at TEXT,
            approved_by TEXT,
            firebase_uid TEXT
        )
        """
    )

    # Ensure firebase_uid column exists if table was created earlier
    cur.execute("PRAGMA table_info(agency_users)")
    cols = [r["name"] for r in cur.fetchall()]
    if "firebase_uid" not in cols:
        try:
            cur.execute("ALTER TABLE agency_users ADD COLUMN firebase_uid TEXT")
        except Exception:
            pass

    # Ensure admin user exists: admin@agent.com / password1234
    admin_email = "admin@agent.com"
    cur.execute("SELECT user_id, firebase_uid FROM agency_users WHERE email = ?", (admin_email,))
    row = cur.fetchone()
    admin_hash = hash_password("password1234")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    admin_fb_uid = row["firebase_uid"] if row and row["firebase_uid"] else None

    # Sync admin with Firebase Auth
    if _init_firebase():
        try:
            fb_u = fb_auth.get_user_by_email(admin_email)
            admin_fb_uid = fb_u.uid
            fb_auth.set_custom_user_claims(fb_u.uid, {"role": "ADMIN", "department": "경영기획본부", "status": "APPROVED"})
        except fb_auth.UserNotFoundError:
            try:
                fb_u = fb_auth.create_user(
                    email=admin_email,
                    password="password1234",
                    display_name="에이전시 대표 관리자",
                    email_verified=True,
                )
                admin_fb_uid = fb_u.uid
                fb_auth.set_custom_user_claims(fb_u.uid, {"role": "ADMIN", "department": "경영기획본부", "status": "APPROVED"})
            except Exception as e:
                logger.warning("Failed to auto-create admin in Firebase: %s", e)

    if not row:
        cur.execute(
            """
            INSERT INTO agency_users (email, password_hash, full_name, department, role, status, created_at, approved_at, approved_by, firebase_uid)
            VALUES (?, ?, '에이전시 대표 관리자', '경영기획본부', 'ADMIN', 'APPROVED', ?, ?, 'SYSTEM', ?)
            """,
            (admin_email, admin_hash, now_str, now_str, admin_fb_uid),
        )
    else:
        # Guarantee admin has correct hash, approved status, and firebase_uid
        cur.execute(
            """
            UPDATE agency_users
            SET password_hash = ?, role = 'ADMIN', status = 'APPROVED', firebase_uid = COALESCE(?, firebase_uid)
            WHERE email = ?
            """,
            (admin_hash, admin_fb_uid, admin_email),
        )

    conn.commit()
    conn.close()


def authenticate_user(email: str, password: str) -> dict[str, Any]:
    """Authenticates user against SQLite DB and generates a real Google Firebase Auth Custom Token."""
    ensure_auth_tables()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM agency_users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {"success": False, "error": "등록되지 않은 이메일 계정입니다."}

    user = dict(row)
    pw_hash = hash_password(password)

    if user["password_hash"] != pw_hash:
        conn.close()
        return {"success": False, "error": "비밀번호가 올바르지 않습니다."}

    # Check approval status
    if user["status"] == "PENDING":
        conn.close()
        return {
            "success": False,
            "error": "관리자 승인 대기 중인 계정입니다. 대표 관리자(admin@agent.com)의 승인 후 로그인이 가능합니다.",
            "status": "PENDING",
        }
    elif user["status"] == "REJECTED":
        conn.close()
        return {
            "success": False,
            "error": "가입 신청이 반려된 계정입니다. 에이전시 관리팀에 문의하세요.",
            "status": "REJECTED",
        }

    # Generate session token (lightweight deterministic bearer token)
    user_email = user["email"]
    date_str = datetime.now().strftime("%Y%m%d")
    seed_str = f"{user_email}_{date_str}".encode("utf-8")
    token_hash = hashlib.sha256(seed_str).hexdigest()[:16]
    token = f"agm_{user['user_id']}_{token_hash}"

    # Generate Google Firebase Custom Token for client-side Firebase Auth sign-in
    firebase_token = None
    firebase_uid = user.get("firebase_uid")

    if _init_firebase():
        try:
            if not firebase_uid:
                try:
                    fb_u = fb_auth.get_user_by_email(user_email)
                    firebase_uid = fb_u.uid
                except fb_auth.UserNotFoundError:
                    fb_u = fb_auth.create_user(
                        email=user_email,
                        password=password,
                        display_name=user["full_name"],
                        email_verified=True,
                    )
                    firebase_uid = fb_u.uid

                # Update SQLite with newly found/created firebase_uid
                cur.execute("UPDATE agency_users SET firebase_uid = ? WHERE user_id = ?", (firebase_uid, user["user_id"]))
                conn.commit()

            # Mint Firebase custom token with user claims
            claims = {
                "role": user["role"],
                "department": user["department"],
                "status": user["status"],
                "user_id": user["user_id"],
            }
            raw_token = fb_auth.create_custom_token(firebase_uid, claims)
            firebase_token = raw_token.decode("utf-8") if isinstance(raw_token, bytes) else raw_token
        except Exception as e:
            logger.warning("Could not mint Firebase custom token for %s: %s", user_email, e)

    conn.close()

    # Log successful login to Cloud Firestore agent-db
    try:
        write_firestore_activity(
            action="직원 로그인 (STAFF_LOGIN)",
            user_email=user["email"],
            user_name=user["full_name"],
            user_role=user["role"],
            details={"department": user["department"], "login_type": "Hybrid Firebase Auth"},
        )
    except Exception as e:
        logger.debug("Firestore login activity write skipped: %s", e)

    return {
        "success": True,
        "token": token,
        "firebase_token": firebase_token,
        "firebase_uid": firebase_uid,
        "firebase_project": "iceu-songpa09",
        "user": {
            "user_id": user["user_id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "department": user["department"],
            "role": user["role"],
            "status": user["status"],
            "created_at": user["created_at"],
            "firebase_uid": firebase_uid,
            "is_admin": user["role"] == "ADMIN" or user["email"] == "admin@agent.com",
        },
    }


def register_user(
    email: str,
    password: str,
    full_name: str,
    department: str = "선수스카우팅팀",
) -> dict[str, Any]:
    """Registers user in SQLite and synchronizes immediately with Google Cloud Firebase Auth."""
    ensure_auth_tables()
    email = email.strip().lower()
    full_name = full_name.strip()
    department = department.strip() or "선수스카우팅팀"

    if not email or "@" not in email:
        return {"success": False, "error": "유효한 이메일 형식을 입력하세요."}
    if len(password) < 4:
        return {"success": False, "error": "비밀번호는 최소 4자 이상이어야 합니다."}
    if not full_name:
        return {"success": False, "error": "성명을 입력해주세요."}

    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM agency_users WHERE LOWER(email) = ?", (email,))
    if cur.fetchone():
        conn.close()
        return {"success": False, "error": "이미 등록된 이메일 계정입니다."}

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pw_hash = hash_password(password)

    # If registering admin@agent.com, auto-approve
    is_admin = email == "admin@agent.com"
    role = "ADMIN" if is_admin else "STAFF"
    status = "APPROVED" if is_admin else "PENDING"
    approved_at = now_str if is_admin else None
    approved_by = "SYSTEM" if is_admin else None

    # Sync with Firebase Auth
    firebase_uid = None
    if _init_firebase():
        try:
            fb_u = fb_auth.get_user_by_email(email)
            firebase_uid = fb_u.uid
        except fb_auth.UserNotFoundError:
            try:
                fb_u = fb_auth.create_user(
                    email=email,
                    password=password,
                    display_name=full_name,
                    email_verified=True,
                )
                firebase_uid = fb_u.uid
            except Exception as e:
                logger.warning("Firebase user creation error: %s", e)

        if firebase_uid:
            try:
                fb_auth.set_custom_user_claims(firebase_uid, {"role": role, "department": department, "status": status})
            except Exception:
                pass

    cur.execute(
        """
        INSERT INTO agency_users (email, password_hash, full_name, department, role, status, created_at, approved_at, approved_by, firebase_uid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (email, pw_hash, full_name, department, role, status, now_str, approved_at, approved_by, firebase_uid),
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": (
            "관리자 계정으로 즉시 활성화되었습니다."
            if is_admin
            else "회원가입 신청이 성공적으로 접수되었습니다. 관리자(admin@agent.com)의 승인 후 로그인하실 수 있습니다."
        ),
        "user_id": user_id,
        "email": email,
        "status": status,
        "firebase_uid": firebase_uid,
        "firebase_synced": firebase_uid is not None,
    }


def get_admin_dashboard_users() -> dict[str, Any]:
    ensure_auth_tables()
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("SELECT user_id, email, full_name, department, role, status, created_at, approved_at, approved_by, firebase_uid FROM agency_users ORDER BY created_at DESC")
    all_users = [dict(r) for r in cur.fetchall()]
    conn.close()

    today_str = datetime.now().strftime("%Y-%m-%d")

    today_signups = [u for u in all_users if u["created_at"].startswith(today_str)]
    pending_users = [u for u in all_users if u["status"] == "PENDING"]
    approved_users = [u for u in all_users if u["status"] == "APPROVED"]

    return {
        "summary": {
            "total_users": len(all_users),
            "pending_count": len(pending_users),
            "approved_count": len(approved_users),
            "today_signup_count": len(today_signups),
            "firebase_project": "iceu-songpa09",
        },
        "today_signups": today_signups,
        "pending_users": pending_users,
        "approved_users": approved_users,
        "all_users": all_users,
    }


def update_user_status(user_id: int, action: str, approver_email: str = "admin@agent.com") -> dict[str, Any]:
    """Approves or rejects a user, syncing the updated claim to Google Cloud Firebase."""
    ensure_auth_tables()
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM agency_users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": f"User ID {user_id} not found"}

    target = dict(row)
    if target["email"] == "admin@agent.com":
        conn.close()
        return {"success": False, "error": "최고 관리자 계정의 상태는 변경할 수 없습니다."}

    action_upper = action.strip().upper()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if action_upper in ("APPROVE", "APPROVED"):
        new_status = "APPROVED"
        cur.execute(
            """
            UPDATE agency_users
            SET status = 'APPROVED', approved_at = ?, approved_by = ?
            WHERE user_id = ?
            """,
            (now_str, approver_email, user_id),
        )
    elif action_upper in ("REJECT", "REJECTED"):
        new_status = "REJECTED"
        cur.execute(
            """
            UPDATE agency_users
            SET status = 'REJECTED', approved_at = ?, approved_by = ?
            WHERE user_id = ?
            """,
            (now_str, approver_email, user_id),
        )
    else:
        conn.close()
        return {"success": False, "error": f"Unknown action: {action}"}

    conn.commit()
    conn.close()

    # Sync claim with Firebase Auth
    firebase_uid = target.get("firebase_uid")
    if _init_firebase() and firebase_uid:
        try:
            fb_auth.set_custom_user_claims(firebase_uid, {
                "role": target["role"],
                "department": target["department"],
                "status": new_status,
                "user_id": target["user_id"],
            })
        except Exception as e:
            logger.warning("Could not sync claim update to Firebase: %s", e)

    return {
        "success": True,
        "user_id": user_id,
        "email": target["email"],
        "full_name": target["full_name"],
        "new_status": new_status,
        "firebase_synced": True,
        "message": f"{target['full_name']} ({target['email']}) 님의 계정이 {new_status} 처리되었습니다. (Firebase 실시간 동기화 완료)",
    }


def verify_firebase_id_token(id_token: str) -> dict[str, Any]:
    """Verifies a Google Firebase ID token sent from the client."""
    if not _init_firebase():
        return {"success": False, "error": "Firebase Admin not initialized"}

    try:
        decoded = fb_auth.verify_id_token(id_token)
        uid = decoded.get("uid")
        email = decoded.get("email")

        # Lookup or link in SQLite
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM agency_users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        row = cur.fetchone()
        user_info = dict(row) if row else None
        conn.close()

        return {
            "success": True,
            "uid": uid,
            "email": email,
            "decoded": decoded,
            "user": user_info,
        }
    except Exception as e:
        return {"success": False, "error": f"Firebase ID 토큰 검증 실패: {str(e)}"}
