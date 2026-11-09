"""
Career Strategist Agent (`src/sports_agency/agents/career_strategist.py`)

Responsible for Node 2C: Career Timing & Strategy Agent.
Evaluates contract expiration cycle leverage, formulates 3-year growth pathways,
and dictates starter playing time guarantee clauses (e.g. 60%+ starter requirement).
"""

from __future__ import annotations

from typing import Any

from sports_agency.agents.base import BaseAgent, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import AgencyGraphState


class CareerStrategistAgent(BaseAgent):
    """
    Career Timing & Strategy Agent (powered by gemini-3.5-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Career Strategist Agent",
            role_description="커리어 수명주기, 계약 만료 주기 레버리지 및 3개년 성장 로드맵 설계 전략가",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        tool_trace = list(state.get("hermes_tool_trace", []))
        logs = list(state.get("model_usage_log", []))
        p = state["player_profile"]

        career_res = invoke_hermes_mcp_tool(
            tool_trace,
            "analyze_career_timing_and_path",
            {
                "player_name": p["name"],
                "target_league_preference": state.get("preferred_league", "ALL"),
                "min_starter_guarantee_pct": 60.0,
            },
        )

        prompt = (
            f"당신은 유럽 축구 에이전시의 커리어 전략 총괄 에이전트(Career Agent)입니다.\n"
            f"선수: {p['name_ko']} ({p['name']}, {p['age']}세, 포지션 {p['position']}, 계약만료 {p['contract_expires']})\n"
            f"판정된 커리어 경로: {career_res['path_label']} (결정 코드: {career_res['timing_decision']})\n"
            f"계약 레버리지: {career_res['contract_leverage']}\n"
            f"3개년 로드맵 개요: Year 1 {career_res['three_year_roadmap'][0]['phase']} -> "
            f"Year 2 {career_res['three_year_roadmap'][1]['phase']} -> "
            f"Year 3 {career_res['three_year_roadmap'][2]['phase']}\n\n"
            f"선수 및 에이전시 실무진을 위한 2~3문장의 핵심 커리어 전략 브리핑을 작성하세요."
        )
        briefing, model_used = ROUTER.generate_text(
            prompt,
            system_instruction="선수의 장기적 시장 가치 극대화, 출전시간 보장, 바이아웃 리밸런싱을 핵심 가치로 브리핑을 작성하세요.",
            use_light_model=True,
            temperature=0.25,
        )
        career_res["career_agent_briefing"] = briefing

        logs.append({"node": "Node 2C: Career Agent (Timing & Pathway)", "model": model_used})
        log_work_event("LANGGRAPH_NODE_2C", f"Career Strategy resolved for {p['name']}: {career_res['path_label']}")

        return {
            "hermes_tool_trace": tool_trace,
            "career_strategy": career_res,
            "model_usage_log": logs,
        }
