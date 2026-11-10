import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT manager_id, name, current_club, league FROM managers WHERE manager_id >= 90000 OR manager_id > 96")
print("Managers with manager_id > 96 or >= 90000:")
for r in c.fetchall():
    print(r)

c.execute("SELECT player_id, name, current_club, league, position FROM players WHERE player_id >= 90000 OR position = 'MGR' and player_id > 2700")
print("\nPlayers with id >= 90000:")
for r in c.fetchall():
    print(r)
