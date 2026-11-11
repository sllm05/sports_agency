import sqlite3
conn = sqlite3.connect('data/agency_desk.db')
cur = conn.cursor()
cur.execute("SELECT league, current_club, COUNT(*) FROM players GROUP BY league, current_club ORDER BY league, COUNT(*) DESC")
rows = cur.fetchall()
league_clubs = {}
for league, club, cnt in rows:
    if league not in league_clubs:
        league_clubs[league] = []
    league_clubs[league].append(club)

for l, clubs in league_clubs.items():
    print(f"[{l}] ({len(clubs)} clubs): {clubs[:5]}...")
conn.close()
