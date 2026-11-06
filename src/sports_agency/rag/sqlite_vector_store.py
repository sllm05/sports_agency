"""
SQLite Unified Vector DB (`src/sports_agency/rag/sqlite_vector_store.py`)

Stores both relational football data AND vector embeddings inside `data/agency_desk.db`:
1. `rag_regulations_vec` table:
   - Embedded with `gemini-embedding-2` (High-performance multimodal/long-context model)
   - Stores official UK FA GBE point rules, 5-League Non-EU quotas, FIFA FFAR Art. 15 & Circular 1873, EPL PSR rules.
2. `scouting_notes_vec` table:
   - Embedded with `gemini-embedding-001` / `text-embedding-004` (Lightweight fast text embedding model)
   - Stores player tactical profiles and club recruitment style notes for semantic tactical fit scoring.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import numpy as np

from sports_agency.config import CONFIG, ROUTER


class SQLiteAgencyVectorStore:
    """
    Unified SQLite Vector DB managing two distinct embedding spaces in `data/agency_desk.db`:
    - High-precision Regulation RAG (`gemini-embedding-2`)
    - Lightweight Tactical Scouting RAG (`gemini-embedding-001`)
    """

    def __init__(self, db_path: Path = CONFIG.db_path, docs_path: Path = CONFIG.docs_path) -> None:
        self.db_path = db_path
        self.docs_path = docs_path
        self.sqlite_vec_loaded = False
        self._ensure_tables()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            import sqlite_vec

            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            self.sqlite_vec_loaded = True
        except Exception:
            pass
        return conn

    def _ensure_tables(self) -> None:
        conn = self._get_conn()
        cur = conn.cursor()
        # Table 1: Legal & Regulations Vector Store (gemini-embedding-2)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS rag_regulations_vec (
                chunk_id TEXT PRIMARY KEY,
                doc_category TEXT NOT NULL,
                title TEXT NOT NULL,
                source_citation TEXT NOT NULL,
                effective_date TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_json TEXT NOT NULL
            )
            """
        )
        # Table 2: Player & Club Tactical Notes Vector Store (gemini-embedding-001)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scouting_notes_vec (
                note_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                entity_name TEXT NOT NULL,
                position TEXT NOT NULL,
                league TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def parse_regulations_markdown(self) -> list[dict[str, str]]:
        """Parses `data/docs/regulations.md` into structured legal chunks with source & effective date."""
        if not self.docs_path.exists():
            return []

        raw_text = self.docs_path.read_text(encoding="utf-8")
        sections = re.split(r"\n(?=## \[문서 )", raw_text)
        chunks: list[dict[str, str]] = []

        for idx, sec in enumerate(sections):
            sec = sec.strip()
            if not sec.startswith("## [문서"):
                continue

            lines = sec.splitlines()
            title = lines[0].replace("## ", "").strip()
            source = "FIFA / UEFA / FA Official Regulations"
            eff_date = "2024-2026 시즌"

            for line in lines[1:6]:
                if "**출처**:" in line:
                    source = line.split("**출처**:")[-1].strip()
                elif "**기준일**:" in line:
                    eff_date = line.split("**기준일**:")[-1].strip()

            # Split sub-sections (###) so retrieval is fine-grained
            sub_sections = re.split(r"\n(?=### )", sec)
            if len(sub_sections) == 1:
                chunks.append(
                    {
                        "chunk_id": f"reg_doc_{idx}_full",
                        "doc_category": self._infer_category(title),
                        "title": title,
                        "source_citation": source,
                        "effective_date": eff_date,
                        "content": sec,
                    }
                )
            else:
                header_intro = sub_sections[0].strip()
                for sub_idx, sub in enumerate(sub_sections[1:], start=1):
                    sub_lines = sub.strip().splitlines()
                    sub_title = sub_lines[0].replace("### ", "").strip()
                    combined_content = f"{header_intro}\n\n{sub.strip()}"
                    chunks.append(
                        {
                            "chunk_id": f"reg_doc_{idx}_sub_{sub_idx}",
                            "doc_category": self._infer_category(title + " " + sub_title),
                            "title": f"{title} — {sub_title}",
                            "source_citation": source,
                            "effective_date": eff_date,
                            "content": combined_content,
                        }
                    )
        return chunks

    @staticmethod
    def _infer_category(title: str) -> str:
        t = title.lower()
        if "gbe" in t or "워크퍼밋" in t:
            return "GBE_WORK_PERMIT"
        if "non-eu" in t or "외국인" in t or "쿼터" in t:
            return "NON_EU_QUOTA"
        if "ffar" in t or "수수료" in t:
            return "FIFA_FFAR_FEE"
        return "PSR_CONTRACT_LAW"

    def ensure_indexed(self, force_reindex: bool = False) -> dict[str, Any]:
        """
        Ensures both `rag_regulations_vec` (via `gemini-embedding-2`) and
        `scouting_notes_vec` (via `gemini-embedding-001`) are populated in SQLite.
        """
        conn = self._get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as cnt FROM rag_regulations_vec")
        reg_count = cur.fetchone()["cnt"]

        cur.execute("SELECT COUNT(*) as cnt FROM scouting_notes_vec")
        scout_count = cur.fetchone()["cnt"]

        reg_model_used = CONFIG.primary_embedding_model
        scout_model_used = CONFIG.light_embedding_model

        if force_reindex or reg_count == 0:
            chunks = self.parse_regulations_markdown()
            if chunks:
                texts = [f"{c['title']}\n출처: {c['source_citation']}\n{c['content']}" for c in chunks]
                vectors, reg_model_used = ROUTER.embed_texts(texts, use_light_model=False)
                cur.execute("DELETE FROM rag_regulations_vec")
                for chunk, vec in zip(chunks, vectors):
                    cur.execute(
                        """
                        INSERT INTO rag_regulations_vec
                        (chunk_id, doc_category, title, source_citation, effective_date, content, embedding_model, embedding_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            chunk["chunk_id"],
                            chunk["doc_category"],
                            chunk["title"],
                            chunk["source_citation"],
                            chunk["effective_date"],
                            chunk["content"],
                            reg_model_used,
                            json.dumps(vec),
                        ),
                    )
                reg_count = len(chunks)

        if force_reindex or scout_count == 0:
            # Build scouting & tactical notes from existing players and club_squad_needs in SQLite
            cur.execute(
                "SELECT player_id, name, name_ko, position, league, strengths_summary "
                "FROM players WHERE is_agency_client = 1 OR market_value_eur >= 40000000"
            )
            players = [dict(r) for r in cur.fetchall()]
            cur.execute(
                "SELECT need_id, club_name, position, league, tactical_style, recruitment_note FROM club_squad_needs"
            )
            clubs = [dict(r) for r in cur.fetchall()]

            notes: list[dict[str, str]] = []
            for p in players:
                notes.append(
                    {
                        "note_id": f"player_{p['player_id']}",
                        "entity_type": "PLAYER",
                        "entity_name": f"{p['name_ko']} ({p['name']})",
                        "position": p["position"],
                        "league": p["league"],
                        "content": f"[{p['position']}] {p['name_ko']}: {p['strengths_summary']}",
                    }
                )
            for c in clubs:
                notes.append(
                    {
                        "note_id": f"club_{c['need_id']}",
                        "entity_type": "CLUB_NEED",
                        "entity_name": c["club_name"],
                        "position": c["position"],
                        "league": c["league"],
                        "content": f"[{c['club_name']} - {c['position']}] 전술 스타일: {c['tactical_style']} | 영입 니즈: {c['recruitment_note']}",
                    }
                )

            if notes:
                texts = [n["content"] for n in notes]
                vectors, scout_model_used = ROUTER.embed_texts(texts, use_light_model=True)
                cur.execute("DELETE FROM scouting_notes_vec")
                for note, vec in zip(notes, vectors):
                    cur.execute(
                        """
                        INSERT INTO scouting_notes_vec
                        (note_id, entity_type, entity_name, position, league, content, embedding_model, embedding_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            note["note_id"],
                            note["entity_type"],
                            note["entity_name"],
                            note["position"],
                            note["league"],
                            note["content"],
                            scout_model_used,
                            json.dumps(vec),
                        ),
                    )
                scout_count = len(notes)

        conn.commit()
        conn.close()
        return {
            "sqlite_db_path": str(self.db_path),
            "sqlite_vec_extension": self.sqlite_vec_loaded,
            "rag_regulations_chunks": reg_count,
            "rag_regulations_embedding_model": reg_model_used,
            "scouting_notes_chunks": scout_count,
            "scouting_notes_embedding_model": scout_model_used,
        }

    def search_regulations(
        self,
        query: str,
        top_k: int = 4,
        category_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Searches `rag_regulations_vec` using `gemini-embedding-2` query vector + cosine similarity.
        """
        self.ensure_indexed()
        q_vecs, model_used = ROUTER.embed_texts([query], use_light_model=False)
        q_vec = np.array(q_vecs[0], dtype=np.float32)
        q_norm = np.linalg.norm(q_vec) or 1.0

        conn = self._get_conn()
        cur = conn.cursor()
        if category_filter:
            cur.execute(
                "SELECT * FROM rag_regulations_vec WHERE doc_category = ?",
                (category_filter,),
            )
        else:
            cur.execute("SELECT * FROM rag_regulations_vec")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        results: list[dict[str, Any]] = []
        q_terms = [t for t in query.lower().split() if len(t) >= 2]

        for row in rows:
            doc_vec = np.array(json.loads(row["embedding_json"]), dtype=np.float32)
            doc_norm = np.linalg.norm(doc_vec) or 1.0
            cosine_sim = float(np.dot(q_vec, doc_vec) / (q_norm * doc_norm))

            # Hybrid keyword boost for exact legal terms (GBE, FFAR, Non-EU, 라리가, EPL, etc.)
            text_lower = (row["title"] + " " + row["content"]).lower()
            keyword_hits = sum(1 for term in q_terms if term in text_lower)
            hybrid_score = round(cosine_sim + min(0.25, keyword_hits * 0.05), 4)

            results.append(
                {
                    "chunk_id": row["chunk_id"],
                    "doc_category": row["doc_category"],
                    "title": row["title"],
                    "source_citation": row["source_citation"],
                    "effective_date": row["effective_date"],
                    "content": row["content"],
                    "embedding_model": row["embedding_model"],
                    "query_embedding_model": model_used,
                    "similarity_score": hybrid_score,
                }
            )

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def search_tactical_fit(
        self,
        player_strengths: str,
        position: str,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Searches `scouting_notes_vec` using lightweight `gemini-embedding-001` (`text-embedding-004`)
        to score semantic tactical similarity between a player's strengths and club recruitment notes.
        """
        self.ensure_indexed()
        q_vecs, model_used = ROUTER.embed_texts([player_strengths], use_light_model=True)
        q_vec = np.array(q_vecs[0], dtype=np.float32)
        q_norm = np.linalg.norm(q_vec) or 1.0

        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM scouting_notes_vec WHERE entity_type = 'CLUB_NEED' AND position = ?",
            (position,),
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        results: list[dict[str, Any]] = []
        for row in rows:
            doc_vec = np.array(json.loads(row["embedding_json"]), dtype=np.float32)
            doc_norm = np.linalg.norm(doc_vec) or 1.0
            cosine_sim = float(np.dot(q_vec, doc_vec) / (q_norm * doc_norm))
            results.append(
                {
                    "club_name": row["entity_name"],
                    "league": row["league"],
                    "position": row["position"],
                    "tactical_note": row["content"],
                    "embedding_model": model_used,
                    "tactical_similarity_score": round(cosine_sim, 4),
                }
            )

        results.sort(key=lambda x: x["tactical_similarity_score"], reverse=True)
        return results[:top_k]


VECTOR_STORE = SQLiteAgencyVectorStore()
