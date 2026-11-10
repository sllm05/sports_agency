import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(agency_recruitment_targets)")
print("agency_recruitment_targets columns:")
for r in c.fetchall():
    print(r)

c.execute("SELECT * FROM agency_recruitment_targets")
for r in c.fetchall():
    print(r)
