import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

# 1. Unify real clubs
c.execute("UPDATE players SET current_club = 'Manchester City FC' WHERE current_club = 'Manchester City'")
c.execute("UPDATE players SET current_club = 'Tottenham Hotspur FC' WHERE current_club = 'Tottenham Hotspur'")
c.execute("UPDATE players SET current_club = 'FC Bayern München', league = 'Bundesliga' WHERE current_club = 'FC 바이에른 뮌헨'")

c.execute("UPDATE market_value_history SET current_club = 'Tottenham Hotspur FC' WHERE current_club = 'Tottenham Hotspur'")
c.execute("UPDATE career_discipline_and_ucl SET current_club = 'Tottenham Hotspur FC' WHERE current_club = 'Tottenham Hotspur'")
c.execute("UPDATE player_playstyle_and_tendencies SET current_club = 'Tottenham Hotspur FC' WHERE current_club = 'Tottenham Hotspur'")

# 2. Virtual League constant
VIRTUAL_LEAGUE = '테스트/가상 리그 (Virtual League)'

# Update existing virtual players (excluding Jeong Sang-bin 90011)
c.execute("""
UPDATE players 
SET league = ? 
WHERE player_id >= 90001 AND player_id <= 90010
""", (VIRTUAL_LEAGUE,))

# Assign Kevin Yoon to Atlas FC so every virtual club has active roster
c.execute("""
UPDATE players 
SET current_club = '아틀라스 FC', league = ? 
WHERE player_id = 90010
""", (VIRTUAL_LEAGUE,))

# 3. Setup Virtual Managers in managers table
virtual_managers_data = [
    (90101, 'Jin-hyuk Kim', '한양 시티 FC', VIRTUAL_LEAGUE, 'South Korea', 44, 'South Korea', 1, '2027-06', '4-3-3', '4-2-3-1', '4-3-3 (120경기), 4-2-3-1 (45경기)', 165, 58.2, 1.82, 1.95, 1.15, 'Jin-hyuk Kim | 한양 시티 FC 지휘관 · 콤팩트 프레싱 기반 전환 속공 전술', 0, 15000, 82, 80, 85, 78, 81, '전방 압박과 수비 안정화에 능한 한국형 실리주의 전술가', '{}', '김진혁', 0),
    (90102, 'Marco Valenti', '솔라리스 시티 FC', VIRTUAL_LEAGUE, 'Italy', 49, 'Italy', 1, '2026-06', '3-5-2', '3-4-2-1', '3-5-2 (180경기), 3-4-2-1 (60경기)', 240, 61.5, 1.88, 1.80, 0.95, 'Marco Valenti | 솔라리스 시티 FC 감독 · 이탈리안 백3 카테나치오 및 윙백 오버래핑', 0, 18000, 85, 83, 86, 82, 84, '단단한 3백 조직력과 빠른 윙백 기동성을 극대화하는 이탈리아 명장', '{}', '마르코 발렌티', 0),
    (90103, 'Sebastian Schneider', '메트로폴리스 FC', VIRTUAL_LEAGUE, 'Germany', 46, 'Germany', 1, '2027-12', '4-2-3-1', '4-3-3', '4-2-3-1 (210경기)', 210, 64.0, 1.94, 2.10, 1.05, 'Sebastian Schneider | 메트로폴리스 FC 총감독 · 분데스 스타일 하이 인텐시티 게겐프레싱', 0, 22000, 87, 85, 88, 84, 86, '데이터 기반 하이 라인 전방 압박 및 볼 탈취 후 6초 내 슈팅 메커니즘', '{}', '세바스티안 슈나이더', 0),
    (90104, 'Hans-Peter Weber', '네오 뮌헨 FC', VIRTUAL_LEAGUE, 'Germany', 52, 'Germany', 1, '2028-06', '4-3-3 Attacking', '4-2-3-1', '4-3-3 (310경기)', 310, 66.5, 2.05, 2.25, 0.90, 'Hans-Peter Weber | 네오 뮌헨 FC 사령탑 · 포지셔널 플레이 및 전방위 빌드업 전술', 0, 25000, 88, 86, 89, 87, 88, '중원 지배와 공간 창출을 극대화하는 독일 베테랑 사령탑', '{}', '한스-페터 베버', 0),
    (90105, 'Laurent Blanc Jr.', '루미나르 SC', VIRTUAL_LEAGUE, 'France', 45, 'France', 1, '2027-06', '4-3-3', '4-4-2 Diamond', '4-3-3 (150경기)', 150, 59.0, 1.80, 1.85, 1.10, 'Laurent Blanc Jr. | 루미나르 SC 감독 · 프렌치 테크니컬 점유율 축구', 0, 16000, 83, 82, 84, 80, 82, '짧은 패스 워크와 유기적인 스위칭 플레이를 강조하는 테크니컬 감독', '{}', '로랑 블랑 주니어', 0),
    (90106, 'Arthur King', '아발론 유나이티드', VIRTUAL_LEAGUE, 'England', 48, 'England', 1, '2026-12', '4-4-2', '4-2-3-1', '4-4-2 (230경기)', 230, 57.5, 1.76, 1.70, 1.15, 'Arthur King | 아발론 유나이티드 사령탑 · 전통 브리티시 다이렉트 풋볼 및 세트피스 특화', 0, 17000, 82, 81, 83, 79, 80, '강력한 신체 조건과 빠른 측면 크로스 공격을 선호하는 잉글랜드 사령탑', '{}', '아서 킹', 0),
    (90107, 'Erik Thornqvist', '호라이즌 로버스', VIRTUAL_LEAGUE, 'Sweden', 47, 'Sweden', 1, '2027-06', '3-4-3', '3-5-2', '3-4-3 (140경기)', 140, 58.5, 1.79, 1.75, 1.08, 'Erik Thornqvist | 호라이즌 로버스 감독 · 북유럽식 피지컬 압박과 속공 역습', 0, 15500, 81, 80, 82, 79, 81, '강력한 수비 블록과 직선적인 전진 패스를 무기로 삼는 북유럽 전술가', '{}', '에릭 토른크비스트', 0),
    (90108, 'Gabriel Santos', '아틀라스 FC', VIRTUAL_LEAGUE, 'Spain', 43, 'Spain', 1, '2028-06', '4-2-3-1', '4-3-3', '4-2-3-1 (175경기)', 175, 62.0, 1.90, 2.00, 1.02, 'Gabriel Santos | 아틀라스 FC 감독 · 라틴식 하프스페이스 공략과 기술적 빌드업', 0, 19000, 84, 84, 85, 82, 83, '스페인식 볼 점유율 축구와 창의적인 미드필더 전술 운용의 전문가', '{}', '가브리엘 산토스', 0),
]

for m in virtual_managers_data:
    c.execute("""
    INSERT OR REPLACE INTO managers (
        manager_id, name, current_club, league, country, age, nationality,
        is_eu_citizen, contract_expires, preferred_formation, secondary_formation,
        top_formations_summary, games_analyzed, win_rate_pct, points_per_game,
        avg_goals_for, avg_goals_against, tactical_style, estimated_buyout_eur,
        weekly_wage_eur, tactical_flexibility_score, attacking_coaching_score,
        defensive_coaching_score, youth_trust_score, in_game_management_score,
        leadership_personality, preferred_player_profiles_json, name_ko, is_agency_client
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, m)

# 4. Insert/Update virtual managers into players table as position='MGR'
for m in virtual_managers_data:
    mgr_id, name, club, league, nat, age = m[0], m[1], m[2], m[3], m[4], m[5]
    name_ko = m[27]
    pref_form = m[9]
    wage = m[19]
    name_full = f"{name} (감독)"
    name_ko_full = f"{name_ko} (감독)"
    c.execute("""
    INSERT OR REPLACE INTO players (
        player_id, name, name_ko, is_agency_client, current_club, league, position,
        secondary_positions, age, nationality, is_eu_citizen, contract_expires,
        market_value_eur, weekly_wage_eur, is_wage_estimated, intl_match_pct,
        continental_minutes_pct, Domestic_minutes_pct, current_league_band, strengths_summary
    ) VALUES (?, ?, ?, ?, ?, ?, 'MGR', ?, ?, ?, 1, '2027-06', ?, ?, 1, 60.0, 50.0, 90.0, 2, ?)
    """, (
        mgr_id, name_full, name_ko_full, 0, club, league,
        pref_form, age, nat, wage * 52 * 3, wage,
        f"[테스트/가상 리그 감독: {club}] {name_ko} ({name}) | 선호 포메이션: {pref_form}"
    ))

conn.commit()
print("Migration completed successfully!")
