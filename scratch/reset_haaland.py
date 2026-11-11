import sqlite3
conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("UPDATE players SET current_club='Manchester City FC', weekly_wage_eur=450000 WHERE player_id=1")
conn.commit()
c.execute("SELECT player_id, name, current_club, weekly_wage_eur FROM players WHERE player_id=1")
print("Reset Haaland row:", c.fetchone())
conn.close()
