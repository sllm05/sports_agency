import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT * FROM club_squad_needs LIMIT 5")
for r in c.fetchall():
    print(r)
