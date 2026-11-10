import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

print("Searching for 'Son' / '손흥민' across all tables...")
for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    text_cols = [col for col in cols]
    for col in text_cols:
        try:
            c.execute(f"SELECT * FROM {t} WHERE CAST({col} AS TEXT) LIKE '%손흥민%' OR CAST({col} AS TEXT) LIKE '%Heung-min Son%'")
            rows = c.fetchall()
            if rows:
                print(f"[{t}.{col}] -> {len(rows)} rows found")
                for r in rows[:3]:
                    print("   ", r)
        except Exception as e:
            pass

print("\nSearching for 'Haaland' / '홀란드' across all tables...")
for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    for col in cols:
        try:
            c.execute(f"SELECT * FROM {t} WHERE CAST({col} AS TEXT) LIKE '%홀란드%' OR CAST({col} AS TEXT) LIKE '%Haaland%'")
            rows = c.fetchall()
            if rows:
                print(f"[{t}.{col}] -> {len(rows)} rows found")
                for r in rows[:3]:
                    print("   ", r)
        except Exception as e:
            pass
