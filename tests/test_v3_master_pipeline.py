"""
Automated Integration Tests for Sports Agency V3.0 Master Plan
Validates the 7-Agent Architecture, Career Agent Timing Decision,
Scouting Prospect Discovery, Triple Output Markdown Document Generation,
and FastAPI Endpoints.
"""

import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from mcp_server.football_mcp_server import (
    analyze_career_timing_and_path,
    discover_undervalued_prospects,
    export_triple_agency_documents,
)
from sports_agency.api.main import app
from sports_agency.graph.agency_workflow import WORKFLOW_MANAGER


class TestSportsAgencyV3MasterPlan(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_career_agent_timing_decision(self):
        """Test Tool 10: Career timing and path decision matrix."""
        res = analyze_career_timing_and_path("Heung-min Son")
        self.assertIn("path_label", res)
        self.assertIn("timing_decision", res)
        self.assertIn("three_year_roadmap", res)
        self.assertEqual(res["timing_decision"], "BOSMAN_RULE_WINDOW (FIFA RSTP Art. 18.3)")
        self.assertEqual(len(res["three_year_roadmap"]), 3)
        self.assertIn("1년차", res["three_year_roadmap"][0]["year"])

    def test_02_scouting_agent_prospect_discovery(self):
        """Test Tool 11: Discover undervalued prospects based on age, percentile, and market value."""
        prospects = discover_undervalued_prospects(max_age=23, min_percentile=75, limit=5)
        self.assertIsInstance(prospects, list)
        self.assertGreater(len(prospects), 0)
        for p in prospects:
            self.assertLessEqual(p["age"], 23)
            self.assertGreaterEqual(p["pos_percentile"], 75)

    def test_03_triple_agency_documents_export(self):
        """Test Tool 12: Export triple agency markdown documents to outputs/ directory."""
        career_md = "# 【커리어 보고서】\n\n테스트 커리어 로드맵"
        deal_md = "# 【협상 대외비】\n\n테스트 협상 치트시트"
        pitch_md = "# 【피칭 덱】\n\n테스트 피칭 덱"

        res = export_triple_agency_documents("Heung-min Son", career_md, deal_md, pitch_md)
        self.assertIn("career_report_file", res)
        self.assertIn("deal_prep_file", res)
        self.assertIn("pitch_deck_file", res)

        for key, fpath in res.items():
            self.assertTrue(Path(fpath).exists(), f"File {fpath} does not exist")

    def test_04_langgraph_workflow_pipeline(self):
        """Test LangGraph 8-node pipeline with Career Agent and Triple Writer."""
        thread_id = "test_v3_unittest_thread_01"
        res = WORKFLOW_MANAGER.start_session(
            thread_id=thread_id,
            player_name="Heung-min Son",
            track_mode="TRACK_A_TRANSFER",
            auto_complete=True,
        )
        self.assertEqual(res.get("status"), "COMPLETED")
        state = res.get("state", {})
        self.assertIn("career_strategy", state)
        self.assertIn("career_report_md", state)
        self.assertIn("deal_prep_md", state)
        self.assertIn("pitch_deck_md", state)
        self.assertIn("saved_files", state)

    def test_05_fastapi_endpoints(self):
        """Test FastAPI endpoints for V3.0 features."""
        # Health
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)

        # Career Timing
        res_career = self.client.get("/api/career/timing?player_name=Heung-min Son")
        self.assertEqual(res_career.status_code, 200)
        data_career = res_career.json()
        self.assertEqual(data_career.get("timing_decision"), "BOSMAN_RULE_WINDOW (FIFA RSTP Art. 18.3)")

        # Scout Prospects
        res_scout = self.client.get("/api/scout/prospects?max_age=23&limit=3")
        self.assertEqual(res_scout.status_code, 200)
        data_scout = res_scout.json()
        self.assertGreater(len(data_scout.get("prospects", [])), 0)

        # Output File Serving
        res_file = self.client.get("/api/outputs/Heung-min_Son/1_career_valuation_report.md")
        self.assertEqual(res_file.status_code, 200)
        self.assertIn("커리어 가치 평가", res_file.text)


if __name__ == "__main__":
    unittest.main()
