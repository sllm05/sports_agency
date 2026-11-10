import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("UPDATE players SET player_id = 2760 WHERE player_id = 90011")
c.execute("UPDATE player_stats SET player_id = 2760 WHERE player_id = 90011")
c.execute("UPDATE market_value_history SET player_id = 2760 WHERE player_id = 90011")
c.execute("UPDATE career_discipline_and_ucl SET player_id = 2760 WHERE player_id = 90011")
c.execute("UPDATE player_playstyle_and_tendencies SET player_id = 2760 WHERE player_id = 90011")

conn.commit()
print("Updated Jeong Sang-bin player_id from 90011 to 2760 successfully!")
