import sys
sys.path.append('.')
import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("SELECT manager_id, name, current_club FROM managers WHERE name LIKE '%Xabi Alonso%'")
print("In managers table:", c.fetchall())
c.execute("SELECT player_id, name, current_club, position FROM players WHERE name LIKE '%Xabi Alonso%'")
print("In players table:", c.fetchall())
conn.close()
