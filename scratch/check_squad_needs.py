import sqlite3
conn = sqlite3.connect('data/agency_desk.db')
cur = conn.cursor()
cur.execute("PRAGMA table_info(club_squad_needs)")
cols = [r[1] for r in cur.fetchall()]
print("club_squad_needs columns:", cols)

cur.execute("SELECT * FROM club_squad_needs LIMIT 5")
for row in cur.fetchall():
    print(dict(zip(cols, row)))

conn.close()
