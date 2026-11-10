import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
cur = conn.cursor()
cur.execute("""
    SELECT p.name, s.minutes_played, s.appearances, s.season
    FROM players p JOIN player_stats s ON p.player_id = s.player_id
    WHERE s.minutes_played > 3800
    LIMIT 10
""")
for r in cur.fetchall():
    print(r)
conn.close()
