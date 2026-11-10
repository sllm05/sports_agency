import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, current_club, league, nationality FROM players WHERE nationality = 'South Korea' OR player_id IN (90011, 2997, 2998, 2999)")
for r in c.fetchall():
    print(r)
