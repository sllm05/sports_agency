import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT * FROM club_standings_and_finances WHERE competition_code = 'PL' LIMIT 1")
print(c.fetchone())
