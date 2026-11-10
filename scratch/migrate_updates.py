import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

print("1. Updating Son Heung-min (player_id=2999) to Los Angeles FC (Major League Soccer)...")
c.execute("""
    UPDATE players
    SET current_club = 'Los Angeles FC',
        league = 'Major League Soccer',
        strengths_summary = '[실시간 로스터: Los Angeles FC (LAFC)] 2025년 여름 토트넘 10년 동행을 마치고 MLS 이적 | LW (ST, RW) | 시세 €38,000,000 | 90분당 전진액션 5.8회, 키패스 2.1회'
    WHERE player_id = 2999
""")

c.execute("""
    UPDATE market_value_history
    SET current_club = 'Los Angeles FC'
    WHERE player_id = 2999
""")

c.execute("""
    UPDATE career_discipline_and_ucl
    SET current_club = 'Los Angeles FC'
    WHERE player_id = 2999
""")

c.execute("""
    UPDATE player_playstyle_and_tendencies
    SET current_club = 'Los Angeles FC',
        loyalty_and_mobility = '토트넘 캡틴 10년 헌신 후 2025년 여름 미국 MLS Los Angeles FC(LAFC)로 전격 이적 완료'
    WHERE player_id = 2999
""")

print("2. Updating Virtual League to Test League...")
c.execute("""
    UPDATE players
    SET league = '테스트 리그 (Test League)'
    WHERE league LIKE '%Virtual%' OR league LIKE '%가상%'
""")

c.execute("""
    UPDATE managers
    SET league = '테스트 리그 (Test League)'
    WHERE league LIKE '%Virtual%' OR league LIKE '%가상%'
""")

c.execute("""
    UPDATE club_standings_and_finances
    SET competition_name = '테스트 리그 (Test League)'
    WHERE competition_name LIKE '%Virtual%' OR competition_name LIKE '%가상%'
""")

print("3. Standardizing Korean player names...")
korean_name_fixes = [
    (943, 'Jens Castrop', '옌스 카스트롭'),
    (1426, 'Hee-chan Hwang', '황희찬'),
    (1440, 'Jae-sung Lee', '이재성'),
    (1462, 'Woo-yeong Jeong', '정우영'),
]
for pid, en, ko in korean_name_fixes:
    c.execute("UPDATE players SET name = ?, name_ko = ? WHERE player_id = ?", (en, ko, pid))

print("4. Verifying foreign player names and Haaland...")
c.execute("SELECT player_id, name, current_club, league FROM players WHERE name LIKE '%Haaland%'")
haaland_rows = c.fetchall()
print(f"Haaland in players: {haaland_rows}")

c.execute("SELECT player_id, name, name_ko, current_club, league FROM players WHERE player_id = 2999")
son_row = c.fetchone()
print(f"Son in players: {son_row}")

c.execute("SELECT DISTINCT league, COUNT(*) FROM players GROUP BY league")
for r in c.fetchall():
    print("League count:", r)

c.execute("SELECT COUNT(*) FROM players WHERE current_club = 'Tottenham Hotspur FC'")
print("Tottenham Hotspur FC player count:", c.fetchone()[0])

conn.commit()
conn.close()
print("Migration completed successfully!")
