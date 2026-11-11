import sqlite3
conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("PRAGMA table_info(players)")
cols = [r[1] for r in c.fetchall()]
print("Players columns:", cols)

c.execute("SELECT * FROM players WHERE id=1")
print("Row 1:", c.fetchone())
conn.close()
