import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT DISTINCT league FROM players")
print("Leagues in players:", [r[0] for r in c.fetchall()])

c.execute("SELECT DISTINCT league FROM managers")
print("Leagues in managers:", [r[0] for r in c.fetchall()])

c.execute("SELECT player_id, name, current_club, league FROM players WHERE current_club LIKE '%Bayern%' or current_club LIKE '%뮌헨%'")
print("\nBayern/Munchen players:")
for r in c.fetchall():
    print(r)

c.execute("SELECT player_id, name, current_club, league FROM players WHERE player_id IN (1, 2998, 2999)")
print("\nKey seeded players (1, 2998, 2999):")
for r in c.fetchall():
    print(r)

c.execute("SELECT player_id, name, current_club, league FROM players WHERE player_id >= 90000")
print("\nVirtual players (>= 90000):")
for r in c.fetchall():
    print(r)

c.execute("SELECT manager_id, name, current_club, league FROM managers")
print("\nManagers:")
for r in c.fetchall():
    print(r)
