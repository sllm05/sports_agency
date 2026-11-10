import sqlite3

def check_or_update():
    conn = sqlite3.connect('data/agency_desk.db')
    cur = conn.cursor()

    # 1. Add columns to managers if needed
    cur.execute("PRAGMA table_info(managers)")
    cols = [r[1] for r in cur.fetchall()]
    if 'name_ko' not in cols:
        cur.execute("ALTER TABLE managers ADD COLUMN name_ko TEXT")
        print("Added name_ko to managers")
    if 'is_agency_client' not in cols:
        cur.execute("ALTER TABLE managers ADD COLUMN is_agency_client INTEGER DEFAULT 0")
        print("Added is_agency_client to managers")

    # 2. Check existing managers
    cur.execute("SELECT manager_id, name FROM managers WHERE manager_id >= 101 AND manager_id <= 104")
    print("Existing 101-104 managers:", cur.fetchall())

    conn.commit()
    conn.close()

if __name__ == '__main__':
    check_or_update()
