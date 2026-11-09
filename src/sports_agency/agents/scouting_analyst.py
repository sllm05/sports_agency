"""
Scouting & Transfer Analyst Agent (`src/sports_agency/agents/scouting_analyst.py`)

Responsible for Node 2A: Hermes Transfer & Scouting Analyst.
Fetches comprehensive player metrics, computes peer group wage bands,
matches optimal destination clubs via tactical vector embeddings,
and calculates PSR book cost and net-gross wage simulations.
"""

from __future__ import annotations

from typing import Any

from sports_agency.agents.base import BaseAgent, apply_contract_override, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE
from sports_agency.schemas.agent_schemas import AgencyGraphState


class ScoutingAnalystAgent(BaseAgent):
    """
    Hermes Transfer & Scouting Analyst Agent (powered by gemini-3.8-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Scouting & Transfer Analyst Agent",
            role_description="Hermes 기반 심층 데이터 스카우팅, 이적 타겟 구단 매칭 및 재무/PSR 밸류에이션 분석가",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        tool_trace = list(state.get("hermes_tool_trace", []))
        logs = list(state.get("model_usage_log", []))

        raw_profile = invoke_hermes_mcp_tool(
            tool_trace,
            "get_player_complete_data",
            {"player_name": state["player_name"]},
        )
        profile = apply_contract_override(raw_profile, state.get("contract_override"))
        pos = profile["position"]
        age = profile["age"]
        val = profile["market_value_eur"]
        cur_wage = profile["weekly_wage_eur"]
        target_wage = int(cur_wage * (1 + state["target_wage_increase_pct"] / 100.0))

        peer_band = invoke_hermes_mcp_tool(
            tool_trace,
            "get_peer_group_wage_band",
            {
                "position": pos,
                "age": age,
                "market_value_eur": val,
                "exclude_player_name": profile["name"],
            },
        )

        clubs = invoke_hermes_mcp_tool(
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

        live_news = invoke_hermes_mcp_tool(
            tool_trace,
            "search_live_club_injury_and_rumors",
            {"club_name": target_club_for_news, "position": pos},
        )

        psr_breakdown = invoke_hermes_mcp_tool(
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
