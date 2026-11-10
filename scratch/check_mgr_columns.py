import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(players)")
columns = [col[1] for col in c.fetchall()]
print("Columns in players:", columns)

c.execute("SELECT * FROM players WHERE position = 'MGR' LIMIT 2")
for r in c.fetchall():
    print("MGR row in players:", dict(zip(columns, r)))
