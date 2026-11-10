import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT manager_id, name, current_club, league, contract_expires FROM managers WHERE current_club LIKE '%City%' OR current_club LIKE '%Manchester%'")
print("Manchester City managers:")
for r in c.fetchall():
    print(r)

c.execute("SELECT manager_id, name, current_club, league, contract_expires FROM managers WHERE current_club IN ('무직', 'FA') OR league LIKE '%무직%' OR current_club IS NULL")
print("Unemployed managers:")
for r in c.fetchall():
    print(r)

c.execute("SELECT count(*), league FROM managers GROUP BY league")
print("Managers by league:")
for r in c.fetchall():
    print(r)

# Let's check all managers name
c.execute("SELECT manager_id, name, current_club, league FROM managers")
rows = c.fetchall()
print(f"Total managers: {len(rows)}")
for r in rows[:15]:
    print(r)
