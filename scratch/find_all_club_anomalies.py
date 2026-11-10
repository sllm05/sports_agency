import sqlite3
from collections import defaultdict

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, name_ko, current_club, league FROM players")
players = c.fetchall()

clubs_by_league = defaultdict(lambda: defaultdict(list))
for p in players:
    clubs_by_league[p[4]][p[3]].append((p[0], p[1]))

print("--- CLUBS BY LEAGUE ---")
for lg, clubs in clubs_by_league.items():
    print(f"\n[LEAGUE: {lg}] (Total clubs: {len(clubs)})")
    for clb, plist in sorted(clubs.items(), key=lambda x: len(x[1])):
        if len(plist) <= 5:
            print(f"  Club '{clb}': {len(plist)} players -> {[p[1] for p in plist]}")

print("\n--- MANAGERS ---")
c.execute("SELECT manager_id, name, current_club, league FROM managers")
for m in c.fetchall():
    if m[3] not in ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']:
        print(f"Non-5-league manager: {m}")
