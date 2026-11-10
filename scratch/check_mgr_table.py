import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM players WHERE position = 'MGR'")
print("Players with position='MGR':", c.fetchone()[0])

c.execute("SELECT player_id, name, current_club, league, position FROM players WHERE position = 'MGR' LIMIT 10")
for r in c.fetchall():
    print(r)

c.execute("SELECT COUNT(*) FROM managers")
print("Total rows in managers table:", c.fetchone()[0])
