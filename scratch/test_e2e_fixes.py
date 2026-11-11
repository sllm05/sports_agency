import sys
import json
from pathlib import Path

# Add project roots
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from fastapi.testclient import TestClient
from sports_agency.api.main import app
from sports_agency.agents.document_writer import _build_datamb_percentile_bars_html

client = TestClient(app)

def run_tests():
    print("=== STARTING E2E VERIFICATION ===")

    # 1. Test GET /api/clubs/by-league
    res = client.get("/api/clubs/by-league")
    assert res.status_code == 200, f"clubs/by-league failed: {res.status_code}"
    leagues = res.json()
    assert "Premier League" in leagues or "La Liga" in leagues, "Leagues not found in response"
    print("✓ Test 1: GET /api/clubs/by-league passed. Leagues found:", list(leagues.keys())[:3])

    # 2. Test POST /api/agency/client/renew-pipeline (Image 5 fix: no [object Object] error)
    payload_renew = {
        "client_id": 1,
        "client_type": "PLAYER",
        "requested_weekly_wage_eur": 560000,
        "contract_extension_years": 3,
        "signing_bonus_eur": 0,
        "new_release_clause_eur": None,
        "action": "EVALUATE"
    }
    res_renew = client.post("/api/agency/client/renew-pipeline", json=payload_renew)
    assert res_renew.status_code == 200, f"renew-pipeline failed: {res_renew.status_code} {res_renew.text}"
    renew_data = res_renew.json()
    assert "director_notes" in renew_data or "club_decision" in renew_data, "renew-pipeline keys missing"
    print("✓ Test 2: POST /api/agency/client/renew-pipeline passed. Decision:", renew_data.get("club_decision"))

    # 3. Test POST /api/agency/client/transfer-pipeline EVALUATE & EXECUTE (Image 4 & 6 fixes: no undefined · undefined)
    payload_eval = {
        "client_id": 1,
        "client_type": "PLAYER",
        "destination_club": "Real Madrid",
        "destination_league": "La Liga",
        "offered_transfer_fee_eur": 230000000,
        "offered_weekly_wage_eur": 607500,
        "contract_years": 4,
        "action": "EVALUATE"
    }
    res_eval = client.post("/api/agency/client/transfer-pipeline", json=payload_eval)
    assert res_eval.status_code == 200, f"transfer EVALUATE failed: {res_eval.status_code} {res_eval.text}"
    eval_data = res_eval.json()
    assert eval_data.get("destination_club") == "Real Madrid", f"Expected Real Madrid, got {eval_data.get('destination_club')}"
    assert eval_data.get("destination_league") == "La Liga", f"Expected La Liga, got {eval_data.get('destination_league')}"
    assert "stage_1_fee_and_buyout" in eval_data, "stage_1_fee_and_buyout missing"
    assert "stage_4_fifa_tms_clearing" in eval_data, "stage_4_fifa_tms_clearing missing"
    print("✓ Test 3a: POST /api/agency/client/transfer-pipeline EVALUATE passed. Club/League:", eval_data.get("destination_club"), eval_data.get("destination_league"))

    # 4. Test DocumentWriter DataMB percentile bars formatting (Image 2 fix)
    sample_player = {
        "progressive_actions_per90": 14.44,
        "key_passes_per90": 3.38,
        "goals_per90": 0.85,
        "xg_per90": 0.65,
        "xa_per90": 0.35,
        "defensive_duels_won_pct": 58.5,
        "minutes_played": 2650
    }
    html_bars = _build_datamb_percentile_bars_html(sample_player)
    assert "\n\n" not in html_bars, "Found multiline blank line break in html bars, which breaks Markdown!"
    assert 'style="margin-bottom: 10px;"' in html_bars
    print("✓ Test 4: DocumentWriter percentile bars passed (no Markdown-breaking blank lines).")

    # 5. Check index.html for zero hardcoded dummy 30.2 aging curve
    with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    assert "incumbentCurve = [82, 70, 58, 46]" not in html_code, "Found hardcoded incumbentCurve dummy template!"
    assert "setBosmanTargetType" in html_code, "setBosmanTargetType function missing in index.html"
    assert "transfer-club-select" in html_code, "transfer-club-select missing in index.html"
    assert "switchScatterView" in html_code, "switchScatterView missing in index.html"
    print("✓ Test 5: UI enhancements and dynamic aging curve verified.")

    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
