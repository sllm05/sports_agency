import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

virtual_teams_standings = [
    ('VL', '테스트/가상 리그 (Virtual League)', '네오 뮌헨 FC', 1, 10, 8, 1, 1, 25, 24, 8, 16, 'W-W-W-D-W', '네오 아레나 (Neo Arena)', 55000, '€+15.00m', 60.0, 12),
    ('VL', '테스트/가상 리그 (Virtual League)', '메트로폴리스 FC', 2, 10, 7, 2, 1, 23, 21, 9, 12, 'W-W-D-W-W', '메트로 스타디움', 62000, '€+22.00m', 55.0, 14),
    ('VL', '테스트/가상 리그 (Virtual League)', '솔라리스 시티 FC', 3, 10, 6, 2, 2, 20, 19, 11, 8, 'W-D-W-L-W', '솔라리스 돔', 48000, '€+8.00m', 50.0, 10),
    ('VL', '테스트/가상 리그 (Virtual League)', '루미나르 SC', 4, 10, 5, 3, 2, 18, 17, 12, 5, 'D-W-D-W-L', '스타드 드 루미나르', 42000, '€+10.00m', 65.0, 9),
    ('VL', '테스트/가상 리그 (Virtual League)', '아발론 유나이티드', 5, 10, 4, 3, 3, 15, 15, 14, 1, 'L-W-D-W-D', '아발론 그라운드', 38000, '€+5.00m', 45.0, 8),
    ('VL', '테스트/가상 리그 (Virtual League)', '한양 시티 FC', 6, 10, 4, 2, 4, 14, 14, 15, -1, 'W-L-L-W-D', '한양 월드컵 경기장', 66000, '€+12.00m', 40.0, 11),
    ('VL', '테스트/가상 리그 (Virtual League)', '아틀라스 FC', 7, 10, 3, 2, 5, 11, 12, 18, -6, 'L-L-W-D-L', '에스타디오 아틀라스', 40000, '€+4.00m', 58.0, 7),
    ('VL', '테스트/가상 리그 (Virtual League)', '호라이즌 로버스', 8, 10, 2, 1, 7, 7, 9, 22, -13, 'L-L-L-D-W', '호라이즌 파크', 35000, '€+2.00m', 52.0, 6),
]

c.execute("DELETE FROM club_standings_and_finances WHERE competition_code = 'VL'")
for team in virtual_teams_standings:
    c.execute("""
    INSERT INTO club_standings_and_finances (
        competition_code, competition_name, club_name, rank_position, played_games,
        won, draw, lost, points, goals_for, goals_against, goal_difference,
        form, stadium_name, stadium_seats, net_transfer_record, foreigners_pct, national_team_players
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, team)

conn.commit()
print("Inserted virtual standings successfully!")
