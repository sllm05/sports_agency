import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

for t in tables:
    if t.startswith('sqlite_'): continue
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    for col in cols:
        try:
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} = 90011")
            cnt = c.fetchone()[0]
            if cnt > 0:
                print(f"Table '{t}', Column '{col}': {cnt} occurrences of 90011")
        except Exception:
            pass
