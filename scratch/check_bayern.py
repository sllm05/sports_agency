import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
cur = conn.cursor()
cur.execute("SELECT DISTINCT current_club FROM players WHERE current_club LIKE '%Bayern%' OR current_club LIKE '%뮌헨%'")
print(cur.fetchall())
