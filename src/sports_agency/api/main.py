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
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from mcp_server.football_mcp_server import get_player_complete_data, list_agency_players
from sports_agency.config import CONFIG, PROJECT_ROOT, ROUTER
from sports_agency.graph.agency_workflow import WORKFLOW_MANAGER
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE

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


# ============================================================================
# Request Schemas
# ============================================================================
class StartWorkflowRequest(BaseModel):
    player_name: str = Field(..., description="선수 이름 (예: 설영우, 손흥민, 이강인)")
    track_mode: str = Field(
        "TRACK_A_TRANSFER",
        description="TRACK_A_TRANSFER (이적 역제의) 또는 TRACK_B_RENEWAL (재계약 협상)",
    )
    target_wage_increase_pct: int = Field(25, ge=0, le=300)
    priority_goal: str = Field("주전 출전 시간 보장 + 적정 주급 확보")
    auto_complete: bool = Field(
        False,
        description="True일 경우 Human-in-the-Loop 일시정지 없이 끝까지 즉시 실행",
    )
    thread_id: str | None = None


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
    top_k: int = Field(4, ge=1, le=10)


class GcpConfigUpdateRequest(BaseModel):
    gcp_project: str = Field(..., description="설정할 GCP Project ID")
    gcp_location: str = Field("global", description="Vertex AI 리전 (Gemini 3.8/Embedding-2는 global 권장)")


# ============================================================================
# Endpoints
# ============================================================================
@app.get("/", response_class=HTMLResponse)
def serve_dashboard() -> HTMLResponse:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Dashboard index.html not found</h1>", status_code=404)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


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
    return {
        "total_count": len(players),
        "korean_roster": korean_players,
        "european_peers": peer_players,
        "all_players": players,
    }


@app.get("/api/players/{player_name}")
def api_get_player(player_name: str) -> dict[str, Any]:
    data = get_player_complete_data(player_name)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data


@app.post("/api/workflow/start")
def api_start_workflow(req: StartWorkflowRequest) -> dict[str, Any]:
    thread_id = req.thread_id or f"deal_{uuid.uuid4().hex[:10]}"
    result = WORKFLOW_MANAGER.start_session(
        thread_id=thread_id,
        player_name=req.player_name,
        track_mode=req.track_mode,
        target_wage_increase_pct=req.target_wage_increase_pct,
        priority_goal=req.priority_goal,
        auto_complete=req.auto_complete,
    )
    return result


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
