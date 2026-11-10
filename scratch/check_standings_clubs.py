import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(club_standings_and_finances)")
print([col[1] for col in c.fetchall()])

c.execute("SELECT club_name FROM club_standings_and_finances WHERE club_name LIKE '%Manchester%' OR club_name LIKE '%Tottenham%'")
for r in c.fetchall():
    print(r)
