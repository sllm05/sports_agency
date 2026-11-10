import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT * FROM players WHERE player_id IN (90101, 90102, 90103)")
print("Virtual managers in players table:", c.fetchall())
