import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
    try:
        with urllib.request.urlopen(req, data=body, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

print("=== 1. Checking Initial Portfolio State ===")
status, data = request("GET", "/api/agency/portfolio")
assert status == 200, f"Failed: {status}"
summary = data["summary"]
print(f"Total clients: {summary['total_clients']}, MV: €{summary['total_portfolio_value_eur']:,}")
assert summary["total_clients"] == 0, "Initial portfolio should have 0 active clients"

print("\n=== 2. Checking Recruitment Targets ===")
status, data = request("GET", "/api/agency/recruitment-targets")
assert status == 200, f"Failed: {status}"
targets = data["targets"]
print(f"Total targets: {len(targets)}")
assert len(targets) == 13, f"Expected 13 targets, got {len(targets)}"

players = [t for t in targets if t["target_type"] == "PLAYER"]
managers = [t for t in targets if t["target_type"] == "MANAGER"]
fa_targets = [t for t in targets if "무직" in (t.get("current_club") or "")]
print(f"Players: {len(players)}, Managers: {len(managers)}, FA (Unemployed): {len(fa_targets)}")
assert len(players) == 10, f"Expected 10 players, got {len(players)}"
assert len(managers) == 3, f"Expected 3 managers, got {len(managers)}"

print("\n=== 3. Testing 1-Page AI Pitch Deck Generation ===")
# Player pitch deck
status, data = request("POST", "/api/agency/recruitment-pitch", {"target_id": 90001, "target_type": "PLAYER"})
assert status == 200, f"Failed player pitch: {status}, {data}"
assert "pitch_deck_markdown" in data or "markdown_content" in data
print("Player pitch deck successfully generated!")

# Manager pitch deck
status, data = request("POST", "/api/agency/recruitment-pitch", {"target_id": 90101, "target_type": "MANAGER"})
assert status == 200, f"Failed manager pitch: {status}, {data}"
print("Manager pitch deck successfully generated!")

print("\n=== 4. Testing Contract Enrollment ===")
# Enroll player 90001
status, data = request("POST", "/api/agency/enroll-client", {
    "target_id": 90001,
    "target_type": "PLAYER",
    "lead_agent": "김대표 Agent",
    "commission_pct": 5.0
})
assert status == 200, f"Failed enrollment: {status}, {data}"
print("Enrolled player 90001: 박태양")

# Check portfolio has 1
status, data = request("GET", "/api/agency/portfolio")
assert data["summary"]["total_clients"] == 1
assert data["summary"]["total_portfolio_value_eur"] > 0
print(f"Portfolio after signing: 1 client, MV €{data['summary']['total_portfolio_value_eur']:,}")

# Check recruitment target status is SIGNED
status, data = request("GET", "/api/agency/recruitment-targets")
p90001 = next(t for t in data["targets"] if t["target_id"] == 90001)
assert p90001["scouting_status"] == "SIGNED"
print("Recruitment target status updated to SIGNED")

print("\n=== 5. Testing Contract Termination (Releasing back to pool) ===")
status, data = request("POST", "/api/agency/terminate-contract", {
    "client_id": 90001,
    "client_type": "PLAYER",
    "reason": "테스트 완료에 따른 영입 풀 복귀"
})
assert status == 200, f"Failed termination: {status}, {data}"
print("Terminated contract for player 90001")

# Check portfolio returns to 0
status, data = request("GET", "/api/agency/portfolio")
assert data["summary"]["total_clients"] == 0
assert data["summary"]["total_portfolio_value_eur"] == 0
print("Portfolio successfully returned to 0 clients, €0")

# Check recruitment target status is back to TARGETED
status, data = request("GET", "/api/agency/recruitment-targets")
p90001 = next(t for t in data["targets"] if t["target_id"] == 90001)
assert p90001["scouting_status"] == "TARGETED"
print("Recruitment target status restored to TARGETED")

print("\n=== ALL END-TO-END TESTS PASSED SUCCESSFULLY! ===")
