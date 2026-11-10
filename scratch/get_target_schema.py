import sqlite3
conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='agency_recruitment_targets'")
row = c.fetchone()
print(row[0] if row else "Table not found")
conn.close()
