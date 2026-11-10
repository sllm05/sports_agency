import sqlite3
from collections import defaultdict

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT league, current_club, count(*) FROM players GROUP BY league, current_club ORDER BY league, current_club")
rows = c.fetchall()

league_clubs = defaultdict(list)
for lg, clb, cnt in rows:
    league_clubs[lg].append((clb, cnt))

print("=== LEAGUE SUMMARY IN PLAYERS ===")
for lg, clbs in league_clubs.items():
    print(f"\n[LEAGUE: {lg}] Total Clubs: {len(clbs)}, Total Players: {sum(x[1] for x in clbs)}")
    if lg in ['Premier League', '테스트/가상 리그 (Virtual League)']:
        for clb, cnt in clbs:
            print(f"   {clb}: {cnt} members")

c.execute("SELECT player_id, name, current_club, league FROM players WHERE name LIKE '%Haaland%' OR name LIKE '%Son%' OR name LIKE '%Musiala%'")
print("\n=== KEY REAL PLAYERS ===")
for r in c.fetchall():
    print(r)

c.execute("SELECT player_id, name, current_club, league, position FROM players WHERE league = '테스트/가상 리그 (Virtual League)'")
print("\n=== VIRTUAL PLAYERS & MANAGERS IN PLAYERS TABLE ===")
for r in c.fetchall():
    print(r)

c.execute("SELECT manager_id, name, current_club, league FROM managers WHERE league = '테스트/가상 리그 (Virtual League)'")
print("\n=== VIRTUAL MANAGERS IN MANAGERS TABLE ===")
for r in c.fetchall():
    print(r)
