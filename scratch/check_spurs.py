import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("--- Tottenham Hotspur ---")
cur.execute("SELECT player_id, name, current_club, league FROM players WHERE current_club = 'Tottenham Hotspur'")
for r in cur.fetchall():
    print(dict(r))

print("--- Tottenham Hotspur FC count ---")
cur.execute("SELECT count(*) FROM players WHERE current_club = 'Tottenham Hotspur FC'")
print("Count:", cur.fetchone()[0])
