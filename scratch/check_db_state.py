import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(managers)")
print("Managers columns:", [r[1] for r in c.fetchall()])

c.execute("PRAGMA table_info(players)")
print("Players columns:", [r[1] for r in c.fetchall()])

c.execute("SELECT * FROM managers WHERE name LIKE '%Guardiola%'")
cols = [d[0] for d in c.description]
for r in c.fetchall():
    print(dict(zip(cols, r)))

c.execute("SELECT * FROM managers LIMIT 5")
for r in c.fetchall():
    print(dict(zip(cols, r)))
