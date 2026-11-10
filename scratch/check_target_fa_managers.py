import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, current_club, league, position FROM players WHERE name LIKE '%Guardiola%' OR name LIKE '%Klopp%' OR name LIKE '%Zidane%' OR name LIKE '%Sarri%'")
print("Target managers in players table:", c.fetchall())

c.execute("SELECT * FROM managers WHERE name LIKE '%Guardiola%'")
print("Pep in managers table:", c.fetchall())

c.execute("SELECT * FROM recruitment_targets WHERE target_name LIKE '%Guardiola%'")
print("Pep in recruitment_targets table:", c.fetchall())
