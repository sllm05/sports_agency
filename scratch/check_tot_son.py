import sqlite3
conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()
c.execute("SELECT player_id, name, nationality, current_club FROM players WHERE current_club = 'Tottenham Hotspur FC' AND (name LIKE '%son%' OR name_ko LIKE '%손흥민%')")
print(c.fetchall())
