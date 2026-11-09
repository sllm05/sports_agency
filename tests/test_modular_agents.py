"""
Unit Test Suite for Modular Sports Agency Agents (`tests/test_modular_agents.py`)

Verifies:
1. Each agent class can be instantiated independently.
2. Individual agent execution operates cleanly on standard AgencyGraphState.
3. Supervisor routing functions properly.
4. Schemas and BaseAgent contracts are strictly respected.
"""

import unittest
from sports_agency.agents import (
    CAREER_STRATEGIST_AGENT,
    DOCUMENT_WRITER_AGENT,
    LEGAL_COMPLIANCE_AGENT,
    NEGOTIATION_SPARRING_AGENT,
    RENEWAL_ANALYST_AGENT,
    SCOUTING_ANALYST_AGENT,
    SUPERVISOR_AGENT,
    BaseAgent,
    CareerStrategistAgent,
    DocumentWriterAgent,
    LegalComplianceAgent,
    NegotiationSparringAgent,
    RenewalAnalystAgent,
    ScoutingAnalystAgent,
    SupervisorAgent,
)
from sports_agency.schemas.agent_schemas import AgencyGraphState


class TestModularAgents(unittest.TestCase):
    def test_agent_instances_and_inheritance(self):
        """Tests that all agent classes inherit from BaseAgent and have valid metadata."""
        agents = [
            SUPERVISOR_AGENT,
            SCOUTING_ANALYST_AGENT,
            RENEWAL_ANALYST_AGENT,
            CAREER_STRATEGIST_AGENT,
            LEGAL_COMPLIANCE_AGENT,
            NEGOTIATION_SPARRING_AGENT,
            DOCUMENT_WRITER_AGENT,
        ]
        for ag in agents:
            self.assertIsInstance(ag, BaseAgent)
            self.assertTrue(bool(ag.name))
            self.assertTrue(bool(ag.role_description))

    def test_supervisor_agent_routing(self):
        """Tests SupervisorAgent run and route methods in isolation."""
        agent = SupervisorAgent()
        state_transfer: AgencyGraphState = {
            "player_name": "Heung-min Son",
            "track_mode": "TRACK_A_TRANSFER",
            "target_wage_increase_pct": 20,
            "priority_goal": "UCL 우승 클럽 이적",
            "model_usage_log": [],
        }
        res = agent.run(state_transfer)
        self.assertIn("supervisor_note", res)
        self.assertEqual(len(res["model_usage_log"]), 1)
        self.assertEqual(agent.route(state_transfer), "hermes_transfer")

        state_renewal: AgencyGraphState = {
            "player_name": "Min-Jae Kim",
            "track_mode": "TRACK_B_RENEWAL",
            "target_wage_increase_pct": 15,
            "priority_goal": "재계약 및 주급 인상",
            "model_usage_log": [],
        }
        self.assertEqual(agent.route(state_renewal), "hermes_renewal")

    def test_scouting_analyst_agent_isolation(self):
        """Tests ScoutingAnalystAgent execution on a player profile."""
        agent = ScoutingAnalystAgent()
        state: AgencyGraphState = {
            "player_name": "Heung-min Son",
            "track_mode": "TRACK_A_TRANSFER",
            "target_wage_increase_pct": 25,
            "preferred_league": "Premier League",
            "hermes_tool_trace": [],
            "model_usage_log": [],
        }
        res = agent.run(state)
        self.assertIn("player_profile", res)
        self.assertIn("peer_wage_band", res)
        self.assertIn("matched_clubs", res)
        self.assertIn("psr_and_tax_breakdown", res)
        self.assertIn("hermes_ai_summary", res)
        self.assertEqual(res["player_profile"]["name"], "Heung-min Son")

    def test_renewal_analyst_agent_isolation(self):
        """Tests RenewalAnalystAgent execution on a renewal track."""
        agent = RenewalAnalystAgent()
        state: AgencyGraphState = {
            "player_name": "Min-Jae Kim",
            "track_mode": "TRACK_B_RENEWAL",
            "target_wage_increase_pct": 10,
            "hermes_tool_trace": [],
            "model_usage_log": [],
        }
        res = agent.run(state)
        self.assertIn("player_profile", res)
        self.assertIn("psr_and_tax_breakdown", res)
        # Renewal transfer fee amortization should be €0
        self.assertEqual(res["psr_and_tax_breakdown"]["annual_transfer_amortization_eur"], 0)


if __name__ == "__main__":
    unittest.main()
