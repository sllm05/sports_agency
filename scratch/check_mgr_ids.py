import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()
c.execute("SELECT player_id, name, current_club, position FROM players WHERE position = 'MGR' LIMIT 10")
for r in c.fetchall():
    print(r)
c.execute("SELECT min(player_id), max(player_id) FROM players WHERE position = 'MGR'")
print("MGR player_id range:", c.fetchall())
