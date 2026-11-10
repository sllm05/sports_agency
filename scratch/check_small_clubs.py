import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT current_club, count(*) FROM players GROUP BY current_club HAVING count(*) <= 2")
for r in cur.fetchall():
    print(dict(r))
