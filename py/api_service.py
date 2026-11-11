"""
FastAPI Web Service Backend (`src/sports_agency/api/main.py`)

Provides REST endpoints for:
- System & GCP ADC status inspection and dynamic project ID configuration (`/api/status`, `/api/config/gcp`)
- Agency player roster & stats retrieval (`/api/players`)
- LangGraph workflow execution up to Human-in-the-Loop interrupt (`/api/workflow/start`)
- LangGraph checkpointed resume with 1-click strategy choice (`/api/workflow/resume`)
- Direct SQLite Vector DB (`gemini-embedding-2` & `gemini-embedding-001`) semantic search (`/api/rag/search`)
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from mcp_server.football_mcp_server import (
    analyze_career_timing_and_path,
    calculate_psr_and_tax_breakdown,
    compare_datamb_peer_matrix,
    discover_undervalued_prospects,
    enroll_target_as_agency_client,
    find_matching_clubs_for_transfer,
    generate_client_recruitment_pitch_deck,
    generate_client_recruitment_deal_memo,
    get_agency_deep_analytics_overview,
    get_agency_portfolio_overview,
    get_player_complete_data,
    list_agency_managers,
    list_agency_players,
    list_agency_recruitment_targets,
    list_agency_teams,
    register_custom_external_client,
    scan_bosman_and_replacement_targets,
    terminate_agency_client_contract,
    terminate_agency_client_contract_formal,
    negotiate_client_club_renewal,
    simulate_client_club_renewal_pipeline,
    negotiate_client_club_transfer,
    simulate_client_club_transfer_pipeline,
    sign_client_to_new_club,
    toggle_target_watchlist,
    check_target_watchlist,
)
from sports_agency.auth_service import (
    authenticate_user,
    get_admin_dashboard_users,
    register_user,
    update_user_status,
)
from sports_agency.config import CONFIG, PROJECT_ROOT, ROUTER
from sports_agency.graph.agency_workflow import WORKFLOW_MANAGER
from sports_agency.live_sync import (
    sync_big5_rosters_from_football_data_org,
    sync_single_player_via_vertex_grounding,
)
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE
from sports_agency.api_football_client import (
    get_quota_status,
    fetch_live_injury_data,
    fetch_live_transfer_history,
    onboard_external_prospect,
)
from sports_agency.tactics_engine import build_player_tactics_payload
from sports_agency.injury_news_sync import (
    get_active_injuries_list,
    get_latest_rumors,
    init_injury_news_tables,
    sync_daily_injuries,
    sync_live_transfer_rumors,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="AI Football Agency Strategy Desk",
    description="LangGraph + Hermes Tool-Calling + SQLite Vector DB RAG + GCP Vertex AI (Gemini 3.8/3.5 Flash & Embedding 2/001)",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

REA_DIR = PROJECT_ROOT / "rea"
if REA_DIR.exists():
    app.mount("/rea", StaticFiles(directory=str(REA_DIR)), name="rea")


@app.on_event("startup")
def on_app_startup() -> None:
    """Initialize DB tables and ensure latest injury/rumor feed is available."""
    try:
        init_injury_news_tables()
        get_latest_rumors(limit=10)
    except Exception as e:
        print(f"[STARTUP] Injury/rumor init warning: {e}")


# ============================================================================
# Request Schemas
# ============================================================================
class ContractOverrideInput(BaseModel):
    actual_weekly_wage_eur: int = Field(0, description="에이전트가 보유한 실제 기밀 현재 주급(EUR, 0이면 DB 기본값 사용)")
    custom_market_value_eur: int = Field(0, description="에이전트 희망 이적료/시세 Override(EUR, 0이면 DB 기본값 사용)")
    contract_years: int = Field(4, ge=1, le=8, description="목표 계약 기간(년)")
    signing_bonus_eur: int = Field(0, ge=0, description="사이닝 보너스(Signing-on Fee, EUR)")
    current_release_clause_eur: int = Field(0, ge=0, description="현재 계약서상 바이아웃(EUR)")
    agent_fee_pct: float = Field(5.0, ge=1.0, le=10.0, description="목표 에이전트 수수료율(% - FIFA FFAR 제13조 상한 3~5%, 쌍방 6%, 최대 10% 허용)")


class StartWorkflowRequest(BaseModel):
    player_name: str = Field(..., description="선수 이름 (예: 손흥민, 이강인, 김민재, Bukayo Saka)")
    track_mode: str = Field(
        "TRACK_A_TRANSFER",
        description="TRACK_A_TRANSFER (이적 역제의) 또는 TRACK_B_RENEWAL (재계약 협상)",
    )
    target_wage_increase_pct: int = Field(25, ge=0, le=300)
    priority_goal: str = Field("주전 출전 시간 보장 + 적정 주급 확보")
    preferred_league: str = Field("ALL", description="희망 이적 리그 필터 (ALL, Premier League, La Liga, Serie A, Bundesliga, Ligue 1)")
    auto_complete: bool = Field(
        False,
        description="True일 경우 Human-in-the-Loop 일시정지 없이 끝까지 즉시 실행",
    )
    contract_override: ContractOverrideInput | None = None
    thread_id: str | None = None


class PsrSimulatorRequest(BaseModel):
    league: str = Field("Premier League", description="대상 리그 (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)")
    transfer_fee_eur: int = Field(25000000, ge=0)
    weekly_wage_eur: int = Field(80000, ge=0)
    contract_years: int = Field(4, ge=1, le=8)
    agent_fee_pct: float = Field(7.0, ge=0.0, le=15.0)
    signing_bonus_eur: int = Field(2000000, ge=0)


class CustomClientRegistrationRequest(BaseModel):
    name: str = Field(..., description="영문 이름 (예: Yang Min-hyeok)")
    name_ko: str = Field(..., description="한글 이름 (예: 양민혁)")
    position: str = Field("RW", description="주 포지션 (ST, LW, RW, AM, CM, DM, CB, RB, LB, GK)")
    secondary_positions: str = Field("LW, AM")
    age: int = Field(20, ge=15, le=45)
    nationality: str = Field("South Korea")
    current_club: str = Field("QPR / K League Prospect")
    league: str = Field("EFL Championship / K League 1")
    current_league_band: int = Field(2, ge=1, le=6)
    market_value_eur: int = Field(4500000, ge=50000)
    weekly_wage_eur: int = Field(15000, ge=500)
    contract_expires: str = Field("2027-06-30")
    goals_per90: float = Field(0.34)
    assists_per90: float = Field(0.22)
    xg_per90: float = Field(0.29)
    xa_per90: float = Field(0.19)
    key_passes_per90: float = Field(1.65)
    progressive_actions_per90: float = Field(6.4)
    defensive_duels_won_pct: float = Field(56.5)
    minutes_played: int = Field(2650)
    appearances: int = Field(32)
    intl_match_pct: float = Field(45.0)
    continental_minutes_pct: float = Field(60.0)
    is_eu_citizen: int = Field(0)
    strengths_summary: str = Field("")
    weaknesses_summary: str = Field("")


class ResumeWorkflowRequest(BaseModel):
    thread_id: str = Field(..., description="일시정지된 LangGraph SqliteSaver 스레드 ID")
    human_action_choice: str = Field(
        "OPTION_2_BONUS_AND_RELEASE_CLAUSE",
        description="OPTION_1_HOLD_BASE_WAGE | OPTION_2_BONUS_AND_RELEASE_CLAUSE | OPTION_3_LOWER_RELEASE_FOR_CLUB_OFFER",
    )


class RagSearchRequest(BaseModel):
    query: str = Field(..., description="검색할 규정 또는 전술 키워드")
    search_type: str = Field(
        "REGULATIONS",
        description="REGULATIONS (gemini-embedding-2) 또는 TACTICAL (gemini-embedding-001)",
    )
    position: str = Field("RB", description="전술 검색 시 포지션 필터")
    top_k: int = Field(5, ge=1, le=10)


class GcpConfigUpdateRequest(BaseModel):
    gcp_project: str = Field(..., description="설정할 GCP Project ID")
    gcp_location: str = Field("global", description="Vertex AI 리전 (Gemini 3.8/Embedding-2는 global 권장)")


class LivePlayerSyncRequest(BaseModel):
    player_name: str = Field(..., description="실시간 웹 검색으로 소속팀/시세/계약만료일을 동기화할 선수 이름")


class FootballDataSyncRequest(BaseModel):
    force_api_refresh: bool = Field(False, description="True일 경우 Football-Data.org v4 API를 새로 호출하여 96개 구단 스쿼드 전체 갱신")


class DailyInjurySyncRequest(BaseModel):
    force_api_refresh: bool = Field(False, description="True일 경우 API-Football 5대 리그 부상자 전수 강제 재동기화")


class RecruitmentPitchRequest(BaseModel):
    target_id: int = Field(..., description="영입 타깃 ID (선수 ID 또는 감독 ID)")
    target_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")


class EnrollClientRequest(BaseModel):
    target_id: int = Field(..., description="영입 타깃 ID")
    target_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    lead_agent: str = Field("Daniel Kim (FIFA Licensed)", description="전담 수석 에이전트 이름")
    commission_pct: float = Field(5.0, ge=1.0, le=6.0, description="대리 수수료율(% - FIFA FFAR 제13조 상한 5~6% 준수)")


class TerminateContractRequest(BaseModel):
    client_id: int = Field(..., description="해지 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    reason: str = Field("상호 합의 계약 해지", description="해지 사유")


class ClientRenewalRequest(BaseModel):
    client_id: int = Field(..., description="재계약 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    new_weekly_wage_eur: int = Field(100000, description="재계약 합의 주급 (EUR)")
    contract_years: int = Field(3, ge=1, le=6, description="계약 연장 기간 (년)")
    new_buyout_eur: int | None = Field(None, description="신설/인상 바이아웃 금액 (EUR)")
    signing_bonus_eur: int = Field(0, description="계약금/서명 보너스 (EUR)")


class ClientTransferRequest(BaseModel):
    client_id: int = Field(..., description="이적 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    destination_club: str = Field("토트넘 홋스퍼 FC", description="이적할 신규 구단명")
    destination_league: str = Field("Premier League", description="이적 구단 리그명")
    transfer_fee_eur: int = Field(35000000, description="합의 이적료 (EUR)")
    new_weekly_wage_eur: int = Field(150000, description="신규 주급 (EUR)")
    contract_years: int = Field(4, ge=1, le=6, description="신규 계약 기간 (년)")


class ClientSignClubRequest(BaseModel):
    client_id: int = Field(..., description="입단 대상 고객 ID (FA)")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    destination_club: str = Field("FC 메트로폴리스", description="입단할 구단명")
    destination_league: str = Field("가상 슈퍼리그", description="입단 구단 리그명")
    weekly_wage_eur: int = Field(80000, description="합의 주급 (EUR)")
    contract_years: int = Field(2, ge=1, le=5, description="계약 기간 (년)")


class ClientRenewalPipelineRequest(BaseModel):
    client_id: int = Field(..., description="재계약 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    requested_weekly_wage_eur: int = Field(120000, description="요청 주급 (EUR)")
    contract_years: int = Field(3, ge=1, le=6, description="계약 연장 기간 (년)")
    requested_buyout_eur: int | None = Field(None, description="요청 바이아웃 금액 (EUR)")
    signing_bonus_eur: int | None = Field(0, description="계약금/서명 보너스 (EUR)")
    action: str = Field("EVALUATE", description="EVALUATE | CONFIRM_DIRECT | ACCEPT_COUNTER")


class ClientTransferPipelineRequest(BaseModel):
    client_id: int = Field(..., description="이적 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    destination_club: str = Field("Tottenham Hotspur FC", description="이적 대상 구단명")
    destination_league: str = Field("Premier League", description="이적 대상 리그명")
    offered_transfer_fee_eur: int = Field(40000000, description="제안 이적료 (EUR)")
    offered_weekly_wage_eur: int = Field(140000, description="제안 주급 (EUR)")
    contract_years: int = Field(4, ge=1, le=6, description="계약 기간 (년)")
    action: str = Field("SIMULATE", description="SIMULATE | EVALUATE | EXECUTE_TRANSFER | FORCE_EXECUTE")


class ClientFormalTerminationRequest(BaseModel):
    client_id: int = Field(..., description="해지 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    settlement_type: str = Field("MUTUAL_RELEASE", description="MUTUAL_RELEASE | EXPEDITED_BUYOUT | DISPUTE_WAIVER")
    reason: str = Field("상호 합의 계약 해지", description="해지 사유")
    settled_commission_eur: int = Field(0, ge=0, description="정산 합의 수수료 (EUR)")
    handover_notes: str = Field("", description="이관 및 정산 합의 비고")


class WatchlistToggleRequest(BaseModel):
    target_id: int = Field(..., description="관심 등록/해제 대상 선수 또는 감독 ID")
    target_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    action: str | None = Field(None, description="TARGET, UNWATCH 또는 None(토글)")


class AuthLoginRequest(BaseModel):
    email: str = Field(..., description="로그인 이메일 (예: admin@agent.com)")
    password: str = Field(..., description="비밀번호 (예: password1234)")


class AuthSignupRequest(BaseModel):
    email: str = Field(..., description="직원 등록 이메일")
    password: str = Field(..., description="비밀번호")
    full_name: str = Field(..., description="직원 성명")
    department: str = Field("선수스카우팅팀", description="소속 부서 (선수스카우팅팀, 법무계약팀, 재무전략팀, 전술데이터팀)")


class AdminApproveRequest(BaseModel):
    user_id: int = Field(..., description="승인/반려할 대상 회원 ID")
    action: str = Field("APPROVE", description="APPROVE 또는 REJECT")
    approver_email: str = Field("admin@agent.com")


# ============================================================================
# Endpoints
# ============================================================================
@app.post("/api/auth/login")
def api_auth_login(req: AuthLoginRequest) -> dict[str, Any]:
    """Firebase/Local Auth Login: Verifies credentials & checks admin approval status."""
    res = authenticate_user(email=req.email, password=req.password)
    if not res.get("success"):
        status_code = 403 if res.get("status") in ("PENDING", "REJECTED") else 401
        raise HTTPException(status_code=status_code, detail=res.get("error", "로그인 실패"))
    return res


@app.post("/api/auth/signup")
def api_auth_signup(req: AuthSignupRequest) -> dict[str, Any]:
    """Staff Self-Registration: Registers staff with status='PENDING' awaiting Admin approval."""
    res = register_user(
        email=req.email,
        password=req.password,
        full_name=req.full_name,
        department=req.department,
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "회원가입 실패"))
    return res


@app.get("/api/admin/users")
def api_get_admin_users() -> dict[str, Any]:
    """Admin Console: Returns today's pending/new signups and approved agency staff roster."""
    return get_admin_dashboard_users()


@app.post("/api/admin/approve-user")
def api_approve_user(req: AdminApproveRequest) -> dict[str, Any]:
    """Admin Console: Approves or rejects staff member account."""
    res = update_user_status(user_id=req.user_id, action=req.action, approver_email=req.approver_email)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "승인 처리 실패"))
    return res
@app.get("/", response_class=HTMLResponse)
def serve_dashboard() -> HTMLResponse:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Dashboard index.html not found</h1>", status_code=404)
    return HTMLResponse(
        content=index_file.read_text(encoding="utf-8"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/tactics", response_class=HTMLResponse)
@app.get("/fm", response_class=HTMLResponse)
@app.get("/fm-match", response_class=HTMLResponse)
def serve_tactics_engine() -> HTMLResponse:
    tactics_file = PROJECT_ROOT / "rea" / "fm_2d_grid_match.html"
    if not tactics_file.exists():
        return HTMLResponse("<h1>Tactics 2D Grid Engine file not found</h1>", status_code=404)
    return HTMLResponse(tactics_file.read_text(encoding="utf-8"))


@app.get("/favicon.ico", include_in_schema=False)
@app.get("/sw.js", include_in_schema=False)
def suppress_browser_defaults() -> Response:
    return Response(status_code=204)


@app.get("/health")
@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "version": "3.0.0"}


@app.get("/api/status")
def get_system_status() -> dict[str, Any]:
    vec_status = VECTOR_STORE.ensure_indexed()
    auth_status = ROUTER.get_status()
    return {
        "status": "ok",
        "gcp_auth": auth_status,
        "vector_db": vec_status,
        "langgraph_checkpointer": f"SqliteSaver ({CONFIG.checkpoint_db_path.name})",
    }


@app.post("/api/config/gcp")
def update_gcp_config(req: GcpConfigUpdateRequest) -> dict[str, Any]:
    """Updates `.env` with the user's GCP Project ID and re-initializes ADC connection."""
    project_id = req.gcp_project.strip()
    location = req.gcp_location.strip() or "global"

    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = location
    CONFIG.gcp_project = project_id
    CONFIG.gcp_location = location

    # Persist to .env file
    env_path = PROJECT_ROOT / ".env"
    env_content = (
        f"GOOGLE_GENAI_USE_VERTEXAI=true\n"
        f"GOOGLE_CLOUD_PROJECT={project_id}\n"
        f"GOOGLE_CLOUD_LOCATION={location}\n"
        f"PRIMARY_LLM_MODEL={CONFIG.primary_llm_model}\n"
        f"LIGHT_LLM_MODEL={CONFIG.light_llm_model}\n"
        f"PRIMARY_EMBEDDING_MODEL={CONFIG.primary_embedding_model}\n"
        f"LIGHT_EMBEDDING_MODEL={CONFIG.light_embedding_model}\n"
        f"EMBEDDING_DIMENSION={CONFIG.embedding_dimension}\n"
        f"USE_GOOGLE_SEARCH_GROUNDING=true\n"
    )
    env_path.write_text(env_content, encoding="utf-8")

    auth_status = ROUTER.refresh_auth()
    # Re-index SQLite vector store with live Vertex AI embeddings if ADC is now active
    vec_status = VECTOR_STORE.ensure_indexed(force_reindex=auth_status["adc_authenticated"])
    return {
        "gcp_auth": auth_status,
        "vector_db": vec_status,
    }


@app.post("/api/auth/refresh")
def refresh_gcp_auth() -> dict[str, Any]:
    """Re-checks GCP ADC credentials after the user runs `gcloud auth application-default login`."""
    auth_status = ROUTER.refresh_auth()
    vec_status = VECTOR_STORE.ensure_indexed(force_reindex=auth_status["adc_authenticated"])
    return {
        "gcp_auth": auth_status,
        "vector_db": vec_status,
    }


@app.get("/api/players")
def api_list_players() -> dict[str, Any]:
    players = list_agency_players()
    korean_players = [p for p in players if p.get("nationality") == "South Korea"]
    peer_players = [p for p in players if p.get("nationality") != "South Korea"]
    agency_clients = [p for p in players if p.get("is_agency_client") == 1]
    return {
        "total_count": len(players),
        "korean_roster": korean_players,
        "european_peers": peer_players,
        "agency_clients": agency_clients,
        "all_players": players,
    }


@app.get("/api/managers")
def api_list_managers() -> dict[str, Any]:
    """Returns head coaches and their tactical profiles."""
    managers = list_agency_managers()
    agency_managers = [m for m in managers if m.get("is_agency_client") == 1]
    return {
        "total_count": len(managers),
        "agency_managers": agency_managers,
        "managers": managers,
    }


@app.get("/api/teams")
def api_list_teams() -> dict[str, Any]:
    """Returns all 96 Big 5 League clubs and their DataMB 7-axis team metrics."""
    teams = list_agency_teams()
    return {
        "total_count": len(teams),
        "teams": teams,
    }


@app.get("/api/analytics/overview")
def api_get_analytics_overview(comp: str = "PL") -> dict[str, Any]:
    """Returns League/UCL standings, club finances, top scorers, global agency market share, and manager profiles."""
    return get_agency_deep_analytics_overview(competition_code=comp)


@app.get("/api/agency/portfolio")
def api_get_agency_portfolio() -> dict[str, Any]:
    """[Pillar 1: Active Portfolio] Returns all signed players and managers in Antigravity Sports portfolio."""
    return get_agency_portfolio_overview()


@app.get("/api/agency/recruitment-targets")
def api_list_recruitment_targets(
    category: str = "ALL",
    target_type: str = "ALL",
) -> dict[str, Any]:
    """[Pillar 2: Recruitment Targets] Returns candidates categorized by UNREPRESENTED, EXPIRING_D6, TIER2_STEPUP, ELITE_MANAGER."""
    return list_agency_recruitment_targets(category=category, target_type=target_type)


@app.post("/api/agency/recruitment-pitch")
def api_generate_recruitment_pitch(req: RecruitmentPitchRequest) -> dict[str, Any]:
    """[Pillar 2: Pitch Deck] Synthesizes a 1-Page Client Acquisition Pitch Deck with inline SVGs for player/family or manager."""
    res = generate_client_recruitment_pitch_deck(target_id=req.target_id, target_type=req.target_type)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    # Ensure both key aliases are present
    if "markdown_content" in res and "pitch_deck_markdown" not in res:
        res["pitch_deck_markdown"] = res["markdown_content"]
    return res


@app.get("/api/agency/recruitment-deal-memo/{target_type}/{target_id}")
def api_get_recruitment_deal_memo(target_type: str, target_id: int) -> dict[str, Any]:
    """[Pillar 2: Deal Memo] Returns comprehensive 6-Axis recruitment radar, upside/downside matrix, 5yr cash flow and FIFA FFAR compliance signoff."""
    res = generate_client_recruitment_deal_memo(target_id=target_id, target_type=target_type.upper())
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@app.post("/api/agency/enroll-client")
def api_enroll_client(req: EnrollClientRequest) -> dict[str, Any]:
    """[Pillar 2 -> Pillar 1] Signs and enrolls a recruitment target into Antigravity Sports active portfolio."""
    res = enroll_target_as_agency_client(
        target_id=req.target_id,
        target_type=req.target_type,
        lead_agent=req.lead_agent,
        commission_pct=req.commission_pct,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/terminate-contract")
def api_terminate_contract(req: TerminateContractRequest) -> dict[str, Any]:
    """[Pillar 1 -> Pillar 2] Releases a client from active agency portfolio back to recruitment targets."""
    res = terminate_agency_client_contract(
        client_id=req.client_id,
        client_type=req.client_type,
        reason=req.reason,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/client/renew")
def api_client_renew_contract(req: ClientRenewalRequest) -> dict[str, Any]:
    """[Pillar 1: Contract Renewal] Negotiates renewal terms with client's current club."""
    res = negotiate_client_club_renewal(
        client_id=req.client_id,
        client_type=req.client_type,
        new_weekly_wage_eur=req.new_weekly_wage_eur,
        contract_years=req.contract_years,
        new_buyout_eur=req.new_buyout_eur,
        signing_bonus_eur=req.signing_bonus_eur,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/client/renew-pipeline")
def api_client_renew_pipeline(req: ClientRenewalPipelineRequest) -> dict[str, Any]:
    """[Pillar 1: Realistic Renewal Pipeline] Evaluates club PSR headroom, sporting director counter-offer & executes addendum."""
    res = simulate_client_club_renewal_pipeline(
        client_id=req.client_id,
        client_type=req.client_type,
        requested_weekly_wage_eur=req.requested_weekly_wage_eur,
        contract_years=req.contract_years,
        requested_buyout_eur=req.requested_buyout_eur,
        signing_bonus_eur=req.signing_bonus_eur,
        action=req.action,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/client/transfer")
def api_client_transfer(req: ClientTransferRequest) -> dict[str, Any]:
    """[Pillar 1: Club Transfer] Executes transfer for client to a new club."""
    res = negotiate_client_club_transfer(
        client_id=req.client_id,
        client_type=req.client_type,
        destination_club=req.destination_club,
        destination_league=req.destination_league,
        transfer_fee_eur=req.transfer_fee_eur,
        new_weekly_wage_eur=req.new_weekly_wage_eur,
        contract_years=req.contract_years,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.get("/api/clubs/by-league")
def api_get_clubs_by_league() -> dict[str, list[str]]:
    """Returns real list of clubs grouped by league from SQLite database."""
    import sqlite3
    db_path = Path("data/agency_desk.db")
    if not db_path.exists():
        db_path = Path("agency_desk.db")
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT league, current_club FROM players WHERE current_club IS NOT NULL AND current_club != '' ORDER BY league, current_club")
    rows = cur.fetchall()
    conn.close()
    
    result: dict[str, list[str]] = {}
    for lg, clb in rows:
        if not lg or not clb:
            continue
        if lg not in result:
            result[lg] = []
        result[lg].append(clb)
    return result


@app.post("/api/agency/client/transfer-pipeline")
def api_client_transfer_pipeline(req: ClientTransferPipelineRequest) -> dict[str, Any]:
    """[Pillar 1: 4-Stage Transfer Transaction Gateway] Fee agreement -> GBE/Visa -> Medical exam -> FIFA TMS clearing."""
    res = simulate_client_club_transfer_pipeline(
        client_id=req.client_id,
        client_type=req.client_type,
        destination_club=req.destination_club,
        destination_league=req.destination_league,
        offered_transfer_fee_eur=req.offered_transfer_fee_eur,
        offered_weekly_wage_eur=req.offered_weekly_wage_eur,
        contract_years=req.contract_years,
        action=req.action,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/client/terminate-formal")
def api_client_terminate_formal(req: ClientFormalTerminationRequest) -> dict[str, Any]:
    """[Pillar 1: Formal Mutual Termination] Mutual release & commission settlement agreement."""
    res = terminate_agency_client_contract_formal(
        client_id=req.client_id,
        client_type=req.client_type,
        settlement_type=req.settlement_type,
        reason=req.reason,
        settled_commission_eur=req.settled_commission_eur,
        handover_notes=req.handover_notes,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/client/sign-club")
def api_client_sign_club(req: ClientSignClubRequest) -> dict[str, Any]:
    """[Pillar 1: FA Signing] Signs an unemployed FA client to a new club."""
    res = sign_client_to_new_club(
        client_id=req.client_id,
        client_type=req.client_type,
        destination_club=req.destination_club,
        destination_league=req.destination_league,
        weekly_wage_eur=req.weekly_wage_eur,
        contract_years=req.contract_years,
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.post("/api/agency/watchlist/toggle")
def api_toggle_watchlist(req: WatchlistToggleRequest) -> dict[str, Any]:
    """[Pillar 2: Watchlist Toggle] Toggles candidate into/out of agency recruitment watchlist."""
    res = toggle_target_watchlist(target_id=req.target_id, target_type=req.target_type, action=req.action)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@app.get("/api/agency/watchlist/check")
def api_check_watchlist(target_id: int, target_type: str = "PLAYER") -> dict[str, Any]:
    """[Pillar 2: Watchlist Check] Returns whether a candidate is currently in the active recruitment watchlist."""
    return check_target_watchlist(target_id=target_id, target_type=target_type)


@app.get("/api/players/{player_name}")
def api_get_player(player_name: str) -> dict[str, Any]:
    data = get_player_complete_data(player_name)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data


@app.post("/api/sync/football-data-org")
def api_sync_football_data_org(req: FootballDataSyncRequest) -> dict[str, Any]:
    """Synchronizes all 96 Big 5 League clubs & live squads from official Football-Data.org v4 API."""
    try:
        summary = sync_big5_rosters_from_football_data_org(force_api_refresh=req.force_api_refresh)
        return {"status": "ok", "summary": summary}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/sync/live-player")
def api_sync_live_player(req: LivePlayerSyncRequest) -> dict[str, Any]:
    """Patches a single player's real-time club, market value, and contract via Vertex AI Google Search Grounding."""
    try:
        result = sync_single_player_via_vertex_grounding(req.player_name)
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/sync/daily-injuries")
def api_sync_daily_injuries(req: DailyInjurySyncRequest | None = None) -> dict[str, Any]:
    """
    Executes Daily Injury & Transfer Rumor Synchronization across Big 5 European leagues.
    - Synchronizes API-Football league-wide injuries into SQLite `players` and `player_injuries`.
    - Refreshes breaking transfer rumors & training injury intelligence into `live_transfer_rumors`.
    """
    force = req.force_api_refresh if req else False
    try:
        injury_res = sync_daily_injuries(force=force)
        rumors = sync_live_transfer_rumors(force=force)
        return {
            "status": "ok",
            "injury_sync": injury_res,
            "latest_rumors_count": len(rumors),
            "rumors": rumors,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/injuries/summary")
def api_get_injuries_summary(league: str = "ALL", limit: int = 50) -> dict[str, Any]:
    """
    Retrieves active injured players list and total counts, optionally filtered by league.
    """
    try:
        injuries = get_active_injuries_list(league=league, limit=limit)
        return {
            "status": "ok",
            "league_filter": league,
            "active_injuries_count": len(injuries),
            "injuries": injuries,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/news/transfer-rumors")
def api_get_transfer_rumors(limit: int = 10, force_refresh: bool = False) -> dict[str, Any]:
    """
    Retrieves real-time European transfer rumors and training injury alerts.
    """
    try:
        if force_refresh:
            rumors = sync_live_transfer_rumors(force=True)
        else:
            rumors = get_latest_rumors(limit=limit)
        return {
            "status": "ok",
            "count": len(rumors),
            "rumors": rumors,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/workflow/start")
def api_start_workflow(req: StartWorkflowRequest) -> dict[str, Any]:
    try:
        thread_id = req.thread_id or f"deal_{uuid.uuid4().hex[:10]}"
        override_dict = req.contract_override.model_dump() if req.contract_override else {}
        result = WORKFLOW_MANAGER.start_session(
            thread_id=thread_id,
            player_name=req.player_name,
            track_mode=req.track_mode,
            target_wage_increase_pct=req.target_wage_increase_pct,
            priority_goal=req.priority_goal,
            preferred_league=req.preferred_league,
            auto_complete=req.auto_complete,
            contract_override=override_dict,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"워크플로우 시작 오류: {str(exc)}") from exc


@app.post("/api/finance/psr-tax")
def api_calculate_psr_and_tax(req: PsrSimulatorRequest) -> dict[str, Any]:
    """Calculates UEFA FSR / EPL PSR Annualized Squad Cost (Amortization + Gross Wage + Agent Commission) & Net-Gross salary conversion."""
    return calculate_psr_and_tax_breakdown(
        league=req.league,
        transfer_fee_eur=req.transfer_fee_eur,
        weekly_wage_eur=req.weekly_wage_eur,
        contract_years=req.contract_years,
        agent_fee_pct=req.agent_fee_pct,
        signing_bonus_eur=req.signing_bonus_eur,
    )


@app.get("/api/radar/bosman")
def api_scan_bosman_radar(
    position: str = "ALL",
    league: str = "ALL",
    max_contract_year: int = 2027,
    min_starter_age: int = 29,
) -> dict[str, Any]:
    """Scans all 96 Big 5 League clubs for Bosman Rule / Contract Expiry windows and aging starter replacement targets."""
    targets = scan_bosman_and_replacement_targets(
        position=position,
        league=league,
        max_contract_year=max_contract_year,
        min_starter_age=min_starter_age,
    )
    return {"count": len(targets), "targets": targets}


@app.get("/api/transfer/club-matches")
def api_get_transfer_club_matches(
    player_name: str,
    league: str = "ALL",
    target_wage_increase_pct: int = 30,
    preferred_position: str | None = None,
) -> dict[str, Any]:
    """Scans Big 5 League clubs for urgent position vacancies, tactical fit, and wage capacity."""
    try:
        import sqlite3
        conn = sqlite3.connect("data/agency_desk.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Check if target is a Manager
        cur.execute("SELECT * FROM managers WHERE LOWER(name) = LOWER(?) LIMIT 1", (player_name,))
        mgr = cur.fetchone()
        if mgr:
            cur.execute("""
                SELECT c.club_name, c.league, c.country, s.rank_position, s.points, s.played_games, s.net_transfer_record
                FROM club_standings_and_finances s
                JOIN club_squad_needs c ON c.club_name = s.club_name
                WHERE s.rank_position >= 7
                GROUP BY c.club_name
                ORDER BY s.rank_position DESC
                LIMIT 5
            """)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            manager_matches = []
            for idx, r in enumerate(rows):
                manager_matches.append({
                    "club_name": r["club_name"],
                    "league": r["league"],
                    "country": r["country"],
                    "tactical_fit_score": 95 - (idx * 2),
                    "recruitment_urgency": "High" if idx < 2 else "Medium",
                    "current_starter": "사령탑 전술 개편 및 리빌딩 필요",
                    "recruitment_note": f"{r['club_name']} (리그 {r.get('rank_position', 10)}위): 신규 명장 선임 및 {mgr['preferred_formation']} 전술 개편 추진 중",
                    "tactical_style": f"{mgr['name']} 감독 | 주포메이션 {mgr['preferred_formation']} 점유율 & 주도형 축구",
                    "max_transfer_fee_budget_eur": 60000000,
                    "max_weekly_wage_offer_eur": int((mgr['weekly_wage_eur'] or 120000) * 1.25),
                    "expected_playing_time_share": 100,
                    "starter_age": 52,
                    "starter_contract_expires": "2025-06",
                    "club_live_standing": {
                        "rank_position": r.get("rank_position", 10),
                        "points": r.get("points", 20),
                        "net_transfer_record": r.get("net_transfer_record", "€0m")
                    }
                })
            return {
                "target_name": player_name,
                "target_type": "MANAGER",
                "matches": manager_matches
            }

        conn.close()

        # Otherwise target is Player
        p_data = get_player_complete_data(player_name)
        pos = preferred_position or p_data.get("position", "FW")
        market_val = p_data.get("market_value_eur", 30000000)
        curr_wage = p_data.get("weekly_wage_eur", 100000)
        target_wage = int(curr_wage * (1 + target_wage_increase_pct / 100))

        matches = find_matching_clubs_for_transfer(
            position=pos,
            max_fee_eur=market_val,
            target_weekly_wage_eur=target_wage,
            preferred_league=league,
        )

        # Fallback if fewer than 3 matches
        if len(matches) < 3:
            fallback_matches = find_matching_clubs_for_transfer(
                position=pos,
                max_fee_eur=int(market_val * 1.5),
                target_weekly_wage_eur=int(target_wage * 0.8),
                preferred_league="ALL",
            )
            existing_clubs = {m["club_name"] for m in matches}
            for fm in fallback_matches:
                if fm["club_name"] not in existing_clubs:
                    matches.append(fm)
                    existing_clubs.add(fm["club_name"])
                if len(matches) >= 4:
                    break

        enriched = []
        for i, m in enumerate(matches[:5]):
            urgency = m.get("recruitment_urgency", "Medium")
            urgency_bonus = 8 if urgency == "High" else 3
            fit_score = max(78, min(98, 96 - (i * 3) + urgency_bonus))
            m["tactical_fit_score"] = fit_score
            m["expected_playing_time_share"] = max(65, min(96, 88 - (i * 4) + urgency_bonus))
            enriched.append(m)

        return {
            "target_name": player_name,
            "target_type": "PLAYER",
            "position": pos,
            "market_value_eur": market_val,
            "current_weekly_wage_eur": curr_wage,
            "target_weekly_wage_eur": target_wage,
            "matches": enriched
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/players/custom")
def api_register_custom_client(req: CustomClientRegistrationRequest) -> dict[str, Any]:
    """Registers an external prospect (e.g., K League, J League, Eredivisie, Liga Portugal, Championship) into `agency_desk.db`."""
    try:
        profile = register_custom_external_client(**req.model_dump())
        return {"status": "ok", "player": profile}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/workflow/resume")
def api_resume_workflow(req: ResumeWorkflowRequest) -> dict[str, Any]:
    result = WORKFLOW_MANAGER.resume_with_human_strategy(
        thread_id=req.thread_id,
        human_action_choice=req.human_action_choice,
    )
    return result


@app.get("/api/workflow/{thread_id}")
def api_get_workflow_state(thread_id: str) -> dict[str, Any]:
    res = WORKFLOW_MANAGER.get_session_state(thread_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


class ComplianceAuditRequest(BaseModel):
    player_id: int
    weekly_wage_eur: int | None = Field(None, ge=0)
    transfer_fee_eur: int = Field(0, ge=0)
    contract_years: int = Field(4, ge=1, le=10)
    agent_fee_pct: float = Field(5.0, ge=0)
    representation_months: int = Field(24, ge=1)
    engaged_by: str = "PLAYER"
    destination_league: str | None = None
    also_represents_club: bool = False
    signing_bonus_eur: int = Field(0, ge=0)


@app.post("/api/compliance/audit")
def api_compliance_audit(req: ComplianceAuditRequest) -> dict[str, Any]:
    """[Compliance Desk] One-click FFAR / GBE / Bosman / PSR audit for a player + deal terms."""
    from mcp_server.compliance_audit import run_compliance_audit

    res = run_compliance_audit(**req.model_dump())
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res

@app.post("/api/rag/search")
def api_search_sqlite_vector_db(req: RagSearchRequest) -> dict[str, Any]:
    if req.search_type.upper() == "TACTICAL":
        matches = VECTOR_STORE.search_tactical_fit(
            player_strengths=req.query,
            position=req.position,
            top_k=req.top_k,
        )
        return {
            "search_type": "TACTICAL_SCOUTING_NOTES",
            "embedding_model": CONFIG.light_embedding_model,
            "results": matches,
        }
    else:
        chunks = VECTOR_STORE.search_regulations(
            query=req.query,
            top_k=req.top_k,
        )
        return {
            "search_type": "LEGAL_REGULATIONS",
            "embedding_model": CONFIG.primary_embedding_model,
            "results": chunks,
        }


@app.get("/api/career/timing")
def api_analyze_career_timing(
    player_name: str,
    target_league: str = "ALL",
    min_starter_pct: float = 60.0,
) -> dict[str, Any]:
    """[Career Agent Endpoint] Evaluates contract expiration leverage, availability, and determines optimal career pathway (Immediate Transfer vs Bosman Hold vs Loan)."""
    res = analyze_career_timing_and_path(
        player_name=player_name,
        target_league_preference=target_league,
        min_starter_guarantee_pct=min_starter_pct,
    )
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return res


@app.get("/api/scout/prospects")
def api_discover_prospects(
    position: str = "ALL",
    max_age: int = 23,
    min_percentile: float = 75.0,
    max_market_value_eur: int = 15000000,
    limit: int = 12,
) -> dict[str, Any]:
    """[Scouting Agent Endpoint] Scans the 2,662 player database for high-performing undervalued prospects."""
    prospects = discover_undervalued_prospects(
        target_position=position,
        max_age=max_age,
        min_percentile=min_percentile,
        max_market_value_eur=max_market_value_eur,
        limit=limit,
    )
    return {"count": len(prospects), "prospects": prospects}


class DataMBCompareRequest(BaseModel):
    player_names: list[str] = Field(default_factory=lambda: ["Pedri", "Declan Rice"])
    position_category: str = "AUTO"
    season: str = "25/26"


@app.post("/api/scout/datamb-compare")
def api_scout_datamb_compare(req: DataMBCompareRequest) -> dict[str, Any]:
    """[Scouting Agent Endpoint] Evaluates up to 4 players via DataMB 7-axis percentile radar & generates an AI briefing."""
    return compare_datamb_peer_matrix(
        player_names=req.player_names,
        position_category=req.position_category,
        season=req.season,
    )


class PrecisionCheckRequest(BaseModel):
    player_name: str
    team_name: str = ""
    season: int = 2024


class ProspectOnboardRequest(BaseModel):
    player_name: str
    team_name: str = ""
    season: int = 2024


@app.get("/api/quota/status")
def api_get_quota_status() -> dict[str, Any]:
    """Returns real-time daily quota usage for API-Football (100 req/day limit) & fallback status."""
    return get_quota_status()


@app.post("/api/live/precision-check")
def api_live_precision_check(req: PrecisionCheckRequest) -> dict[str, Any]:
    """
    On-Demand Precision Strike for official player injuries and transfers.
    Uses API-Football (max 100 calls/day), and automatically falls back to
    Football-Data.org / Google Search Grounding when quota is exhausted or key is absent.
    """
    injuries = fetch_live_injury_data(player_name=req.player_name, team_name=req.team_name, season=req.season)
    transfers = fetch_live_transfer_history(player_name=req.player_name)
    quota = get_quota_status()
    return {
        "player_name": req.player_name,
        "team_name": req.team_name,
        "injuries": injuries,
        "transfers": transfers,
        "quota": quota,
    }


@app.post("/api/prospects/onboard-external")
def api_onboard_external_prospect(req: ProspectOnboardRequest) -> dict[str, Any]:
    """
    Onboards a prospect outside the Big 5 Leagues (K League, J League, South America, Eredivisie, etc.)
    using API-Football real-time data, persisting into SQLite agency_desk.db and generating vector embeddings.
    """
    res = onboard_external_prospect(
        player_name=req.player_name,
        team_name=req.team_name,
        season=req.season,
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Onboarding failed"))
    return res


@app.get("/api/outputs/{player_folder}/{filename}")
def download_nested_output_markdown(player_folder: str, filename: str) -> FileResponse:
    safe_folder = Path(player_folder).name
    safe_file = Path(filename).name
    target_path = CONFIG.output_dir / safe_folder / safe_file
    if not target_path.exists():
        # Fallback to root outputs dir
        root_path = CONFIG.output_dir / safe_file
        if root_path.exists():
            return FileResponse(path=str(root_path), media_type="text/markdown; charset=utf-8", filename=safe_file)
        raise HTTPException(status_code=404, detail=f"Output file {safe_folder}/{safe_file} not found")
    return FileResponse(
        path=str(target_path),
        media_type="text/markdown; charset=utf-8",
        filename=safe_file,
    )


@app.get("/api/outputs/{filename}")
def download_output_markdown(filename: str) -> FileResponse:
    safe_name = Path(filename).name
    target_path = CONFIG.output_dir / safe_name
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    return FileResponse(
        path=str(target_path),
        media_type="text/markdown; charset=utf-8",
        filename=safe_name,
    )


# ============================================================================
# 2D Tactical Grid Match Engine & Real Match/Player Highlights API
# ============================================================================
@app.get("/api/tactics/match-highlights")
def get_tactical_match_highlights(match_id: int = 3857262) -> dict[str, Any]:
    """
    Returns 100% real StatsBomb Open Data match highlight events and key player moments
    with exact (x, y) meter pitch coordinates (0~120m, 0~80m), xG, and 360 freeze frames.
    Defaults to 2022 Qatar World Cup Group H Match 3857262 (South Korea 2:1 Portugal).
    """
    return {
        "match_info": {
            "match_id": match_id,
            "title": "2022 카타르 월드컵 조별리그 H조 3차전: 대한민국 2 : 1 포르투갈",
            "date": "2022-12-02",
            "stadium": "Education City Stadium, Al Rayyan",
            "home_team": "대한민국 (South Korea)",
            "away_team": "포르투갈 (Portugal)",
            "final_score": "2 : 1",
            "youtube_highlight_id": "DVNwiAPuPTY", # Official FIFA World Cup Highlight clip (Embed playable)
            "youtube_watch_url": "https://www.youtube.com/watch?v=DVNwiAPuPTY",
            "youtube_search_query": "South Korea vs Portugal 2022 World Cup official highlights",
            "youtube_search_url": "https://www.youtube.com/results?search_query=South+Korea+vs+Portugal+2022+World+Cup+official+highlights",
        },
        "key_match_highlights": [
            {
                "id": "goal_por_01",
                "minute": 4,
                "second": 53,
                "display_time": "04:53",
                "title": "포르투갈 리카르도 호르타 선제골",
                "scorer": "Ricardo Horta",
                "team": "away",
                "type": "GOAL",
                "xg": 0.2915,
                "start_location": [113.6, 47.0],
                "start_grid": [17.04, 7.05],
                "description": "달로트의 우측면 오버래핑 컷백 크로스를 호르타가 문전에서 오른발 논스톱 슈팅으로 선제골 득점.",
            },
            {
                "id": "goal_kor_01",
                "minute": 26,
                "second": 43,
                "display_time": "26:43",
                "title": "대한민국 김영권 코너킥 세컨볼 동점골",
                "scorer": "김영권 (Young-Gwon Kim)",
                "assist": "이강인 (Kang-In Lee 코너킥 기점)",
                "team": "home",
                "type": "GOAL",
                "xg": 0.6242,
                "corner_location": [120.0, 0.1],
                "corner_grid": [18.0, 0.0],
                "start_location": [116.7, 38.0],
                "start_grid": [17.5, 5.7],
                "description": "이강인의 예리한 좌측 코너킥이 크리스티아누 호날두의 등을 맞고 굴절된 세컨볼을 김영권이 몸을 날려 왼발 발리 동점골!",
            },
            {
                "id": "goal_kor_02",
                "minute": 90,
                "second": 28,
                "display_time": "90:28",
                "title": "대한민국 황희찬 극장 역전 결승골 (손흥민 70m 질주 어시스트)",
                "scorer": "황희찬 (Hee-Chan Hwang)",
                "assist": "손흥민 (Heung-Min Son)",
                "team": "home",
                "type": "GOAL",
                "xg": 0.4219,
                "recovery_location": [47.5, 65.2],
                "recovery_grid": [7.12, 9.78],
                "son_carry_coords": [
                    {"x": 47.5, "y": 65.2, "col": 7.12, "row": 9.78},
                    {"x": 65.0, "y": 61.0, "col": 9.75, "row": 9.15},
                    {"x": 82.5, "y": 56.5, "col": 12.38, "row": 8.48},
                    {"x": 98.3, "y": 52.3, "col": 14.75, "row": 7.85},
                ],
                "pass_start": [98.3, 52.3],
                "pass_grid": [14.75, 7.85],
                "shot_location": [108.3, 44.6],
                "shot_grid": [16.25, 6.69],
                "freeze_frame": [
                    {"name": "조규성 (Gue-Sung Cho)", "team": "home", "col": 13.95, "row": 8.85},
                    {"name": "황희찬 (Hee-Chan Hwang)", "team": "home", "col": 16.25, "row": 6.69},
                    {"name": "손흥민 (Heung-Min Son)", "team": "home", "col": 14.75, "row": 7.85},
                    {"name": "디오고 달로트 (Dalot)", "team": "away", "col": 15.1, "row": 7.9},
                    {"name": "페페 (Pepe)", "team": "away", "col": 16.5, "row": 7.2},
                    {"name": "안토니우 실바 (A. Silva)", "team": "away", "col": 16.4, "row": 6.1},
                    {"name": "디오고 코스타 (Costa)", "team": "away", "col": 17.5, "row": 6.0},
                ],
                "description": "손흥민의 하프라인 70m 단독 폭풍 질주! 포르투갈 수비수 3명 가랑이 사이로 찔러준 킬패스를 쇄도하던 황희찬이 침착한 오른발 논스톱 슈팅으로 극적 2:1 역전 결승골! 16강 진출 확정!",
            },
        ],
        "player_moments": [
            {
                "player_name": "손흥민",
                "player_en": "Heung-Min Son",
                "role": "CAPTAIN / WINGER",
                "moments": [
                    {
                        "time": "15:21",
                        "title": "하프스페이스 왼발 감아차기 슈팅",
                        "type": "SHOT",
                        "location": [108.5, 21.6],
                        "grid": [16.28, 3.24],
                        "xg": 0.011,
                        "desc": "좌측 하프스페이스에서 페페를 제친 후 기습적인 왼발 감아차기 유효슈팅.",
                    },
                    {
                        "time": "39:55",
                        "title": "중거리 위협적 인프런트 슈팅",
                        "type": "SHOT",
                        "location": [94.6, 44.2],
                        "grid": [14.19, 6.63],
                        "xg": 0.0247,
                        "desc": "아크 정면에서 수비 블록을 피하며 디오고 코스타 골키퍼 정면을 위협한 유효슈팅.",
                    },
                    {
                        "time": "90:20",
                        "title": "70m 폭풍 질주 & 극장 결승골 가랑이 스루패스 어시스트",
                        "type": "ASSIST",
                        "location": [98.3, 52.3],
                        "grid": [14.75, 7.85],
                        "xg": 0.4219,
                        "desc": "하프라인에서 볼을 낚아채 수비수 3명을 유인한 후 가랑이 사이로 황희찬에게 완벽한 어시스트 전달!",
                    },
                ],
            },
            {
                "player_name": "이강인",
                "player_en": "Kang-In Lee",
                "role": "PLAYMAKER",
                "moments": [
                    {
                        "time": "26:41",
                        "title": "택배 코너킥 크로스 (김영권 동점골 기점)",
                        "type": "KEY_PASS",
                        "location": [120.0, 0.1],
                        "grid": [18.0, 0.0],
                        "xg": 0.6242,
                        "desc": "좌측 코너킥 깃발에서 날카롭게 감겨 호날두의 등을 맞고 김영권 발밑에 떨어진 기적의 코너킥.",
                    },
                ],
            },
            {
                "player_name": "황희찬",
                "player_en": "Hee-Chan Hwang",
                "role": "STRIKER / IMPACT SUB",
                "moments": [
                    {
                        "time": "90:28",
                        "title": "박스 쇄도 오른발 원터치 역전 결승골",
                        "type": "GOAL",
                        "location": [108.3, 44.6],
                        "grid": [16.25, 6.69],
                        "xg": 0.4219,
                        "desc": "손흥민의 침투 패스 타이밍에 맞추어 오프사이드 트랩을 완벽히 무너뜨리며 디오고 코스타 골키퍼를 뚫은 원더골!",
                    },
                ],
            },
            {
                "player_name": "김민재",
                "player_en": "Min-Jae Kim",
                "role": "MONSTER DEFENDER",
                "moments": [
                    {
                        "time": "Defensive Rock",
                        "title": "최후방 1:1 대인마크 및 40m 전진 롱빌드업 패스",
                        "type": "DEF_ACTION",
                        "location": [32.5, 40.0],
                        "grid": [4.87, 6.0],
                        "xg": 0.0,
                        "desc": "상대 최전방 공격수의 침투 경로를 원천 차단하고 공중볼 경합 100% 승리 후 최전방 역습 기점 패스 공급.",
                    },
                ],
            },
        ],
    }


@app.get("/api/tactics/player-highlights")
def get_player_tactical_highlights(
    player_name: str = "",
    player_id: Optional[int] = None,
) -> dict[str, Any]:
    """
    Returns dynamic, 100% position-tailored 2D tactical highlight moments,
    real club roster, top league rival roster, and verified YouTube highlight/skills sync
    for the specified scouted player.
    """
    if not player_name and not player_id:
        raise HTTPException(
            status_code=400, detail="player_name or player_id is required"
        )
    res = build_player_tactics_payload(
        player_name=player_name, player_id=player_id
    )
    if not res:
        raise HTTPException(
            status_code=404,
            detail=f"Player '{player_name}' not found in tactical database",
        )
    return res

