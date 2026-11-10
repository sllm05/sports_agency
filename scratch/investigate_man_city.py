import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("--- CLUBS WITH 'Manchester' OR 'City' ---")
cur.execute("SELECT DISTINCT current_club, league, COUNT(*) as cnt FROM players WHERE current_club LIKE '%City%' OR current_club LIKE '%Manchester%' GROUP BY current_club, league")
for r in cur.fetchall():
    print(dict(r))

print("\n--- TEAMS TABLE WITH 'Manchester' OR 'City' ---")
cur.execute("SELECT * FROM teams WHERE name LIKE '%City%' OR name LIKE '%Manchester%'")
for r in cur.fetchall():
    print(dict(r))

print("\n--- ALL LEAGUES IN PLAYERS ---")
cur.execute("SELECT DISTINCT league, COUNT(*) as cnt FROM players GROUP BY league")
for r in cur.fetchall():
    print(dict(r))

print("\n--- VIRTUAL PLAYERS & MANAGERS ---")
cur.execute("SELECT COUNT(*) FROM players WHERE player_id >= 90000")
print("Virtual players (id >= 90000):", cur.fetchone()[0])
cur.execute("SELECT DISTINCT current_club, league FROM players WHERE player_id >= 90000")
for r in cur.fetchall():
    print("  Virtual club:", dict(r))

cur.execute("SELECT COUNT(*) FROM managers WHERE manager_id >= 90000")
print("Virtual managers (id >= 90000):", cur.fetchone()[0])
cur.execute("SELECT DISTINCT current_club FROM managers WHERE manager_id >= 90000")
for r in cur.fetchall():
    print("  Virtual mgr club:", dict(r))
