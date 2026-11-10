import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT manager_id, name, name_ko, nationality, current_club, league FROM managers")
managers = c.fetchall()
print(f"Total managers: {len(managers)}")
for m in managers[:10]:
    print(m)

korean_managers = [m for m in managers if m[3] == 'South Korea']
print(f"Korean managers: {len(korean_managers)}")
for m in korean_managers:
    print(m)
