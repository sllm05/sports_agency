import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT DISTINCT competition_code, competition_name, count(*) FROM club_standings_and_finances GROUP BY competition_code, competition_name")
for r in c.fetchall():
    print(r)
