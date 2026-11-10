import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

print("Searching for player_id=2999 across all tables...")
for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    for col in cols:
        try:
            c.execute(f"SELECT * FROM {t} WHERE CAST({col} AS TEXT) = '2999'")
            rows = c.fetchall()
            if rows:
                print(f"[{t}.{col}] -> {len(rows)} rows found")
                for r in rows:
                    print("   ", r)
        except Exception:
            pass
