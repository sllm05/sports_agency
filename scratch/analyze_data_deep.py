import sqlite3
from pathlib import Path

print("=== DATA/RAW BREAKDOWN ===")
raw_dir = Path("data/raw")
if raw_dir.exists():
    for f in sorted(raw_dir.glob("*")):
        if f.is_file():
            print(f"  {f.name:<45} | {f.stat().st_size / (1024*1024):>8.2f} MB")
        elif f.is_dir():
            s = sum(x.stat().st_size for x in f.rglob('*') if x.is_file())
            print(f"  {f.name + '/' :<45} | {s / (1024*1024):>8.2f} MB")

print("\n=== DATA/DATASETS BREAKDOWN ===")
ds_dir = Path("data/datasets")
if ds_dir.exists():
    for f in sorted(ds_dir.glob("*")):
        if f.is_file():
            print(f"  {f.name:<45} | {f.stat().st_size / (1024*1024):>8.2f} MB")
        elif f.is_dir():
            s = sum(x.stat().st_size for x in f.rglob('*') if x.is_file())
            print(f"  {f.name + '/' :<45} | {s / (1024*1024):>8.2f} MB")

print("\n=== DATA/DOCS BREAKDOWN ===")
docs_dir = Path("data/docs")
if docs_dir.exists():
    for f in sorted(docs_dir.glob("*")):
        if f.is_file():
            print(f"  {f.name:<45} | {f.stat().st_size / (1024*1024):>8.2f} MB")
        elif f.is_dir():
            s = sum(x.stat().st_size for x in f.rglob('*') if x.is_file())
            print(f"  {f.name + '/' :<45} | {s / (1024*1024):>8.2f} MB")

print("\n=== AGENCY_DESK.DB TABLES ===")
db_path = Path("data/agency_desk.db")
if db_path.exists():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    for t in tables:
        cur.execute(f"SELECT count(*) FROM {t}")
        cnt = cur.fetchone()[0]
        print(f"  Table: {t:<35} | {cnt:>8} rows")
    conn.close()

print("\n=== AGENCY_CHECKPOINTS.DB TABLES ===")
chk_path = Path("data/agency_checkpoints.db")
if chk_path.exists():
    conn = sqlite3.connect(chk_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    for t in tables:
        cur.execute(f"SELECT count(*) FROM {t}")
        cnt = cur.fetchone()[0]
        print(f"  Table: {t:<35} | {cnt:>8} rows")
    conn.close()
