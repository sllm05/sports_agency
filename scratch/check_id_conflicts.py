import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()
c.execute("SELECT player_id, name FROM players WHERE player_id IN (101, 102, 103, 104)")
print("Player ID 101-104:", c.fetchall())

# Check max player_id
c.execute("SELECT max(player_id) FROM players")
print("Max player_id:", c.fetchone()[0])
