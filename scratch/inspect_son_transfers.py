import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT * FROM transfer_history WHERE player_name LIKE '%Son%' OR player_name LIKE '%손%'")
for r in c.fetchall():
    print("transfer_history:", r)

c.execute("SELECT * FROM agency_recruitment_targets WHERE name LIKE '%Son%' OR name_ko LIKE '%손%'")
for r in c.fetchall():
    print("agency_recruitment_targets:", r)

c.execute("SELECT * FROM players WHERE is_agency_client = 1")
print("Agency clients:")
for r in c.fetchall():
    print("Client:", r[0], r[1], r[2], r[4], r[5], r[6])
