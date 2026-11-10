import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("PRAGMA table_info(managers)")
cols = [r[1] for r in c.fetchall()]
print("Has name_ko in managers?", 'name_ko' in cols)
print("Has is_agency_client in managers?", 'is_agency_client' in cols)

# Check agency_contracts table to see how managers are linked
c.execute("PRAGMA table_info(agency_contracts)")
print("agency_contracts columns:", [r[1] for r in c.fetchall()])
c.execute("SELECT * FROM agency_contracts")
print("agency_contracts rows:")
for r in c.fetchall():
    print(r)
