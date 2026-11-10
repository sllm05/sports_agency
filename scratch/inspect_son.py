import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT * FROM players WHERE name LIKE '%Son%' OR name_ko LIKE '%손흥민%'")
for r in c.fetchall():
    print("Player:", r)

c.execute("SELECT * FROM agency_contracts WHERE client_name LIKE '%손흥민%' OR client_name LIKE '%Son%'")
for r in c.fetchall():
    print("Agency contract:", r)

c.execute("SELECT * FROM transfer_history WHERE player_id = 2999")
for r in c.fetchall():
    print("Transfer history 2999:", r)
