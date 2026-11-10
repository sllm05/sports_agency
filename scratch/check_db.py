import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(players)")
print("Players columns:", [col[1] for col in c.fetchall()])

c.execute("SELECT * FROM players WHERE name LIKE '%Son%' OR name_ko LIKE '%손흥민%'")
for r in c.fetchall():
    print("Son in players:", r)

c.execute("SELECT * FROM players WHERE name LIKE '%Haaland%' OR name_ko LIKE '%홀란드%'")
for r in c.fetchall():
    print("Haaland in players:", r)

c.execute("SELECT DISTINCT current_club FROM players WHERE league = 'Premier League'")
pl_clubs = [r[0] for r in c.fetchall()]
print(f"Premier League clubs count: {len(pl_clubs)}")
print("Clubs:", pl_clubs)

c.execute("SELECT league, COUNT(DISTINCT current_club), COUNT(*) FROM players GROUP BY league")
for r in c.fetchall():
    print("League stats:", r)
