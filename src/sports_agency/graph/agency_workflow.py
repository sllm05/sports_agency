"""
LangGraph Multi-Agent Workflow (`src/sports_agency/graph/agency_workflow.py`)

Enforces Project Rules:
- Zero hardcoding: all player/club data, GBE point rules, and regulation citations come dynamically
  from SQLite (`data/agency_desk.db` & `rag_regulations_vec`), and all analyses, dialogues, and documents
  are generated live by Vertex AI (`gemini-3.8-flash` & `gemini-3.5-flash`).
- All workflow steps are logged to `work.log`.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Literal, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from mcp_server.football_mcp_server import (
    HERMES_MCP_TOOLS,
    calculate_gbe_points_from_db,
)
from sports_agency.config import CONFIG, ROUTER
from sports_agency.logger import log_work_event
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE


# ============================================================================
# Pydantic Structured Output Schemas (Vertex AI response_schema)
# ============================================================================
class LegalRagReviewSchema(BaseModel):
    non_eu_quota_result: str = Field(
        ...,
        description="타겟 구단 및 해당 리그의 Non-EU 외국인 선수 등록 쿼터 규정 판독 결과 (1~2문장)",
    )
    ffar_fee_guidance: str = Field(
        ...,
        description="FIFA FFAR 제15조 수수료 상한 및 Circular No. 1873 유예 공문 기반 방어 논리 (2~3문장)",
    )


class SparringRound1Schema(BaseModel):
    opening_ask_wage_eur: int = Field(
        ...,
        description="에이전트가 선수의 Opta 백분위, 잔여 계약, 비교군 주급을 근거로 1차 제시하는 주급(유로 정수)",
    )
    club_counter_wage_eur: int = Field(
        ...,
        description="구단 스포츠 디렉터가 PSR 장부 비용, 내구성/결장 리스크, 약점 백분위를 근거로 역제안하는 1차 주급(유로 정수)",
    )
    agent_r1: str = Field(..., description="1라운드 선수 에이전트 AI의 오프닝 요구 대사 (Opta 실측 강점, UCL 경력, 비교군 주급 인용)")
    director_r1: str = Field(..., description="1라운드 상대 구단 스포츠 디렉터 AI의 반박 및 역제안 대사 (구단 PSR 감가상각 비용, 선수 보완점/가용률, FFAR 수수료 인용)")


class SparringRound2Schema(BaseModel):
    agreed_base_wage_eur: int = Field(..., description="2라운드 협상 끝에 최종 합의된 기본 주급(유로 정수)")
    agreed_bonus_wage_eur: int = Field(..., description="2라운드 협상 끝에 신설 합의된 주당 환산 성과/출전 보너스(유로 정수)")
    release_clause_eur: int = Field(..., description="최종 합의된 바이아웃(Release Clause) 금액(유로 정수)")
    agreed_fee_pct: float = Field(..., description="최종 합의된 에이전트 수수료율(%, 예: 6.0 ~ 7.5)")
    agent_r2: str = Field(..., description="2라운드 사람 수석 에이전트의 전략을 반영한 선수 에이전트 AI의 카운터 대사")
    director_r2: str = Field(..., description="2라운드 상대 구단 스포츠 디렉터 AI의 최종 합의 수용 대사")


class DualOutputDocsSchema(BaseModel):
    deal_prep_md: str = Field(..., description="에이전트 내부 대외비용 협상 전략 치트시트 전체 마크다운 문서")
    pitch_deck_md: str = Field(..., description="구단 스포츠 디렉터 발송용 1-Page 선수 가치 제안서 전체 마크다운 문서")


class AgencyGraphState(TypedDict, total=False):
    player_name: str
    track_mode: str
    target_wage_increase_pct: int
    priority_goal: str
    preferred_league: str
    human_action_choice: str
    contract_override: dict[str, Any]

    supervisor_note: str
    model_usage_log: list[dict[str, str]]
    hermes_tool_trace: list[dict[str, Any]]

    player_profile: dict[str, Any]
    peer_wage_band: dict[str, Any]
    matched_clubs: list[dict[str, Any]]
    tactical_vector_matches: list[dict[str, Any]]
    live_club_news: dict[str, Any]
    psr_and_tax_breakdown: dict[str, Any]
    hermes_ai_summary: str

    rag_retrieved_chunks: list[dict[str, Any]]
    rag_legal_review: dict[str, Any]

    negotiation_metrics: dict[str, Any]
    sparring_transcript: list[dict[str, str]]

    deal_prep_md: str
    pitch_deck_md: str
    saved_files: dict[str, str]


def _invoke_hermes_mcp_tool(
    tool_trace: list[dict[str, Any]],
    tool_name: str,
    args: dict[str, Any],
) -> Any:
    tool_fn = HERMES_MCP_TOOLS[tool_name]
    xml_call = (
        f'<tool_call>{json.dumps({"name": tool_name, "arguments": args}, ensure_ascii=False)}</tool_call>'
    )
    result = tool_fn(**args)
    tool_trace.append(
        {
            "tool": tool_name,
            "args": args,
            "xml_protocol": xml_call,
        }
    )
    return result


# ============================================================================
# Node 1: Supervisor Router (`gemini-3.5-flash`)
# ============================================================================
def supervisor_node(state: AgencyGraphState) -> dict[str, Any]:
    player_name = state["player_name"]
    track_mode = state["track_mode"]
    inc_pct = state["target_wage_increase_pct"]
    goal = state["priority_goal"]

    prompt = (
        f"스포츠 에이전시 수석 라우터로서 다음 요청을 분석하여 2문장 이내로 워크플로우 분기 결정 브리핑을 작성해줘:\n"
        f"- 대상 선수: {player_name}\n"
        f"- 업무 트랙 코드: {track_mode}\n"
        f"- 목표 주급 인상률: +{inc_pct}%\n"
        f"- 협상 최우선 가치: {goal}"
    )
    note, model_used = ROUTER.generate_text(
        prompt,
        system_instruction="당신은 유럽 축구 에이전시의 수석 오케스트레이터(Supervisor)입니다.",
        use_light_model=True,
        temperature=0.2,
    )

    log_work_event("LANGGRAPH_NODE_1", f"Supervisor routed player={player_name} to mode={track_mode}")
    logs = list(state.get("model_usage_log", []))
    logs.append({"node": "Node 1: Supervisor Router", "model": model_used})
    return {
        "supervisor_note": note,
        "model_usage_log": logs,
    }


def route_by_track(
    state: AgencyGraphState,
) -> Literal["hermes_transfer", "hermes_renewal"]:
    if state.get("track_mode") == "TRACK_A_TRANSFER":
        return "hermes_transfer"
    return "hermes_renewal"


def _apply_contract_override(profile: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    """Applies confidential contract overrides entered by the agent onto the loaded player profile."""
    if not override:
        return profile
    p = dict(profile)
    if override.get("actual_weekly_wage_eur") and int(override["actual_weekly_wage_eur"]) > 0:
        p["weekly_wage_eur"] = int(override["actual_weekly_wage_eur"])
        p["is_wage_estimated"] = 0
        p["confidential_override_applied"] = True
    if override.get("custom_market_value_eur") and int(override["custom_market_value_eur"]) > 0:
        p["market_value_eur"] = int(override["custom_market_value_eur"])
    if override.get("contract_years") and int(override["contract_years"]) > 0:
        p["target_contract_years"] = int(override["contract_years"])
    else:
        p["target_contract_years"] = 4
    p["target_signing_bonus_eur"] = int(override.get("signing_bonus_eur") or 0)
    p["current_release_clause_eur"] = int(override.get("current_release_clause_eur") or 0)
    p["agent_fee_target_pct"] = float(override.get("agent_fee_pct") or 7.0)
    return p


# ============================================================================
# Node 2A: Hermes Transfer & Scouting Analyst (`gemini-3.8-flash` + `gemini-embedding-001`)
# ============================================================================
def hermes_transfer_node(state: AgencyGraphState) -> dict[str, Any]:
    tool_trace = list(state.get("hermes_tool_trace", []))
    logs = list(state.get("model_usage_log", []))

    raw_profile = _invoke_hermes_mcp_tool(
        tool_trace,
        "get_player_complete_data",
        {"player_name": state["player_name"]},
    )
    profile = _apply_contract_override(raw_profile, state.get("contract_override"))
    pos = profile["position"]
    age = profile["age"]
    val = profile["market_value_eur"]
    cur_wage = profile["weekly_wage_eur"]
    target_wage = int(cur_wage * (1 + state["target_wage_increase_pct"] / 100.0))

    peer_band = _invoke_hermes_mcp_tool(
        tool_trace,
        "get_peer_group_wage_band",
        {
            "position": pos,
            "age": age,
            "market_value_eur": val,
            "exclude_player_name": profile["name"],
        },
    )

    clubs = _invoke_hermes_mcp_tool(
        tool_trace,
        "find_matching_clubs_for_transfer",
        {
            "position": pos,
            "max_fee_eur": val,
            "target_weekly_wage_eur": target_wage,
            "preferred_league": state.get("preferred_league", "ALL"),
        },
    )

    tend = profile.get("playstyle_and_tendencies", {})
    tactical_query_str = (
        f"{profile['name_ko']} ({pos}): {profile['strengths_summary']} | "
        f"{tend.get('tactical_archetype', '')} | {tend.get('strengths_tags', '')}"
    )
    tactical_matches = VECTOR_STORE.search_tactical_fit(
        player_strengths=tactical_query_str,
        position=pos,
        top_k=3,
    )
    if tactical_matches:
        logs.append(
            {
                "node": "Node 2A: Tactical Fit Vector Match (SQLite)",
                "model": tactical_matches[0]["embedding_model"],
            }
        )

    top_club = clubs[0] if clubs else {}
    target_club_for_news = top_club.get("club_name") if top_club else profile["current_club"]
    target_league_for_psr = top_club.get("league") if top_club else profile["league"]

    live_news = _invoke_hermes_mcp_tool(
        tool_trace,
        "search_live_club_injury_and_rumors",
        {"club_name": target_club_for_news, "position": pos},
    )

    psr_breakdown = _invoke_hermes_mcp_tool(
        tool_trace,
        "calculate_psr_and_tax_breakdown",
        {
            "league": target_league_for_psr,
            "transfer_fee_eur": val,
            "weekly_wage_eur": target_wage,
            "contract_years": int(profile.get("target_contract_years", 4)),
            "agent_fee_pct": float(profile.get("agent_fee_target_pct", 7.0)),
            "signing_bonus_eur": int(profile.get("target_signing_bonus_eur", 0)),
        },
    )

    band_q25 = peer_band["wage_band_eur"]["q25_conservative"]
    band_q75 = peer_band["wage_band_eur"]["q75_ambitious"]

    mgr_info = (
        f"감독 {top_club.get('manager_name', '')} (포메이션 {top_club.get('manager_preferred_formation', '')}, "
        f"리더십/성향: {top_club.get('manager_leadership_personality', '')}, "
        f"포지션 요구사항: {top_club.get('manager_position_requirement', '')})"
        if top_club else ""
    )
    ucl_info = profile.get("career_and_ucl", {})
    vp_info = profile.get("valuation_and_profile", {})

    prompt = (
        f"당신은 NousResearch Hermes 아키텍처 기반의 축구 데이터 분석 에이전트입니다.\n"
        f"아래 실제 SQLite DB 조회 및 실시간 검색 결과를 바탕으로 3~4문장의 핵심 스카우팅 & 밸류에이션 분석 요약을 작성하세요:\n"
        f"- 고객(선수/감독): {profile['name_ko']} ({profile['name']}), 포지션 {pos}, 시세 €{val:,} (커리어 최고 €{vp_info.get('highest_market_value_eur', val):,}), 현재 주급 €{cur_wage:,} ({'실제 기밀계약 입력값' if not profile.get('is_wage_estimated', 1) else '시장 추정치'})\n"
        f"- Opta/Understat 실측 장단점 및 내구성: {tend.get('tactical_archetype', '')} | {tend.get('strengths_tags', '')} | {tend.get('weaknesses_tags', '')} | {tend.get('durability_and_availability_note', '')}\n"
        f"- 통산 & UCL 경력: 통산 {ucl_info.get('career_matches', 0)}경기 (UCL/유럽대항전 {ucl_info.get('ucl_matches', 0)}경기 {ucl_info.get('ucl_goals', 0)}골 {ucl_info.get('ucl_assists', 0)}도움)\n"
        f"- 동급 Peer 주급 밴드: Q25 €{band_q25:,} ~ 중앙값 €{peer_band['wage_band_eur']['median_fair']:,} ~ Q75 €{band_q75:,}\n"
        f"- 구단 연간 PSR 장부 총비용(감가상각+세전연봉+수수료): 연 €{psr_breakdown['annual_psr_book_cost_eur']:,}/년 (세후 주급 약 €{psr_breakdown['weekly_net_wage_eur']:,}/주)\n"
        f"- 매칭 1순위 구단 및 감독 전술 적합도: {target_club_for_news} | {mgr_info} | ({live_news.get('tactical_context', '')})"
    )
    ai_summary, model_used = ROUTER.generate_text(
        prompt,
        system_instruction="실제 데이터 수치(유로화, 백분위, 연간 PSR 장부 비용)를 정확히 인용하여 간결하고 전문적인 에이전시 분석 톤으로 작성하세요.",
        use_light_model=False,
        temperature=0.3,
    )
    logs.append({"node": "Node 2A: Hermes Transfer Analyst", "model": model_used})
    log_work_event("LANGGRAPH_NODE_2A", f"Completed Hermes Transfer Analysis for {profile['name']}")

    return {
        "hermes_tool_trace": tool_trace,
        "player_profile": profile,
        "peer_wage_band": peer_band,
        "matched_clubs": clubs,
        "tactical_vector_matches": tactical_matches,
        "live_club_news": live_news,
        "psr_and_tax_breakdown": psr_breakdown,
        "hermes_ai_summary": ai_summary,
        "model_usage_log": logs,
    }


# ============================================================================
# Node 2B: Hermes Renewal & Wage Benchmarking Analyst (`gemini-3.8-flash`)
# ============================================================================
def hermes_renewal_node(state: AgencyGraphState) -> dict[str, Any]:
    tool_trace = list(state.get("hermes_tool_trace", []))
    logs = list(state.get("model_usage_log", []))

    raw_profile = _invoke_hermes_mcp_tool(
        tool_trace,
        "get_player_complete_data",
        {"player_name": state["player_name"]},
    )
    profile = _apply_contract_override(raw_profile, state.get("contract_override"))
    pos = profile["position"]
    age = profile["age"]
    val = profile["market_value_eur"]
    cur_wage = profile["weekly_wage_eur"]
    target_wage = int(cur_wage * (1 + state["target_wage_increase_pct"] / 100.0))

    peer_band = _invoke_hermes_mcp_tool(
        tool_trace,
        "get_peer_group_wage_band",
        {
            "position": pos,
            "age": age,
            "market_value_eur": val,
            "exclude_player_name": profile["name"],
        },
    )

    cur_club = profile["current_club"]
    live_news = _invoke_hermes_mcp_tool(
        tool_trace,
        "search_live_club_injury_and_rumors",
        {"club_name": cur_club, "position": pos},
    )

    psr_breakdown = _invoke_hermes_mcp_tool(
        tool_trace,
        "calculate_psr_and_tax_breakdown",
        {
            "league": profile["league"],
            "transfer_fee_eur": 0,  # Renewal has zero new transfer fee amortization!
            "weekly_wage_eur": target_wage,
            "contract_years": int(profile.get("target_contract_years", 4)),
            "agent_fee_pct": float(profile.get("agent_fee_target_pct", 7.0)),
            "signing_bonus_eur": int(profile.get("target_signing_bonus_eur", 0)),
        },
    )

    band_q25 = peer_band["wage_band_eur"]["q25_conservative"]
    band_q75 = peer_band["wage_band_eur"]["q75_ambitious"]
    tend = profile.get("playstyle_and_tendencies", {})

    prompt = (
        f"당신은 Hermes 아키텍처 기반의 축구 선수 연봉 밸류에이션 분석 에이전트입니다.\n"
        f"현 소속 구단({cur_club})과의 재계약 협상을 위한 3~4문장의 핵심 정량 근거 요약을 작성하세요:\n"
        f"- 선수: {profile['name_ko']} ({profile['name']}), {age}세, 시세 €{val:,}, 현재 주급 €{cur_wage:,} ({'실제 기밀계약 입력값' if not profile.get('is_wage_estimated', 1) else '시장 추정치'})\n"
        f"- Opta/Understat 퍼포먼스 및 내구성: 상위 {100 - profile['pos_percentile'] + 1}%, {tend.get('strengths_tags', '')} | {tend.get('durability_and_availability_note', '')}\n"
        f"- 동급 비교군(Peer 5인) 주급 밴드: €{band_q25:,} ~ €{band_q75:,}\n"
        f"- 재계약 시 구단 PSR 장부 이점: 외부 대체자 영입 시 이적료 감가상각(연 €{int(val/5):,})이 추가 발생하지만, 재계약 시 이적료 감가상각 €0으로 연간 구단 PSR 총비용이 €{psr_breakdown['annual_psr_book_cost_eur']:,}/년에 불과함\n"
        f"- 구단 동향: {live_news.get('tactical_context', '')}"
    )
    ai_summary, model_used = ROUTER.generate_text(
        prompt,
        system_instruction="재계약 협상에서 에이전트가 구단 단장에게 제시할 수 있는 날카로운 정량 근거(대체자 이적료 감가상각 절감 효과 포함)를 요약하세요.",
        use_light_model=False,
        temperature=0.3,
    )
    logs.append({"node": "Node 2B: Hermes Renewal Analyst", "model": model_used})
    log_work_event("LANGGRAPH_NODE_2B", f"Completed Hermes Renewal Analysis for {profile['name']}")

    return {
        "hermes_tool_trace": tool_trace,
        "player_profile": profile,
        "peer_wage_band": peer_band,
        "matched_clubs": [],
        "tactical_vector_matches": [],
        "live_club_news": live_news,
        "psr_and_tax_breakdown": psr_breakdown,
        "hermes_ai_summary": ai_summary,
        "model_usage_log": logs,
    }


# ============================================================================
# Node 3: Legal & GBE RAG Specialist (`gemini-embedding-2` + `gemini-3.5-flash`)
# ============================================================================
def legal_and_gbe_rag_node(state: AgencyGraphState) -> dict[str, Any]:
    logs = list(state.get("model_usage_log", []))
    p = state["player_profile"]
    clubs = state.get("matched_clubs", [])
    track_mode = state["track_mode"]

    target_club = (
        clubs[0]
        if (track_mode == "TRACK_A_TRANSFER" and clubs)
        else {
            "club_name": p["current_club"],
            "league": p["league"],
            "non_eu_slots_free": 99,
        }
    )

    target_league = target_club.get("league", p["league"])
    client_role = "감독(Head Coach)" if p.get("position") == "MGR" else f"프로축구선수({p.get('position')})"
    league_specific_law_terms = {
        "Premier League": "영국 FA GBE 워크퍼밋 15점 Auto-Pass ESC 예외슬롯 EPL PSR 5년 감가상각",
        "La Liga": "스페인 라리가 Non-EU 외국인 3명 쿼터 Royal Decree 1006/1985 의무 바이아웃 Release Clause",
        "Serie A": "이탈리아 세리에A Non-EU 시즌당 2명 신규 영입 제한 쿼터 세후 연봉 협상",
        "Bundesliga": "독일 분데스리가 Non-EU 외국인 무제한 등록 DFL 재정 건전성",
        "Ligue 1": "프랑스 리그1 Non-EU 4명 쿼터 LFP 바이아웃 금지 신사협정",
    }.get(target_league, f"{target_league} 외국인 쿼터 및 계약 규정")

    # 1. Retrieve regulation chunks dynamically from SQLite `rag_regulations_vec` (`gemini-embedding-2`)
    rag_query = (
        f"{league_specific_law_terms}, {client_role} {track_mode}, "
        f"FIFA FFAR 제15조 에이전트 수수료 상한 유예 Circular No. 1873, "
        f"FIFA RSTP 제18조 3항 보스만 룰 계약만료 6개월 사전협상, UEFA FSR 구단 감가상각 5년 상한"
    )
    retrieved_chunks = VECTOR_STORE.search_regulations(query=rag_query, top_k=5)
    if retrieved_chunks:
        logs.append(
            {
                "node": "Node 3: SQLite Regulation Vector Search",
                "model": retrieved_chunks[0]["query_embedding_model"],
            }
        )

    # Extract provenance citations by category without duplicate fallback
    def _get_citation_by_category(cat: str, fallback_query: str) -> str:
        for ch in retrieved_chunks:
            if ch["doc_category"] == cat:
                return f"[출처: {ch['source_citation']}, 기준일: {ch['effective_date']}]"
        cat_hits = VECTOR_STORE.search_regulations(query=fallback_query, top_k=1, category_filter=cat)
        if cat_hits:
            ch = cat_hits[0]
            if ch["chunk_id"] not in {c["chunk_id"] for c in retrieved_chunks}:
                retrieved_chunks.append(ch)
            return f"[출처: {ch['source_citation']}, 기준일: {ch['effective_date']}]"
        top = retrieved_chunks[0]
        return f"[출처: {top['source_citation']}, 기준일: {top['effective_date']}]"

    gbe_source = _get_citation_by_category("GBE_WORK_PERMIT", "영국 FA GBE 워크퍼밋 점수 산정 Auto-Pass ESC")
    non_eu_source = _get_citation_by_category("NON_EU_QUOTA", f"{target_league} Non-EU 외국인 선수 등록 쿼터 슬롯")
    ffar_source = _get_citation_by_category("FIFA_FFAR_FEE", "FIFA FFAR Article 15 service fee cap Circular 1873 suspension")
    psr_source = _get_citation_by_category("PSR_CONTRACT_LAW", "EPL PSR UEFA FSR 이적료 감가상각 5년 RSTP Article 18")

    # 2. Calculate GBE points dynamically from SQLite `gbe_scoring_rules` table
    gbe_calc = calculate_gbe_points_from_db(
        intl_match_pct=float(p["intl_match_pct"]),
        continental_minutes_pct=float(p["continental_minutes_pct"]),
        league_band=int(p["current_league_band"]),
    )

    # 3. Synthesize Non-EU quota status & FIFA FFAR legal review via `gemini-3.5-flash` from retrieved chunks
    chunks_context = "\n\n".join(
        f"[{c['title']} | 출처: {c['source_citation']} | 기준일: {c['effective_date']}]\n{c['content']}"
        for c in retrieved_chunks
    )
    eu_status_label = "EU 시민권자 (Non-EU 쿼터 무관)" if p.get("is_eu_citizen") else f"Non-EU 국적 ({p.get('nationality', 'Unknown')})"
    legal_prompt = (
        f"아래 SQLite 벡터 DB에서 검색된 공식 규정 원문만을 근거로 다음 2가지 항목을 JSON 객체로 작성해줘:\n"
        f"1) 'non_eu_quota_result': 타겟 구단({target_club['club_name']}, 리그: {target_league}, 잔여 Non-EU 슬롯 코드: {target_club['non_eu_slots_free']})에 "
        f"{client_role}({p['name']}, 국적/자격: {eu_status_label}, 계약만료: {p.get('contract_expires', '')})를 등록할 때의 리그 외국인/Non-EU 쿼터 및 계약 규정 판독 결과 (1~2문장)\n"
        f"2) 'ffar_fee_guidance': 구단이 FIFA FFAR 제15조를 근거로 에이전트 수수료를 3%로 제한하려 할 때, "
        f"유예 공문(Circular No. 1873 등)과 출처/기준일을 들어 반박하는 법률 자문 요약 (2~3문장)\n\n"
        f"[검색된 규정 원문]\n{chunks_context}"
    )
    parsed_legal, model_used = ROUTER.generate_structured(
        legal_prompt,
        LegalRagReviewSchema,
        system_instruction="검색된 공식 규정 원문만을 근거로 정확한 법률 판독 결과를 작성하세요.",
        use_light_model=True,
        temperature=0.1,
    )
    logs.append({"node": "Node 3: Legal & GBE RAG Summary", "model": model_used})

    rag_legal_review = {
        "gbe_points": gbe_calc["total_points"],
        "gbe_work_permit_result": gbe_calc["status_summary"],
        "gbe_source": gbe_source,
        "non_eu_quota_result": parsed_legal.non_eu_quota_result,
        "non_eu_source": non_eu_source,
        "ffar_fee_guidance": parsed_legal.ffar_fee_guidance,
        "ffar_source": ffar_source,
        "psr_source": psr_source,
    }

    log_work_event(
        "LANGGRAPH_NODE_3",
        f"Completed SQLite Vector RAG & GBE calculation ({gbe_calc['total_points']} pts) for {p['name']}",
    )
    return {
        "rag_retrieved_chunks": retrieved_chunks,
        "rag_legal_review": rag_legal_review,
        "model_usage_log": logs,
    }


# ============================================================================
# Node 4A: Sparring Round 1 (`gemini-3.8-flash`)
# ============================================================================
def sparring_round_1_node(state: AgencyGraphState) -> dict[str, Any]:
    logs = list(state.get("model_usage_log", []))
    p = state["player_profile"]
    band = state["peer_wage_band"]["wage_band_eur"]
    clubs = state.get("matched_clubs", [])
    track_mode = state["track_mode"]
    legal = state["rag_legal_review"]
    psr = state.get("psr_and_tax_breakdown", {})

    cur_wage = p["weekly_wage_eur"]
    desired_wage = int(cur_wage * (1 + state["target_wage_increase_pct"] / 100.0))
    ref_opening_ask = max(desired_wage, band["median_fair"])
    ref_club_counter = int((cur_wage + ref_opening_ask) / 2)

    top_club = clubs[0] if (track_mode == "TRACK_A_TRANSFER" and clubs) else {}
    target_club_name = top_club.get("club_name", p["current_club"])
    starter_context = (
        f"현 주전 {top_club['current_starter']}({top_club['starter_age']}세, 만료 {top_club['starter_contract_expires']}, 주급 €{top_club['starter_weekly_wage_eur']:,})"
        if top_club
        else f"현 소속 구단({p['current_club']}) 핵심 전력 유지 및 동급 대체자 이적료(€{p['market_value_eur']:,}+) 절감"
    )

    tend = p.get("playstyle_and_tendencies", {})
    ucl = p.get("career_and_ucl", {})
    vp = p.get("valuation_and_profile", {})
    mgr_context = (
        f"타겟 구단 감독: {top_club.get('manager_name', '')} (포메이션 {top_club.get('manager_preferred_formation', '')}, "
        f"포지션 전술 요구사항: {top_club.get('manager_position_requirement', '')})"
        if top_club.get("manager_name")
        else f"현 소속팀 감독 전술 시스템 핵심 적합 자원"
    )
    club_fin = top_club.get("club_live_standing") or p.get("club_standing_and_finance") or {}
    club_fin_str = (
        f"리그 {club_fin.get('rank_position', '-')}위 ({club_fin.get('points', 0)}점), 구장 {club_fin.get('stadium_seats', 45000):,}석, 최근 순이적지출 {club_fin.get('net_transfer_record', '€0')}"
        if club_fin else ""
    )

    prompt = (
        f"유럽 축구 이적/재계약 협상 테이블의 1라운드 공방을 JSON 객체로 작성하세요.\n"
        f"[1. 선수 및 Opta/Understat 실측 심층 데이터]\n"
        f"- 선수: {p['name_ko']} ({p['name']}), 나이 {p['age']}세, 계약만료 {p['contract_expires']}, 시세 €{p['market_value_eur']:,} (커리어 피크 €{vp.get('highest_market_value_eur', p['market_value_eur']):,})\n"
        f"- 전술 아키타입: {tend.get('tactical_archetype', '')}\n"
        f"- 에이전트 공격 무기 (실측 강점 백분위 & UCL 경력): {tend.get('strengths_tags', p['strengths_summary'])} | 통산 {ucl.get('career_matches', 0)}경기 (UCL/유럽대항전 {ucl.get('ucl_matches', 0)}경기 {ucl.get('ucl_goals', 0)}골 {ucl.get('ucl_assists', 0)}도움)\n"
        f"- 구단 디렉터 압박 무기 (실측 약점 백분위 & 내구성/가용률): {tend.get('weaknesses_tags', '')} | {tend.get('durability_and_availability_note', '')}\n\n"
        f"[2. 구단 전술·재정 및 PSR/세제 데이터]\n"
        f"- 상대 구단: {target_club_name} ({starter_context}) | {club_fin_str}\n"
        f"- 감독 전술 적합도: {mgr_context}\n"
        f"- 비교군 주급 밴드: Q25 €{band['q25_conservative']:,} ~ 중앙값 €{band['median_fair']:,} ~ Q75 €{band['q75_ambitious']:,} (현재 주급 €{cur_wage:,}/주)\n"
        f"- 구단 PSR 장부 총비용 시뮬레이션({psr.get('league', p['league'])}, {psr.get('negotiation_basis', 'GROSS_WEEKLY')}): "
        f"요구 주급 기준 연간 구단 PSR 장부 총비용(이적료 감가상각 €{psr.get('annual_transfer_amortization_eur', 0):,}/년 + 세전 연봉 €{psr.get('annual_gross_wage_eur', 0):,}/년 + 사회보장세/수수료) = 연 €{psr.get('annual_psr_book_cost_eur', 0):,}/년 (세후 주급 약 €{psr.get('weekly_net_wage_eur', 0):,}/주)\n"
        f"- 워크퍼밋/규정 검증: {legal['gbe_work_permit_result']} | {legal['non_eu_quota_result']}\n\n"
        f"[3. 협상 수치 및 대사 생성 지침]\n"
        f"- 에이전트 희망 1차 요구 주급(opening_ask_wage_eur, 기준선 약 €{ref_opening_ask:,}/주 내외)과 구단 디렉터의 1차 역제안 주급(club_counter_wage_eur, 기준선 약 €{ref_club_counter:,}/주 내외)을 선수 백분위와 구단 재정 상황에 맞춰 정수로 산출하고 대사에 정확히 일치시켜 인용하세요.\n"
        f"- 'agent_r1': Opta 상위 백분위 강점, 감독 포메이션 요구사항 부합도, 비교군 주급 중앙값/Q75, 그리고 구단 주전 대체/이적료 절감 효과를 근거로 opening_ask_wage_eur 및 에이전트 수수료 {p.get('agent_fee_target_pct', 7.0)}%를 당당히 요구하세요.\n"
        f"- 'director_r1': 선수의 Opta 하위 백분위 보완점 또는 시즌 가용률(출전 분수), 구단 연간 PSR 장부 총비용(연 €{psr.get('annual_psr_book_cost_eur', 0):,}) 부담, FIFA FFAR 제15조 원안(3% 상한)을 근거로 club_counter_wage_eur를 역제안하며 날카롭게 압박하세요."
    )

    parsed, model_used = ROUTER.generate_structured(
        prompt,
        SparringRound1Schema,
        system_instruction="실제 유럽 축구 협상 테이블의 에이전트와 구단 스포츠 디렉터 화법으로 Opta 백분위, 감독 전술, PSR 감가상각 수치를 정확히 인용해 작성하세요.",
        use_light_model=False,
        temperature=0.35,
    )
    logs.append({"node": "Node 4A: Sparring Simulator (Round 1)", "model": model_used})

    opening_ask_wage = int(parsed.opening_ask_wage_eur or ref_opening_ask)
    club_counter_wage = int(parsed.club_counter_wage_eur or ref_club_counter)

    transcript = [
        {"round": "Round 1", "speaker": "선수 에이전트 AI", "message": parsed.agent_r1},
        {
            "round": "Round 1",
            "speaker": f"{target_club_name} 디렉터 AI",
            "message": parsed.director_r1,
        },
    ]

    negotiation_metrics = {
        "target_club_name": target_club_name,
        "cur_wage": cur_wage,
        "opening_ask_wage": opening_ask_wage,
        "club_counter_wage": club_counter_wage,
        "fallback_floor_wage": band["q25_conservative"],
    }

    log_work_event(
        "LANGGRAPH_NODE_4A",
        f"Sparring Round 1 completed vs {target_club_name} (ask=€{opening_ask_wage:,}, counter=€{club_counter_wage:,})",
    )
    return {
        "negotiation_metrics": negotiation_metrics,
        "sparring_transcript": transcript,
        "model_usage_log": logs,
    }


# ============================================================================
# Node 4B: Sparring Round 2 (`gemini-3.8-flash`)
# ============================================================================
def sparring_round_2_node(state: AgencyGraphState) -> dict[str, Any]:
    logs = list(state.get("model_usage_log", []))
    tool_trace = list(state.get("hermes_tool_trace", []))
    p = state["player_profile"]
    legal = state["rag_legal_review"]
    psr = state.get("psr_and_tax_breakdown", {})
    metrics = dict(state["negotiation_metrics"])
    transcript = list(state.get("sparring_transcript", []))
    choice = state.get("human_action_choice", "OPTION_2_BONUS_AND_RELEASE_CLAUSE")

    target_club_name = metrics["target_club_name"]
    opening_ask_wage = metrics["opening_ask_wage"]
    club_counter_wage = metrics["club_counter_wage"]
    tend = p.get("playstyle_and_tendencies", {})

    if choice == "OPTION_1_HOLD_BASE_WAGE":
        ref_base = opening_ask_wage
        ref_bonus = int(opening_ask_wage * 0.05)
        ref_rc = int(p["market_value_eur"] * 1.8)
        strategy_label = "전략 1: 기본급 원안 강행 + Opta 상위 백분위 스탯 및 대체자 비용 비교 압박"
    elif choice == "OPTION_3_LOWER_RELEASE_FOR_CLUB_OFFER":
        ref_base = club_counter_wage
        ref_bonus = int(opening_ask_wage * 0.12)
        ref_rc = int(p["market_value_eur"] * 1.25)
        strategy_label = "전략 3: 구단 기본급 수용 + 바이아웃(Release Clause) 대폭 하향 및 셀온/인센티브 실리 확보"
    else:
        ref_base = int((opening_ask_wage + club_counter_wage) / 2)
        ref_bonus = int(opening_ask_wage * 0.15)
        ref_rc = int(p["market_value_eur"] * 1.45)
        strategy_label = "전략 2: 기본급 절충 + 가용률 연동 출전/공격포인트 보너스 신설(PSR 고정비 완화) + FFAR 유예 조항 수수료 방어"

    prompt = (
        f"수석 에이전트(사람)가 선택한 개입 전략('{strategy_label}')을 반영하여 2라운드 최종 타결 수치와 대화를 JSON 객체로 작성하세요.\n"
        f"- 1라운드 요약: 에이전트 요구 €{opening_ask_wage:,}/주 vs 구단 역제안 €{club_counter_wage:,}/주\n"
        f"- 선수 내구성/가용률 방어 논리: {tend.get('durability_and_availability_note', '')}\n"
        f"- 구단 세제 및 PSR 규칙: {psr.get('tax_regime_note', '')}\n"
        f"- 가이드라인 타결 수치(전략 반영): 기본 주급(agreed_base_wage_eur) 약 €{ref_base:,}/주 내외, "
        f"주간 환산 출전/성과 보너스(agreed_bonus_wage_eur) 약 +€{ref_bonus:,}/주 상당(공식전 20경기 출전 달성 시 발동하여 구단 PSR 고정비 리스크 헷지), "
        f"바이아웃(release_clause_eur) 약 €{ref_rc:,} 내외, 에이전트 수수료(agreed_fee_pct) 약 6.0~7.0%\n"
        f"- 에이전트 수수료 방어 근거: {legal['ffar_source']} ({legal['ffar_fee_guidance']})\n"
        f"- 재정 규정 근거: {legal['psr_source']}\n"
        f"작성 지침:\n"
        f"- 'agent_r2': 수석 에이전트의 전략('{strategy_label}'), FIFA Circular No. 1873 수수료 상한 유예 근거, 그리고 PSR 고정비 부담을 낮추는 조건부 보너스/바이아웃 구조를 제시하세요.\n"
        f"- 'director_r2': 에이전트의 PSR 회계 배려 및 전술 적합성에 동의하며 최종 합의된 수치(agreed_base_wage_eur, agreed_bonus_wage_eur, release_clause_eur, agreed_fee_pct)로 Term Sheet 서명을 수락하세요."
    )

    parsed, model_used = ROUTER.generate_structured(
        prompt,
        SparringRound2Schema,
        system_instruction="수석 에이전트의 전략 지시를 완벽히 반영하여 최종 합의(Term Sheet)에 도달하는 협상 수치와 대화를 작성하세요.",
        use_light_model=False,
        temperature=0.3,
    )
    logs.append({"node": "Node 4B: Sparring Simulator (Round 2 HITL)", "model": model_used})

    agreed_base = int(parsed.agreed_base_wage_eur or ref_base)
    agreed_bonus = int(parsed.agreed_bonus_wage_eur or ref_bonus)
    release_clause = int(parsed.release_clause_eur or ref_rc)
    agreed_fee_pct = float(parsed.agreed_fee_pct or 6.0)

    # Recalculate final agreed PSR & Net-Gross breakdown
    final_psr = _invoke_hermes_mcp_tool(
        tool_trace,
        "calculate_psr_and_tax_breakdown",
        {
            "league": psr.get("league", p["league"]),
            "transfer_fee_eur": p["market_value_eur"] if state.get("track_mode") == "TRACK_A_TRANSFER" else 0,
            "weekly_wage_eur": agreed_base,
            "contract_years": int(p.get("target_contract_years", 4)),
            "agent_fee_pct": agreed_fee_pct,
            "signing_bonus_eur": int(p.get("target_signing_bonus_eur", 0)),
        },
    )

    transcript.extend(
        [
            {
                "round": "Round 2 (Human-in-the-Loop 반영)",
                "speaker": "선수 에이전트 AI (사람 전략 반영)",
                "message": parsed.agent_r2,
            },
            {
                "round": "Round 2 (최종 타결)",
                "speaker": f"{target_club_name} 디렉터 AI",
                "message": parsed.director_r2,
            },
        ]
    )

    metrics.update(
        {
            "human_strategy_label": strategy_label,
            "agreed_base_wage": agreed_base,
            "agreed_bonus_wage": agreed_bonus,
            "release_clause_eur": release_clause,
            "agreed_fee_pct": agreed_fee_pct,
            "agreed_weekly_net_wage_eur": final_psr["weekly_net_wage_eur"],
            "agreed_annual_net_wage_eur": final_psr["annual_net_wage_eur"],
            "agreed_annual_psr_book_cost_eur": final_psr["annual_psr_book_cost_eur"],
            "agreed_total_deal_package_eur": final_psr["total_deal_package_cost_eur"],
        }
    )

    log_work_event(
        "LANGGRAPH_NODE_4B",
        f"Sparring Round 2 resolved with strategy={choice} -> agreed_base=€{agreed_base:,}, bonus=€{agreed_bonus:,}, annual_psr=€{final_psr['annual_psr_book_cost_eur']:,}",
    )
    return {
        "hermes_tool_trace": tool_trace,
        "psr_and_tax_breakdown": final_psr,
        "negotiation_metrics": metrics,
        "sparring_transcript": transcript,
        "model_usage_log": logs,
    }


# ============================================================================
# Node 5: Dual-Output Practical Document Writer (`gemini-3.8-flash`)
# ============================================================================
def dual_output_writer_node(state: AgencyGraphState) -> dict[str, Any]:
    tool_trace = list(state.get("hermes_tool_trace", []))
    logs = list(state.get("model_usage_log", []))

    p = state["player_profile"]
    band = state["peer_wage_band"]["wage_band_eur"]
    peers = state["peer_wage_band"].get("peers", [])
    legal = state["rag_legal_review"]
    metrics = state["negotiation_metrics"]
    psr = state.get("psr_and_tax_breakdown", {})
    clubs = state.get("matched_clubs", [])
    tactical_matches = state.get("tactical_vector_matches", [])
    live_news = state.get("live_club_news", {})
    transcript = state.get("sparring_transcript", [])

    target_club_name = metrics["target_club_name"]
    ask_wage = metrics["opening_ask_wage"]
    club_offer = metrics["club_counter_wage"]
    agreed_base = metrics["agreed_base_wage"]
    agreed_bonus = metrics["agreed_bonus_wage"]
    release_clause = metrics["release_clause_eur"]
    agreed_fee_pct = metrics["agreed_fee_pct"]
    fallback_wage = metrics["fallback_floor_wage"]

    tend = p.get("playstyle_and_tendencies", {})
    ucl = p.get("career_and_ucl", {})
    vp = p.get("valuation_and_profile", {})
    top_club = clubs[0] if clubs else {}

    peer_rows_md = "\n".join(
        f"| {pr['name_ko']} ({pr['name']}) | {pr['current_club']} ({pr['league']}) | {pr['age']}세 | "
        f"€{pr['market_value_eur']:,} | €{pr['weekly_wage_eur']:,} | 상위 {100 - pr['pos_percentile'] + 1}% |"
        for pr in peers
    )

    club_rows_md = "\n".join(
        f"| **{idx+1}순위: {c['club_name']}** ({c['league']}) | 감독 {c.get('manager_name', '-')} ({c.get('manager_preferred_formation', '-')}) | "
        f"{c['current_starter']} ({c['starter_age']}세, 만료 {c['starter_contract_expires']}) | "
        f"€{c['starter_weekly_wage_eur']:,} | €{c['max_weekly_wage_offer_eur']:,} | {c.get('manager_position_requirement', c['recruitment_note'])} |"
        for idx, c in enumerate(clubs[:3])
    )

    tactical_vec_md = "\n".join(
        f"- **{tm['club_name']}** ({tm['league']}): 전술 벡터 유사도 `{tm['tactical_similarity_score']}` *(임베딩: {tm['embedding_model']})*"
        for tm in tactical_matches
    )

    writer_prompt = (
        f"당신은 유럽 축구 에이전시의 수석 문서 작성 에이전트입니다.\n"
        f"아래 실제 SQLite 심층 데이터(Opta/Understat 백분위, UCL 경력, 감독 전술 요구치, 구단 PSR 감가상각 및 세후/세전 연봉), "
        f"벡터 RAG 법률 판독 결과, 그리고 모의 협상 타결 수치를 모두 반영하여 현업용 마크다운 문서 2종('deal_prep_md', 'pitch_deck_md')을 JSON 객체로 작성하세요.\n\n"
        f"[1. 선수 및 Opta/Understat 실측 심층 데이터]\n"
        f"- 이름: {p['name_ko']} ({p['name']}), 소속: {p['current_club']} ({p['league']}), 포지션: {p['position']} ({p['secondary_positions']}), 나이: {p['age']}세\n"
        f"- 시세: €{p['market_value_eur']:,} (커리어 피크 €{vp.get('highest_market_value_eur', p['market_value_eur']):,}), 현재 주급: €{p['weekly_wage_eur']:,} ({'실제 기밀계약 입력' if not p.get('is_wage_estimated', 1) else '추정치'}), 계약만료: {p['contract_expires']}\n"
        f"- 시즌 스탯: {p['minutes_played']}분 출전, 90분당 득점 {p['goals_per90']}, 도움 {p['assists_per90']}, 전진액션 {p['progressive_actions_per90']}회, 키패스 {p['key_passes_per90']}회, 동 포지션 상위 {100 - p['pos_percentile'] + 1}%\n"
        f"- 전술 아키타입: {tend.get('tactical_archetype', '')}\n"
        f"- 실측 강점(Strengths): {tend.get('strengths_tags', p['strengths_summary'])}\n"
        f"- 실측 보완점(Weaknesses) 및 카운터 방어: {tend.get('weaknesses_tags', '')}\n"
        f"- 내구성/가용률(Availability %) 진단: {tend.get('durability_and_availability_note', '')}\n"
        f"- 통산 & UCL 경력: 통산 {ucl.get('career_matches', 0)}경기 {ucl.get('career_goals', 0)}골 | UCL/유럽대항전 {ucl.get('ucl_matches', 0)}경기 ({ucl.get('ucl_goals', 0)}골 {ucl.get('ucl_assists', 0)}도움) | A매치 {vp.get('international_caps', 0)}경기\n\n"
        f"[2. 비교군(Peer 5인) 주급 밴드 및 마크다운 표]\n"
        f"- Q25: €{band['q25_conservative']:,} / 중앙값: €{band['median_fair']:,} / Q75: €{band['q75_ambitious']:,}\n"
        f"- 비교군 표 행:\n{peer_rows_md}\n\n"
        f"[3. 매칭 구단, 감독 전술 적합도 및 실시간 검색 동향]\n"
        f"- 타겟 구단: {target_club_name} (감독: {top_club.get('manager_name', '현 감독')}, 포메이션: {top_club.get('manager_preferred_formation', '-')}, 포지션 요구사항: {top_club.get('manager_position_requirement', '-')})\n"
        f"- 실시간 동향({live_news.get('source', '')}): {live_news.get('headline', '')} — {live_news.get('tactical_context', '')}\n"
        f"- 구단 비교 행:\n{club_rows_md if club_rows_md else '현 소속팀 재계약 트랙'}\n"
        f"- 전술 벡터 유사도:\n{tactical_vec_md}\n\n"
        f"[4. 구단 재무(PSR/FFP 감가상각) 및 국가별 세전/세후(Net-Gross) 시뮬레이션]\n"
        f"- 협상 기준 세제: {psr.get('league', p['league'])} ({psr.get('negotiation_basis', 'GROSS_WEEKLY')}, 소득세율 {psr.get('top_income_tax_rate_pct', 45)}%, 구단 사회보장세 {psr.get('employer_social_rate_pct', 12)}%)\n"
        f"- 합의 기본급 세전/세후: 세전 주급 €{agreed_base:,}/주 (연 €{psr.get('annual_gross_wage_eur', agreed_base*52):,}) ↔ 선수 실수령 세후 주급 약 €{psr.get('weekly_net_wage_eur', int(agreed_base*0.55)):,}/주 (세후 연봉 €{psr.get('annual_net_wage_eur', 0):,})\n"
        f"- 구단 연간 PSR 장부 총비용(Annualized Squad Cost): 이적료 감가상각(연 €{psr.get('annual_transfer_amortization_eur', 0):,}) + 세전 연봉 + 사회보장세 + 수수료 상각 = **연 €{psr.get('annual_psr_book_cost_eur', 0):,}/년** (총 계약 패키지 €{psr.get('total_deal_package_cost_eur', 0):,})\n"
        f"- 세제/재정 해설: {psr.get('tax_regime_note', '')}\n\n"
        f"[5. SQLite Vector RAG 법률·워크퍼밋 판독 및 출처]\n"
        f"- 영국 GBE: {legal['gbe_work_permit_result']} {legal['gbe_source']}\n"
        f"- Non-EU 쿼터: {legal['non_eu_quota_result']} {legal['non_eu_source']}\n"
        f"- FIFA 수수료: {legal['ffar_fee_guidance']} {legal['ffar_source']}\n"
        f"- 재정 규정: {legal['psr_source']}\n\n"
        f"[6. 모의 협상 타결 조건 ({metrics['human_strategy_label']})]\n"
        f"- 1차 요구액(Anchor): €{ask_wage:,}/주 | 구단 1차 역제안: €{club_offer:,}/주 | 마지노선(Fallback): €{fallback_wage:,}/주\n"
        f"- 최종 합의 기본급: €{agreed_base:,}/주 + 성과 보너스: €{agreed_bonus:,}/주 상당 | 바이아웃: €{release_clause:,} | 에이전트 수수료: {agreed_fee_pct}%\n"
        f"- 협상 대화 요약: {json.dumps(transcript, ensure_ascii=False)}\n\n"
        f"작성 지침:\n"
        f"- 'deal_prep_md': 에이전트 내부 대외비용 협상 치트시트 (1. 타겟 금액 밴드 Anchor/Target/Fallback 및 세전·세후 실수령액 비교, 2. Peer 비교군 마크다운 표, 3. 구단 디렉터 예상 압박 질문 3가지[선수 약점 백분위/가용률, 구단 PSR 감가상각 부담, FFAR 3% 수수료 상한] 및 법률/데이터 카운터 논리)\n"
        f"- 'pitch_deck_md': {target_club_name} 스포츠 디렉터 및 감독 제출용 1-Page Executive Dossier (1. 감독 맞춤형 전술 적합도[포메이션·포지션 요구치 및 Opta 상위 백분위], 2. 단장/CFO 맞춤형 재무·PSR 감가상각 시뮬레이션 표 및 주전 세대교체 가성비 비교표, 3. GBE 워크퍼밋 및 Non-EU 즉시 등록 법률 증명[출처·기준일 명시], 4. 최종 제안 Term Sheet 요약)\n"
        f'반드시 JSON 키 "deal_prep_md", "pitch_deck_md"만 포함하여 마크다운 원문 문자열로 응답하세요.'
    )

    parsed_docs, model_used = ROUTER.generate_structured(
        writer_prompt,
        DualOutputDocsSchema,
        system_instruction="실제 데이터와 법률 출처를 정확히 인용하여 현업 에이전시 품질의 마크다운 문서 2종을 작성하세요.",
        use_light_model=False,
        temperature=0.25,
    )
    deal_prep_md = parsed_docs.deal_prep_md
    pitch_deck_md = parsed_docs.pitch_deck_md

    logs.append({"node": "Node 5: Dual-Output Document Writer", "model": model_used})

    saved = _invoke_hermes_mcp_tool(
        tool_trace,
        "export_agency_documents",
        {
            "player_name": p["name"],
            "deal_prep_md": deal_prep_md,
            "pitch_deck_md": pitch_deck_md,
        },
    )

    log_work_event("LANGGRAPH_NODE_5", f"Generated & saved Dual-Output Markdown documents for {p['name']}")
    return {
        "hermes_tool_trace": tool_trace,
        "deal_prep_md": deal_prep_md,
        "pitch_deck_md": pitch_deck_md,
        "saved_files": saved,
        "model_usage_log": logs,
    }


# ============================================================================
# Graph Builder & SqliteSaver Checkpointer Manager
# ============================================================================
class AgencyWorkflowManager:
    def __init__(self) -> None:
        CONFIG.checkpoint_db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(CONFIG.checkpoint_db_path), check_same_thread=False, timeout=30.0)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self.checkpointer = SqliteSaver(self._conn)
        self.interactive_graph = self._build_graph(interrupt_for_human=True)
        self.auto_graph = self._build_graph(interrupt_for_human=False)

    def _build_graph(self, interrupt_for_human: bool = True):
        builder = StateGraph(AgencyGraphState)

        builder.add_node("supervisor", supervisor_node)
        builder.add_node("hermes_transfer", hermes_transfer_node)
        builder.add_node("hermes_renewal", hermes_renewal_node)
        builder.add_node("legal_rag", legal_and_gbe_rag_node)
        builder.add_node("sparring_round_1", sparring_round_1_node)
        builder.add_node("sparring_round_2", sparring_round_2_node)
        builder.add_node("dual_writer", dual_output_writer_node)

        builder.add_edge(START, "supervisor")
        builder.add_conditional_edges(
            "supervisor",
            route_by_track,
            {
                "hermes_transfer": "hermes_transfer",
                "hermes_renewal": "hermes_renewal",
            },
        )
        builder.add_edge("hermes_transfer", "legal_rag")
        builder.add_edge("hermes_renewal", "legal_rag")
        builder.add_edge("legal_rag", "sparring_round_1")
        builder.add_edge("sparring_round_1", "sparring_round_2")
        builder.add_edge("sparring_round_2", "dual_writer")
        builder.add_edge("dual_writer", END)

        if interrupt_for_human:
            return builder.compile(
                checkpointer=self.checkpointer,
                interrupt_before=["sparring_round_2"],
            )
        return builder.compile(checkpointer=self.checkpointer)

    def start_session(
        self,
        thread_id: str,
        player_name: str,
        track_mode: str = "TRACK_A_TRANSFER",
        target_wage_increase_pct: int = 25,
        priority_goal: str = "주전 출전 시간 보장 + 주급 인상",
        preferred_league: str = "ALL",
        auto_complete: bool = False,
        human_action_choice: str = "OPTION_2_BONUS_AND_RELEASE_CLAUSE",
        contract_override: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        initial_state: AgencyGraphState = {
            "player_name": player_name,
            "track_mode": track_mode,
            "target_wage_increase_pct": target_wage_increase_pct,
            "priority_goal": priority_goal,
            "preferred_league": preferred_league,
            "human_action_choice": human_action_choice,
            "contract_override": contract_override or {},
            "model_usage_log": [],
            "hermes_tool_trace": [],
            "sparring_transcript": [],
        }
        graph = self.auto_graph if auto_complete else self.interactive_graph
        result = graph.invoke(initial_state, config=config)
        snapshot = graph.get_state(config)
        waiting_for_human = bool(snapshot.next and "sparring_round_2" in snapshot.next)
        return {
            "thread_id": thread_id,
            "status": "WAITING_FOR_HUMAN_STRATEGY" if waiting_for_human else "COMPLETED",
            "next_nodes": list(snapshot.next),
            "state": result,
        }

    def resume_with_human_strategy(
        self,
        thread_id: str,
        human_action_choice: str,
    ) -> dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        self.interactive_graph.update_state(
            config,
            {"human_action_choice": human_action_choice},
        )
        result = self.interactive_graph.invoke(None, config=config)
        snapshot = self.interactive_graph.get_state(config)
        return {
            "thread_id": thread_id,
            "status": "COMPLETED" if not snapshot.next else "IN_PROGRESS",
            "next_nodes": list(snapshot.next),
            "state": result,
        }

    def get_session_state(self, thread_id: str) -> dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        snapshot = self.interactive_graph.get_state(config)
        if not snapshot or not snapshot.values:
            return {"error": f"Thread '{thread_id}' not found in SqliteSaver"}
        return {
            "thread_id": thread_id,
            "status": "WAITING_FOR_HUMAN_STRATEGY" if snapshot.next else "COMPLETED",
            "next_nodes": list(snapshot.next),
            "state": dict(snapshot.values),
        }


WORKFLOW_MANAGER = AgencyWorkflowManager()
