import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(player_playstyle_and_tendencies)")
print("Columns:", [col[1] for col in c.fetchall()])
