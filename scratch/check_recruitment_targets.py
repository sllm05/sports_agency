import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(agency_recruitment_targets)")
print([col[1] for col in c.fetchall()])

c.execute("SELECT * FROM agency_recruitment_targets LIMIT 5")
for r in c.fetchall():
    print(r)
