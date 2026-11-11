"""
Base Agent Module (`src/sports_agency/agents/base.py`)

Defines the foundational BaseAgent class and shared utilities for all
modular sports agency AI agents in the LangGraph workflow.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any

from mcp_server.football_mcp_server import HERMES_MCP_TOOLS
from sports_agency.schemas.agent_schemas import AgencyGraphState


def invoke_hermes_mcp_tool(
    tool_trace: list[dict[str, Any]],
    tool_name: str,
    args: dict[str, Any],
) -> Any:
    """
    Invokes an MCP tool from HERMES_MCP_TOOLS and logs the XML protocol call
    into the agent's tool trace for transparency and auditing.
    """
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


def apply_contract_override(
    profile: dict[str, Any],
    override: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Applies confidential contract overrides entered by the human agent onto
    the loaded player profile.
    """
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


class BaseAgent(ABC):
    """
    Abstract base class for all Sports Agency AI agents.
    Provides standardized metadata, lifecycle logging, and tool execution.
    """

    def __init__(self, name: str, role_description: str) -> None:
        self.name = name
        self.role_description = role_description

    def _append_model_log(
        self,
        state: AgencyGraphState,
        node_label: str,
        model_name: str,
    ) -> list[dict[str, str]]:
        """Appends model usage provenance to the state's model_usage_log list."""
        logs = list(state.get("model_usage_log", []))
        logs.append({"node": node_label, "model": model_name})
        return logs

    @abstractmethod
    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        """Executes the agent's core task and returns state update dictionary."""
        pass
