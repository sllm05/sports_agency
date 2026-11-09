"""
Comprehensive Full Backend & V3.0 Master Plan Verification Suite
Tests all REST endpoints, LangGraph multi-agent orchestration, HITL interrupt/resume,
MCP tools, SQLite Vector RAG, and financial/tax calculations.
"""

import unittest
from fastapi.testclient import TestClient

from sports_agency.api.main import app


class TestFullBackendSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_system_health_and_status(self):
        """Test health and system vector/checkpointer status."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ok")

        res_status = self.client.get("/api/status")
        self.assertEqual(res_status.status_code, 200)
        data = res_status.json()
        self.assertIn("vector_db", data)
        self.assertIn("langgraph_checkpointer", data)

    def test_02_roster_and_analytics_endpoints(self):
        """Test players, managers, and analytics overview."""
        res_players = self.client.get("/api/players")
        self.assertEqual(res_players.status_code, 200)
        players = res_players.json()
        self.assertGreater(players["total_count"], 0)
        self.assertGreater(len(players["korean_roster"]), 0)

        res_managers = self.client.get("/api/managers")
        self.assertEqual(res_managers.status_code, 200)
        managers = res_managers.json()
        self.assertEqual(managers["total_count"], 96)

        res_analytics = self.client.get("/api/analytics/overview?comp=PL")
        self.assertEqual(res_analytics.status_code, 200)
        analytics = res_analytics.json()
        self.assertIn("standings_and_finances", analytics)
        self.assertIn("top_scorers", analytics)

    def test_03_player_complete_profile(self):
        """Test complete 360 profile for Korean stars and European peers."""
        for name in ["Heung-min Son", "Min-Jae Kim", "Erling Haaland"]:
            res = self.client.get(f"/api/players/{name}")
            self.assertEqual(res.status_code, 200, f"Failed for {name}")
            data = res.json()
            self.assertEqual(data["name"], name)
            self.assertIn("goals_per90", data)
            self.assertIn("pos_percentile", data)
            self.assertIn("valuation_and_profile", data)
            self.assertIn("playstyle_and_tendencies", data)

    def test_04_desk1_scouting_undervalued_prospects(self):
        """Module 1: Undervalued prospects discovery."""
        res = self.client.get("/api/scout/prospects?max_age=23&min_percentile=70&limit=5")
        self.assertEqual(res.status_code, 200)
        prospects = res.json()["prospects"]
        self.assertGreater(len(prospects), 0)
        for p in prospects:
            self.assertLessEqual(p["age"], 23)
            self.assertGreaterEqual(p["pos_percentile"], 70)

    def test_05_desk2_career_timing_matrix(self):
        """Module 2: Career timing decision matrix."""
        # Son Heung-min (Expiring contract -> Bosman window)
        res_son = self.client.get("/api/career/timing?player_name=Heung-min Son")
        self.assertEqual(res_son.status_code, 200)
        data_son = res_son.json()
        self.assertIn("timing_decision", data_son)
        self.assertIn("three_year_roadmap", data_son)
        self.assertEqual(data_son["timing_decision"], "BOSMAN_RULE_WINDOW (FIFA RSTP Art. 18.3)")

    def test_06_desk3_bosman_radar_and_manager_matching(self):
        """Module 3: Bosman targets radar."""
        res = self.client.get("/api/radar/bosman?position=LW&league=Premier League&max_contract_year=2026")
        self.assertEqual(res.status_code, 200)
        targets = res.json()["targets"]
        self.assertIsInstance(targets, list)

    def test_07_desk4_psr_and_tax_simulator(self):
        """Module 4: PSR amortization and 5 Big League tax simulator."""
        payload = {
            "league": "Premier League",
            "transfer_fee_eur": 40000000,
            "weekly_wage_eur": 120000,
            "contract_years": 4,
            "agent_fee_pct": 7.0,
            "signing_bonus_eur": 3000000,
        }
        res = self.client.post("/api/finance/psr-tax", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("annual_psr_book_cost_eur", data)
        self.assertIn("weekly_net_wage_eur", data)
        self.assertGreater(data["annual_psr_book_cost_eur"], 0)

    def test_08_dual_vector_rag_search(self):
        """Test FIFA legal regulations RAG and tactical scouting notes RAG."""
        # Legal search
        res_legal = self.client.post("/api/rag/search", json={
            "query": "FIFA RSTP Article 18.3 free agent pre-contract",
            "search_type": "REGULATIONS",
            "top_k": 3
        })
        self.assertEqual(res_legal.status_code, 200)
        self.assertEqual(res_legal.json()["search_type"], "LEGAL_REGULATIONS")
        self.assertGreater(len(res_legal.json()["results"]), 0)

        # Tactical search
        res_tactical = self.client.post("/api/rag/search", json={
            "query": "Inverted winger cut inside shooting",
            "search_type": "TACTICAL",
            "position": "LW",
            "top_k": 3
        })
        self.assertEqual(res_tactical.status_code, 200)
        self.assertEqual(res_tactical.json()["search_type"], "TACTICAL_SCOUTING_NOTES")

    def test_09_custom_client_manual_registration(self):
        """Test registering an external client without API-Football."""
        payload = {
            "name": "Jeong Sang-bin",
            "name_ko": "정상빈",
            "position": "RW",
            "secondary_positions": "ST, LW",
            "age": 22,
            "nationality": "South Korea",
            "current_club": "Minnesota United",
            "league": "Major League Soccer",
            "current_league_band": 3,
            "market_value_eur": 2500000,
            "weekly_wage_eur": 12000,
            "contract_expires": "2026-12-31",
            "goals_per90": 0.28,
            "assists_per90": 0.18,
            "xg_per90": 0.25,
            "xa_per90": 0.15,
            "key_passes_per90": 1.4,
            "progressive_actions_per90": 5.2,
            "defensive_duels_won_pct": 52.0,
            "minutes_played": 1850,
            "appearances": 24,
            "intl_match_pct": 20.0,
            "continental_minutes_pct": 0.0,
            "is_eu_citizen": 0,
            "strengths_summary": "Explosive sprint speed, direct transition counter-attack",
            "weaknesses_summary": "Aerial duel success, consistency against low block",
        }
        res = self.client.post("/api/players/custom", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ok")

    def test_10_langgraph_hitl_workflow_lifecycle(self):
        """
        Test the complete LangGraph workflow lifecycle:
        1. Start workflow with auto_complete=False -> Must interrupt at HITL!
        2. Verify checkpoint state in SqliteSaver.
        3. Resume with chosen strategy -> Must execute Round 2, PSR, and generate 3 documents!
        """
        thread_id = "test_hitl_lifecycle_thread_101"
        start_payload = {
            "player_name": "Min-Jae Kim",
            "track_mode": "TRACK_A_TRANSFER",
            "target_wage_increase_pct": 20,
            "priority_goal": "수비 핵심 주전 + 바이아웃 보너스",
            "preferred_league": "ALL",
            "auto_complete": False,
            "thread_id": thread_id,
        }
        res_start = self.client.post("/api/workflow/start", json=start_payload)
        self.assertEqual(res_start.status_code, 200)
        start_data = res_start.json()
        self.assertEqual(start_data["status"], "WAITING_FOR_HUMAN_STRATEGY")
        self.assertEqual(start_data["next_nodes"], ["sparring_round_2"])

        # Check session state from SqliteSaver
        res_state = self.client.get(f"/api/workflow/{thread_id}")
        self.assertEqual(res_state.status_code, 200)
        self.assertEqual(res_state.json()["status"], "WAITING_FOR_HUMAN_STRATEGY")

        # Resume with Human Strategy
        resume_payload = {
            "thread_id": thread_id,
            "human_action_choice": "OPTION_2_BONUS_AND_RELEASE_CLAUSE",
        }
        res_resume = self.client.post("/api/workflow/resume", json=resume_payload)
        self.assertEqual(res_resume.status_code, 200)
        resume_data = res_resume.json()
        self.assertEqual(resume_data["status"], "COMPLETED")
        final_state = resume_data["state"]
        self.assertIn("career_report_md", final_state)
        self.assertIn("deal_prep_md", final_state)
        self.assertIn("pitch_deck_md", final_state)
        self.assertIn("saved_files", final_state)

    def test_11_api_quota_and_status(self):
        """Test API-Football quota tracker endpoint."""
        res = self.client.get("/api/quota/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["provider"], "API-Football (API-Sports)")
        self.assertIn("calls_used", data)
        self.assertIn("calls_remaining", data)

    def test_12_dynamic_player_tactics_highlights(self):
        """Test dynamic player-specific 2D tactical highlight replay engine."""
        # 1. Test World Class Striker: Erling Haaland (Man City vs Arsenal)
        res_haaland = self.client.get("/api/tactics/player-highlights?player_name=Erling Haaland")
        self.assertEqual(res_haaland.status_code, 200)
        data_h = res_haaland.json()
        self.assertIn("Haaland", data_h["player_info"]["name"])
        self.assertEqual(data_h["player_info"]["target_slot_id"], "H11")  # ST slot
        self.assertEqual(data_h["match_info"]["home_team"], "Manchester City FC")
        self.assertEqual(data_h["match_info"]["away_team"], "Arsenal FC")
        self.assertEqual(len(data_h["home_roster"]), 11)
        self.assertEqual(len(data_h["away_roster"]), 11)
        target_p = next((p for p in data_h["home_roster"] if p.get("is_target")), None)
        self.assertIsNotNone(target_p)
        self.assertEqual(target_p["id"], "H11")
        self.assertEqual(len(data_h["key_match_highlights"]), 3)

        # 2. Test Winger: Bukayo Saka (Arsenal vs Man City)
        res_saka = self.client.get("/api/tactics/player-highlights?player_name=Bukayo Saka")
        self.assertEqual(res_saka.status_code, 200)
        data_s = res_saka.json()
        self.assertIn("Saka", data_s["player_info"]["name"])
        self.assertEqual(data_s["player_info"]["target_slot_id"], "H8")  # RW slot
        self.assertEqual(data_s["match_info"]["home_team"], "Arsenal FC")
        self.assertEqual(data_s["match_info"]["away_team"], "Manchester City FC")

        # 3. Test Defender: Min-Jae Kim (Bayern Munich vs Dortmund)
        res_kim = self.client.get("/api/tactics/player-highlights?player_name=Min-Jae Kim")
        self.assertEqual(res_kim.status_code, 200)
        data_k = res_kim.json()
        self.assertIn("Min-Jae Kim", data_k["player_info"]["name"])
        self.assertEqual(data_k["player_info"]["target_slot_id"], "H3")  # CB slot
        self.assertEqual(data_k["match_info"]["home_team"], "FC Bayern München")

        # 4. Unknown player returns 404
        res_404 = self.client.get("/api/tactics/player-highlights?player_name=NonExistentPlayerXYZ999")
        self.assertEqual(res_404.status_code, 404)


if __name__ == "__main__":
    unittest.main()
