import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("PRAGMA table_info(agency_recruitment_targets)")
print(c.fetchall())
conn.close()
