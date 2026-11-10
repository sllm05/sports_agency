import os
import sys
from fastapi.testclient import TestClient

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("./src"))

from sports_agency.api.main import app

client = TestClient(app)

def test_recruitment_targets():
    print("[1] Testing GET /api/agency/recruitment-targets...")
    res = client.get("/api/agency/recruitment-targets")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    targets = data.get("targets", [])
    print(f"  -> Found {len(targets)} recruitment targets (total: {len(targets)})")
    assert len(targets) == 15, f"Expected 15 targets, found {len(targets)}"

    # Check Pep Guardiola
    pep = next((t for t in targets if t["target_id"] == 101 and t["target_type"] == "MANAGER"), None)
    assert pep is not None, "Pep Guardiola (ID 101, MANAGER) not found!"
    print(f"  -> Pep Guardiola found: {pep['name_ko']} ({pep['name']}), category={pep['category']}, club={pep['current_club']}")
    assert pep["name_ko"] == "펩 과르디올라"
    assert pep["category"] == "FA_LEGEND"

    # Check Lamine Yamal
    yamal = next((t for t in targets if t["target_id"] == 2 and t["target_type"] == "PLAYER"), None)
    assert yamal is not None, "Lamine Yamal (ID 2, PLAYER) not found!"
    print(f"  -> Lamine Yamal found: {yamal['name_ko']} ({yamal['name']}), category={yamal['category']}")
    assert yamal["name_ko"] == "라민 야말"

    # Check managers and players count
    managers = [t for t in targets if t["target_type"] == "MANAGER"]
    players = [t for t in targets if t["target_type"] == "PLAYER"]
    print(f"  -> Managers: {len(managers)} (Guardiola, Klopp, Zidane, Sarri)")
    print(f"  -> Players: {len(players)}")
    assert len(managers) == 4, f"Expected 4 managers, found {len(managers)}"
    assert len(players) == 11, f"Expected 11 players, found {len(players)}"
    print("  [PASS] Recruitment targets test successful!")

def test_pitch_decks():
    print("\n[2] Testing POST /api/agency/recruitment-pitch...")
    # Pep Guardiola pitch deck
    res_pep = client.post("/api/agency/recruitment-pitch", json={
        "target_id": 101,
        "target_type": "MANAGER"
    })
    assert res_pep.status_code == 200, f"Pep pitch deck failed: {res_pep.status_code}"
    pep_data = res_pep.json()
    assert pep_data.get("status") == "success"
    pitch_pep = pep_data.get("markdown_content", "")
    assert "펩 과르디올라" in pitch_pep or "Pep Guardiola" in pitch_pep
    print(f"  -> Pep pitch deck generated ({len(pitch_pep)} chars)")

    # Lamine Yamal pitch deck
    res_yamal = client.post("/api/agency/recruitment-pitch", json={
        "target_id": 2,
        "target_type": "PLAYER"
    })
    assert res_yamal.status_code == 200, f"Yamal pitch deck failed: {res_yamal.status_code}"
    yamal_data = res_yamal.json()
    assert yamal_data.get("status") == "success"
    pitch_yamal = yamal_data.get("markdown_content", "")
    assert "라민 야말" in pitch_yamal or "Lamine Yamal" in pitch_yamal
    print(f"  -> Yamal pitch deck generated ({len(pitch_yamal)} chars)")
    print("  [PASS] Pitch decks test successful!")

def test_watchlist():
    print("\n[3] Testing Watchlist toggle & check...")
    # Toggle Pep in watchlist
    res_toggle = client.post("/api/agency/watchlist/toggle", json={
        "target_id": 101,
        "target_type": "MANAGER",
        "action": "TARGET"
    })
    assert res_toggle.status_code == 200
    toggle_data = res_toggle.json()
    assert toggle_data.get("status") == "success"
    print(f"  -> Toggled Pep to watchlist: {toggle_data.get('scouting_status')}")

    # Check watchlist
    res_check = client.get("/api/agency/watchlist/check?target_id=101&target_type=MANAGER")
    assert res_check.status_code == 200
    check_data = res_check.json()
    assert check_data.get("in_watchlist") is True
    print(f"  -> Check Pep watchlist: {check_data.get('in_watchlist')}")

    # Untoggle Pep
    res_untoggle = client.post("/api/agency/watchlist/toggle", json={
        "target_id": 101,
        "target_type": "MANAGER",
        "action": "UNWATCH"
    })
    assert res_untoggle.status_code == 200
    res_check2 = client.get("/api/agency/watchlist/check?target_id=101&target_type=MANAGER")
    check_data2 = res_check2.json()
    assert check_data2.get("in_watchlist") is False
    print(f"  -> Untoggled Pep: in_watchlist={check_data2.get('in_watchlist')}")
    print("  [PASS] Watchlist test successful!")

def test_html_ui():
    print("\n[4] Testing Static HTML Navigation & Scouting integration...")
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    assert 'id="nav-btn-recruitment"' not in html, "Found obsolete nav-btn-recruitment in navbar!"
    assert 'id="nav-btn-portfolio"' in html, "nav-btn-portfolio missing!"
    assert 'id="nav-btn-scouting"' in html, "nav-btn-scouting missing!"
    assert '선수·감독 스카우팅 & 영입' in html, "Combined scouting tab title missing!"

    # Check 3 sub-views
    assert 'id="scouting-view-recruitment"' in html, "scouting-view-recruitment missing!"
    assert 'id="scouting-view-watchlist"' in html, "scouting-view-watchlist missing!"
    assert 'id="scouting-view-all"' in html, "scouting-view-all missing!"

    # Check subview switcher buttons
    assert 'id="scout-view-tab-recruitment"' in html, "scout-view-tab-recruitment missing!"
    assert 'id="scout-view-tab-watchlist"' in html, "scout-view-tab-watchlist missing!"
    assert 'id="scout-view-tab-all"' in html, "scout-view-tab-all missing!"

    # Check JS functions
    assert 'switchScoutingView' in html, "switchScoutingView function missing!"
    assert 'loadAgencyRecruitmentTargets' in html, "loadAgencyRecruitmentTargets function missing!"
    assert 'buildRecruitmentCardHtml' in html, "buildRecruitmentCardHtml function missing!"
    print("  [PASS] Static HTML navigation & scouting integration test successful!")

if __name__ == "__main__":
    test_recruitment_targets()
    test_pitch_decks()
    test_watchlist()
    test_html_ui()
    print("\n🎉 ALL E2E TESTS PASSED PERFECTLY!")
