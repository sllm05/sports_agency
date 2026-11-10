import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("--- PLAYERS IN 'Manchester City' ---")
cur.execute("SELECT player_id, name, current_club, league FROM players WHERE current_club = 'Manchester City'")
for r in cur.fetchall():
    print(dict(r))

print("\n--- PLAYERS IN 'Manchester City FC' ---")
cur.execute("SELECT player_id, name, current_club, league FROM players WHERE current_club = 'Manchester City FC'")
for r in cur.fetchall():
    print(dict(r))

print("\n--- WHAT TABLES EXIST IN DB? ---")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for r in cur.fetchall():
    print(dict(r))
