import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
cur = conn.cursor()
cur.execute("UPDATE agency_recruitment_targets SET scouting_status = 'TARGETED'")
conn.commit()
conn.close()
print("Reset all recruitment targets to TARGETED")
