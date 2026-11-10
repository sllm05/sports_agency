import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("Tables in db:", tables)

for t in tables:
    if t.startswith('sqlite_'):
        continue
    c.execute(f"PRAGMA table_info({t})")
    cols = [col[1] for col in c.fetchall()]
    for col in cols:
        try:
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} = 'Manchester City'")
            cnt = c.fetchone()[0]
            if cnt > 0:
                print(f"Table '{t}', Column '{col}': {cnt} occurrences of 'Manchester City'")
        except Exception:
            pass
        try:
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} = 'Tottenham Hotspur'")
            cnt = c.fetchone()[0]
            if cnt > 0:
                print(f"Table '{t}', Column '{col}': {cnt} occurrences of 'Tottenham Hotspur'")
        except Exception:
            pass
        try:
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} = 'FC 바이에른 뮌헨'")
            cnt = c.fetchone()[0]
            if cnt > 0:
                print(f"Table '{t}', Column '{col}': {cnt} occurrences of 'FC 바이에른 뮌헨'")
        except Exception:
            pass
        try:
            c.execute(f"SELECT COUNT(*) FROM {t} WHERE {col} = '분데스리가'")
            cnt = c.fetchone()[0]
            if cnt > 0:
                print(f"Table '{t}', Column '{col}': {cnt} occurrences of '분데스리가'")
        except Exception:
            pass
