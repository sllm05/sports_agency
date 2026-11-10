import sqlite3
import urllib.request
import json
import re

print("==================================================================")
print("COMPREHENSIVE VERIFICATION SUITE FOR USER REQUEST #10")
print("==================================================================")

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

# 1. Check Son Heung-min
print("\n[CHECK 1] Son Heung-min (손흥민) Club & Transfer Status:")
c.execute("SELECT player_id, name, name_ko, current_club, league, nationality FROM players WHERE player_id = 2999")
son = c.fetchone()
print(f" -> Player: {son}")
assert son[3] == 'Los Angeles FC', f"Expected Los Angeles FC, got {son[3]}"
assert son[4] == 'Major League Soccer', f"Expected Major League Soccer, got {son[4]}"

c.execute("SELECT COUNT(*) FROM players WHERE current_club = 'Tottenham Hotspur FC' AND (name = 'Heung-min Son' OR name_ko = '손흥민')")
tot_son = c.fetchone()[0]
assert tot_son == 0, f"Son Heung-min must not be in Tottenham Hotspur FC! Found: {tot_son}"

c.execute("SELECT COUNT(*) FROM players WHERE current_club = 'Tottenham Hotspur FC'")
tot_count = c.fetchone()[0]
print(f" -> Tottenham Hotspur FC roster count without Son: {tot_count} players (Pass)")

# 2. Check Erling Haaland
print("\n[CHECK 2] Erling Haaland (홀란드) Duplicate Check:")
c.execute("SELECT player_id, name, name_ko, current_club, league FROM players WHERE name LIKE '%Haaland%'")
haaland_players = c.fetchall()
print(f" -> Haaland in players table: {len(haaland_players)} row(s)")
assert len(haaland_players) == 1, f"Expected exactly 1 Haaland row, found {len(haaland_players)}: {haaland_players}"
print(f"    {haaland_players[0]}")

c.execute("SELECT target_id, target_type, name, name_ko, category FROM agency_recruitment_targets WHERE name LIKE '%Haaland%'")
haaland_targets = c.fetchall()
print(f" -> Haaland in agency_recruitment_targets: {len(haaland_targets)} row(s)")
assert len(haaland_targets) == 1, f"Expected 1 target row, got {len(haaland_targets)}"
print(f"    {haaland_targets[0]}")

c.execute("SELECT DISTINCT current_club FROM players WHERE league = 'Premier League'")
pl_clubs = [r[0] for r in c.fetchall()]
print(f" -> Premier League distinct clubs: {len(pl_clubs)}")
assert len(pl_clubs) == 20, f"Premier League must have exactly 20 clubs, found {len(pl_clubs)}: {pl_clubs}"
assert 'Manchester City FC' in pl_clubs
assert 'Manchester City' not in pl_clubs

# 3. Check Leagues and Test League
print("\n[CHECK 3] League Structure & Removal of '가상리그':")
c.execute("SELECT DISTINCT league, COUNT(*) FROM players GROUP BY league")
leagues = c.fetchall()
for lg in leagues:
    print(f" -> {lg[0]}: {lg[1]} players")

# Ensure no league has '가상' in its name
c.execute("SELECT COUNT(*) FROM players WHERE league LIKE '%가상%' OR league LIKE '%Virtual%'")
virtual_count = c.fetchone()[0]
assert virtual_count == 0, f"Found {virtual_count} players with 가상/Virtual in league name!"

c.execute("SELECT COUNT(*) FROM players WHERE league = '테스트 리그 (Test League)'")
test_count = c.fetchone()[0]
assert test_count == 18, f"Expected 18 test players/managers, got {test_count}"
print(f" -> Test League (테스트 리그): {test_count} players/managers (Pass)")

# 4. Check Frontend HTML
print("\n[CHECK 4] Frontend HTML Verification:")
with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert 'VIRTUAL_LEAGUE' not in html or '<option value="VIRTUAL_LEAGUE">' not in html, "Found VIRTUAL_LEAGUE option in HTML!"
assert '<option value="TEST_LEAGUE">🧪 테스트 리그 (Test League)</option>' in html, "TEST_LEAGUE option missing!"
print(" -> <option value=\"TEST_LEAGUE\"> present and VIRTUAL_LEAGUE option removed (Pass)")

assert 'function formatPlayerName(p)' in html, "formatPlayerName function missing!"
print(" -> formatPlayerName function implemented (Pass)")

# 5. Check Live API
print("\n[CHECK 5] Live API & Web Server Verification (Port 8000):")
req = urllib.request.urlopen('http://127.0.0.1:8000/api/players')
data = json.loads(req.read().decode('utf-8'))
all_p = data.get('all_players', [])

son_api = [p for p in all_p if p.get('player_id') == 2999][0]
print(f" -> API Son Heung-min: {son_api['name']} ({son_api['name_ko']}) | Club: {son_api['current_club']} | League: {son_api['league']}")
assert son_api['current_club'] == 'Los Angeles FC'
assert son_api['league'] == 'Major League Soccer'

haaland_api = [p for p in all_p if 'haaland' in p.get('name', '').lower()]
print(f" -> API Haaland count: {len(haaland_api)}")
assert len(haaland_api) == 1
assert haaland_api[0]['current_club'] == 'Manchester City FC'

korean_api = [p for p in all_p if p.get('nationality') == 'South Korea']
print(f" -> Korean players count in API: {len(korean_api)}")
for kp in korean_api:
    print(f"    ID {kp['player_id']}: {kp['name']} ({kp['name_ko']}) | {kp['current_club']} ({kp['league']})")

conn.close()
print("\n==================================================================")
print("ALL VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
print("==================================================================")
