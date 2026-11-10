import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("SELECT player_id, name, current_club, league FROM players WHERE player_id >= 90000")
print("Virtual players in players table:")
for r in c.fetchall():
    print(r)
c.execute("SELECT manager_id, name, current_club, league FROM managers WHERE manager_id >= 90000")
print("\nVirtual managers in managers table:")
for r in c.fetchall():
    print(r)
conn.close()
