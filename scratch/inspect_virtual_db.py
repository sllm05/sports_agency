import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, current_club, league, is_agency_client FROM players WHERE player_id >= 90000")
print("Virtual players:")
for r in c.fetchall():
    print(r)

c.execute("SELECT manager_id, name, current_club, league, is_agency_client FROM managers WHERE manager_id >= 90000")
print("\nVirtual managers:")
for r in c.fetchall():
    print(r)
