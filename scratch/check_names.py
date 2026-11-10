import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, name_ko, nationality, is_agency_client FROM players LIMIT 20")
for r in c.fetchall():
    print(r)

print("\n--- Korean Players ---")
c.execute("SELECT player_id, name, name_ko, nationality, current_club, league FROM players WHERE nationality = 'South Korea'")
for r in c.fetchall():
    print(r)

print("\n--- Foreign Players with Korean name_ko ---")
c.execute("SELECT player_id, name, name_ko, nationality FROM players WHERE nationality != 'South Korea' AND name != name_ko LIMIT 20")
for r in c.fetchall():
    print(r)
