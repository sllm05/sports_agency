import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()
c.execute("SELECT count(*) FROM players WHERE position = 'MGR'")
print("Managers in players table:", c.fetchone()[0])
