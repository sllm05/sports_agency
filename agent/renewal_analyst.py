"""
Contract Renewal Analyst Agent (`src/sports_agency/agents/renewal_analyst.py`)

Responsible for Node 2B: Hermes Contract Renewal & Benchmarking Analyst.
Evaluates current club extension leverage, replacement transfer fee amortization
savings under PSR/FFP rules, and peer wage band anchoring for retention talks.
"""

from __future__ import annotations

from typing import Any

from sports_agency.agents.base import BaseAgent, apply_contract_override, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import AgencyGraphState


class RenewalAnalystAgent(BaseAgent):
    """
    Hermes Renewal & Wage Benchmarking Analyst Agent (powered by gemini-3.8-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Contract Renewal Analyst Agent",
            role_description="원소속 구단 재계약 레버리지 및 대체자 이적료 감가상각 절감 효과 분석가",
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

        cur_club = profile["current_club"]
        live_news = invoke_hermes_mcp_tool(
            tool_trace,
            "search_live_club_injury_and_rumors",
            {"club_name": cur_club, "position": pos},
        )

        psr_breakdown = invoke_hermes_mcp_tool(
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
