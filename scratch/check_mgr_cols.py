import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(managers)")
cols = [col[1] for col in c.fetchall()]
print("Columns in managers:", cols)
