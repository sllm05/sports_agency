"""
Unit Test Suite for External Data Pipeline (`tests/test_data_pipeline.py`)
Verifies integration of Capology, Transfermarkt, Understat, and FBref percentile functions.
"""

import unittest
from sports_agency.data_pipeline import (
    compute_fbref_radar_percentiles,
    get_understat_real_match_moments,
    sync_capology_verified_wages,
)
from sports_agency.tactics_engine import build_player_tactics_payload


class TestDataPipeline(unittest.TestCase):
    def test_capology_verified_wages_sync(self):
        """Tests that Capology verified wages sync successfully."""
        updated = sync_capology_verified_wages()
        self.assertGreater(updated, 0)

    def test_understat_real_match_moments(self):
        """Tests that Understat returns real shot coordinates for top stars."""
        haaland_moments = get_understat_real_match_moments("Erling Haaland")
        self.assertIsNotNone(haaland_moments)
        self.assertGreaterEqual(len(haaland_moments), 2)
        self.assertIn("x", haaland_moments[0])
        self.assertIn("xg", haaland_moments[0])

    def test_fbref_radar_percentiles(self):
        """Tests DataMB 8-axis percentile computation."""
        percentiles = compute_fbref_radar_percentiles(1)
        self.assertEqual(len(percentiles), 8)
        self.assertIn("progressive_carries", percentiles)
        self.assertIn("xg_xa", percentiles)

    def test_tactics_engine_integrates_understat(self):
        """Tests that tactics engine loads Understat real match coordinates."""
        payload = build_player_tactics_payload("Erling Haaland")
        self.assertIsNotNone(payload)
        self.assertTrue(payload["success"])
        highlights = payload["key_match_highlights"]
        self.assertGreaterEqual(len(highlights), 1)
        self.assertIn("Understat", highlights[0]["title"])


if __name__ == "__main__":
    unittest.main()
