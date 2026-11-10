import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT player_id, name, name_ko, nationality, current_club, league FROM players WHERE nationality = 'South Korea'")
korean_players = c.fetchall()

print(f"Total Korean players: {len(korean_players)}")
for p in korean_players:
    print(p)
