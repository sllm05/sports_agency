import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

# Check all leagues and club counts in players
c.execute("""
SELECT league, current_club, COUNT(*) 
FROM players 
GROUP BY league, current_club 
ORDER BY league, COUNT(*) ASC
""")

for league, club, cnt in c.fetchall():
    print(f"[{league}] '{club}': {cnt} players")
