import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    client = httpx.Client(base_url=BASE_URL, timeout=15.0)

    print("=== 1. Health check ===")
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("Health check OK:", r.json())

    print("\n=== 2. Static HTML check ===")
    r = client.get("/")
    assert r.status_code == 200
    html = r.text
    assert 'id="page-portfolio"' in html
    assert 'id="page-recruitment"' in html
    assert 'id="modal-client-renewal"' in html
    assert 'id="modal-client-transfer"' in html
    assert 'id="modal-client-sign-club"' in html
    assert 'id="btn-scouting-watchlist"' in html
    print("Static HTML contains all pages, modals, and watchlist buttons!")

    print("\n=== 3. Check initial recruitment targets ===")
    r = client.get("/api/agency/recruitment-targets")
    assert r.status_code == 200
    data = r.json()
    initial_count = data["total_targets"]
    print(f"Initial targets count: {initial_count}")

    print("\n=== 4. Test Watchlist Toggle with Real Player (ID: 1990) ===")
    # Check status
    r = client.get("/api/agency/watchlist/check?target_id=1990&target_type=PLAYER")
    assert r.status_code == 200
    in_wl = r.json()["in_watchlist"]
    print(f"Target 1990 initially in watchlist: {in_wl}")

    if in_wl:
        # Toggle off first
        client.post("/api/agency/watchlist/toggle", json={"target_id": 1990, "target_type": "PLAYER"})

    # Toggle ON
    r = client.post("/api/agency/watchlist/toggle", json={"target_id": 1990, "target_type": "PLAYER"})
    assert r.status_code == 200
    res = r.json()
    assert res["in_watchlist"] is True
    print("Toggle ON succeeded:", res["message"])

    # Verify recruitment targets list updated
    r = client.get("/api/agency/recruitment-targets")
    targets = r.json()["targets"]
    found_1990 = next((t for t in targets if t["target_id"] == 1990 and t["target_type"] == "PLAYER"), None)
    assert found_1990 is not None, "Target 1990 should be in recruitment targets"
    assert found_1990["is_virtual"] is False, "Real player must have is_virtual=False"
    print(f"Found in Watchlist: {found_1990['name_ko']} ({found_1990['name']}), Club: {found_1990['current_club']}, Category: {found_1990['category']}")

    print("\n=== 5. Test 1-Page Pitch Deck Generation ===")
    r = client.post("/api/agency/recruitment-pitch", json={"target_id": 1990, "target_type": "PLAYER"})
    assert r.status_code == 200
    pitch_data = r.json()
    md = pitch_data.get("pitch_deck_markdown") or pitch_data.get("markdown_content")
    assert md and len(md) > 200
    print(f"Pitch Deck generated successfully! Length: {len(md)} chars. Preview:\n{md[:200]}...")

    print("\n=== 6. Enroll Scouted Target as Agency Client ===")
    r = client.post("/api/agency/enroll-client", json={
        "target_id": 1990,
        "target_type": "PLAYER",
        "lead_agent": "김대표 수석에이전트",
        "commission_pct": 5.0
    })
    assert r.status_code == 200
    print("Enrolled client:", r.json()["message"])

    # Verify portfolio
    r = client.get("/api/agency/portfolio")
    pf = r.json()
    client_ids = [p["client_id"] for p in pf.get("players", [])]
    assert 1990 in client_ids, "1990 should now be in active portfolio"
    print(f"Active clients count: {pf['summary']['total_clients']}")

    print("\n=== 7. Test Contract Renewal for Active Client ===")
    r = client.post("/api/agency/client/renew", json={
        "client_id": 1990,
        "client_type": "PLAYER",
        "new_weekly_wage_eur": 250000,
        "contract_years": 3,
        "new_buyout_eur": 120000000,
        "signing_bonus_eur": 5000000
    })
    assert r.status_code == 200
    print("Contract renewal result:", r.json()["message"])

    print("\n=== 8. Test Club Transfer for Active Client ===")
    r = client.post("/api/agency/client/transfer", json={
        "client_id": 1990,
        "client_type": "PLAYER",
        "destination_club": "Real Madrid CF",
        "destination_league": "La Liga",
        "transfer_fee_eur": 80000000,
        "new_weekly_wage_eur": 280000,
        "contract_years": 4
    })
    assert r.status_code == 200
    print("Club transfer result:", r.json()["message"])

    print("\n=== 9. Test Contract Termination ===")
    r = client.post("/api/agency/terminate-contract", json={
        "client_id": 1990,
        "client_type": "PLAYER",
        "reason": "원소속 복귀 및 테스트 완료"
    })
    assert r.status_code == 200
    print("Contract termination result:", r.json()["message"])

    # Remove from watchlist
    r = client.post("/api/agency/watchlist/toggle", json={"target_id": 1990, "target_type": "PLAYER"})
    assert r.status_code == 200
    assert r.json()["in_watchlist"] is False
    print("Cleaned up: 1990 removed from watchlist")

    print("\n=== 10. Test Virtual FA Target (90005 - Lukas Müller) ===")
    # Enroll
    r = client.post("/api/agency/enroll-client", json={
        "target_id": 90005,
        "target_type": "PLAYER",
        "lead_agent": "김대표 수석에이전트",
        "commission_pct": 5.0
    })
    assert r.status_code == 200
    print("Enrolled virtual FA client:", r.json()["message"])

    # Sign with a virtual club
    r = client.post("/api/agency/client/sign-club", json={
        "client_id": 90005,
        "client_type": "PLAYER",
        "destination_club": "메트로폴리스 FC",
        "destination_league": "가상 유로 챌린지",
        "weekly_wage_eur": 35000,
        "contract_years": 2
    })
    assert r.status_code == 200
    print("FA Signing result:", r.json()["message"])

    # Terminate back to pool
    r = client.post("/api/agency/terminate-contract", json={
        "client_id": 90005,
        "client_type": "PLAYER",
        "reason": "계약 만료 테스트"
    })
    assert r.status_code == 200
    print("Terminated virtual client back to recruitment pool:", r.json()["message"])

    print("\n==========================================")
    print("ALL 10 END-TO-END WORKFLOW TESTS PASSED 100%!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
