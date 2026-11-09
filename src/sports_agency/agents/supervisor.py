"""
Supervisor Router Agent (`src/sports_agency/agents/supervisor.py`)

Responsible for Node 1: Analyzes incoming client dossier, objectives, and parameters,
briefs the executive desk, and routes workflow dynamically into Track A (Transfer)
or Track B (Renewal).
"""

from __future__ import annotations

from typing import Any, Literal

from sports_agency.agents.base import BaseAgent
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import AgencyGraphState


class SupervisorAgent(BaseAgent):
    """
    Supervisor Router Agent (powered by Vertex AI light model, e.g. gemini-3.5-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Supervisor Router Agent",
            role_description="스포츠 에이전시 수석 오케스트레이터 및 워크플로우 분기 라우터",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
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
        logs = self._append_model_log(state, "Node 1: Supervisor Router", model_used)
        return {
            "supervisor_note": note,
            "model_usage_log": logs,
        }

    def route(
        self,
        state: AgencyGraphState,
    ) -> Literal["hermes_transfer", "hermes_renewal"]:
        """Conditional routing edge determining transfer vs renewal pathway."""
        if state.get("track_mode") == "TRACK_A_TRANSFER":
            return "hermes_transfer"
        return "hermes_renewal"
