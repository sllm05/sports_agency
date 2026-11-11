"""
LangGraph Multi-Agent Workflow Orchestrator (`src/sports_agency/graph/agency_workflow.py`)

Connects modular, specialized Sports Agency AI agents into a high-performance,
checkpointed LangGraph workflow with Human-in-the-Loop (HITL) capability.

Architecture:
- Modular Agents: `sports_agency.agents.*`
- Structured Schemas & State: `sports_agency.schemas.agent_schemas.*`
- Graph State Engine: LangGraph StateGraph with SqliteSaver checkpointing
"""

from __future__ import annotations

import sqlite3
from typing import Any, Literal

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from sports_agency.agents import (
    CAREER_STRATEGIST_AGENT,
    DOCUMENT_WRITER_AGENT,
    LEGAL_COMPLIANCE_AGENT,
    NEGOTIATION_SPARRING_AGENT,
    RENEWAL_ANALYST_AGENT,
    SCOUTING_ANALYST_AGENT,
    SUPERVISOR_AGENT,
    apply_contract_override,
    invoke_hermes_mcp_tool,
)
from sports_agency.config import CONFIG
from sports_agency.schemas.agent_schemas import (
    AgencyGraphState,
    DualOutputDocsSchema,
    LegalRagReviewSchema,
    SparringRound1Schema,
    SparringRound2Schema,
    TripleOutputDocsSchema,
)

# Re-export schemas and helpers for backward compatibility with external imports
__all__ = [
    "AgencyGraphState",
    "DualOutputDocsSchema",
    "LegalRagReviewSchema",
    "SparringRound1Schema",
    "SparringRound2Schema",
    "TripleOutputDocsSchema",
    "_invoke_hermes_mcp_tool",
    "_apply_contract_override",
    "supervisor_node",
    "route_by_track",
    "hermes_transfer_node",
    "hermes_renewal_node",
    "career_agent_node",
    "legal_and_gbe_rag_node",
    "sparring_round_1_node",
    "sparring_round_2_node",
    "triple_output_writer_node",
    "dual_output_writer_node",
    "AgencyWorkflowManager",
    "WORKFLOW_MANAGER",
]

_invoke_hermes_mcp_tool = invoke_hermes_mcp_tool
_apply_contract_override = apply_contract_override


# ============================================================================
# Modular LangGraph Node Delegates
# ============================================================================

def supervisor_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 1: Supervisor Router Agent"""
    return SUPERVISOR_AGENT.run(state)


def route_by_track(
    state: AgencyGraphState,
) -> Literal["hermes_transfer", "hermes_renewal"]:
    """Conditional Edge: Routes to Transfer (2A) or Renewal (2B)"""
    return SUPERVISOR_AGENT.route(state)


def hermes_transfer_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 2A: Hermes Transfer & Scouting Analyst Agent"""
    return SCOUTING_ANALYST_AGENT.run(state)


def hermes_renewal_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 2B: Hermes Renewal & Wage Benchmarking Analyst Agent"""
    return RENEWAL_ANALYST_AGENT.run(state)


def career_agent_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 2C: Career Timing & Strategy Agent"""
    return CAREER_STRATEGIST_AGENT.run(state)


def legal_and_gbe_rag_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 3: Legal & GBE RAG Compliance Specialist Agent"""
    return LEGAL_COMPLIANCE_AGENT.run(state)


def sparring_round_1_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 4A: Sparring Negotiation Simulator (Round 1)"""
    return NEGOTIATION_SPARRING_AGENT.run_round_1(state)


def sparring_round_2_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 4B: Sparring Negotiation Simulator (Round 2 Human-in-the-Loop)"""
    return NEGOTIATION_SPARRING_AGENT.run_round_2(state)


def triple_output_writer_node(state: AgencyGraphState) -> dict[str, Any]:
    """Node 5: Triple-Output Practical Document Writer Agent"""
    return DOCUMENT_WRITER_AGENT.run(state)


# Backward compatibility alias
dual_output_writer_node = triple_output_writer_node


# ============================================================================
# Graph Builder & SqliteSaver Checkpointer Manager
# ============================================================================

class AgencyWorkflowManager:
    """
    Manages LangGraph workflow compilation, checkpoint database connections,
    and Human-in-the-Loop session resumption.
    """

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
        builder.add_node("career_agent", career_agent_node)
        builder.add_node("legal_rag", legal_and_gbe_rag_node)
        builder.add_node("sparring_round_1", sparring_round_1_node)
        builder.add_node("sparring_round_2", sparring_round_2_node)
        builder.add_node("triple_writer", triple_output_writer_node)

        builder.add_edge(START, "supervisor")
        builder.add_conditional_edges(
            "supervisor",
            route_by_track,
            {
                "hermes_transfer": "hermes_transfer",
                "hermes_renewal": "hermes_renewal",
            },
        )
        builder.add_edge("hermes_transfer", "career_agent")
        builder.add_edge("hermes_renewal", "career_agent")
        builder.add_edge("career_agent", "legal_rag")
        builder.add_edge("legal_rag", "sparring_round_1")
        builder.add_edge("sparring_round_1", "sparring_round_2")
        builder.add_edge("sparring_round_2", "triple_writer")
        builder.add_edge("triple_writer", END)

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
