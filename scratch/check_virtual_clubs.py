import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("SELECT target_id, name, name_ko, current_club, category, scouting_status FROM agency_recruitment_targets WHERE target_id >= 90000")
rows = c.fetchall()
print(f"Total virtual targets: {len(rows)}")
for r in rows:
    print(r)
conn.close()
