import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("All tables in agency_desk.db:", tables)

for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM [{t}]")
    cnt = cur.fetchone()[0]
    cur.execute(f"PRAGMA table_info([{t}])")
    cols = [c[1] for c in cur.fetchall()]
    print(f"- {t} ({cnt} rows): {cols[:6]} ...")

conn.close()
