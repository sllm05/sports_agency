import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("--- MANAGERS IN 'Manchester City' OR 'Manchester City FC' ---")
cur.execute("SELECT manager_id, name, name_ko, current_club FROM managers WHERE current_club LIKE '%Manchester%' OR current_club LIKE '%City%'")
for r in cur.fetchall():
    print(dict(r))

print("\n--- ARE THERE OTHER CLUBS WITH SLIGHT NAME MISMATCHES? ---")
cur.execute("SELECT DISTINCT current_club FROM players ORDER BY current_club")
clubs = [r[0] for r in cur.fetchall() if r[0]]
for c in clubs:
    # check if 'FC' or no 'FC' exists
    if c.endswith(' FC'):
        base = c[:-3]
        if base in clubs:
            print(f"Duplicate club found: '{c}' vs '{base}'")
    if c.endswith(' AFC'):
        base = c[:-4]
        if base in clubs:
            print(f"Duplicate club found: '{c}' vs '{base}'")
