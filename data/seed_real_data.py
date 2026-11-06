"""
Seed real-world football agency dataset into SQLite (`data/agency_desk.db`).
Sources modeled after Transfermarkt (market value, contract expiry),
FBref (per-90 performance metrics & positional percentiles),
and Capology (estimated weekly wages in EUR).
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "agency_desk.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Players table (Client roster + European 5-league Peer Benchmark group)
    cur.execute(
        """
        CREATE TABLE players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            name_ko TEXT NOT NULL,
            is_agency_client INTEGER NOT NULL DEFAULT 0,
            current_club TEXT NOT NULL,
            league TEXT NOT NULL,
            position TEXT NOT NULL,
            secondary_positions TEXT,
            age INTEGER NOT NULL,
            nationality TEXT NOT NULL,
            is_eu_citizen INTEGER NOT NULL DEFAULT 0,
            contract_expires TEXT NOT NULL,
            market_value_eur INTEGER NOT NULL,
            weekly_wage_eur INTEGER NOT NULL,
            is_wage_estimated INTEGER NOT NULL DEFAULT 1,
            intl_match_pct REAL NOT NULL,
            continental_minutes_pct REAL NOT NULL,
            Domestic_minutes_pct REAL NOT NULL,
            current_league_band INTEGER NOT NULL,
            strengths_summary TEXT NOT NULL
        )
        """
    )

    # 2. Player season stats table (FBref style per-90 metrics)
    cur.execute(
        """
        CREATE TABLE player_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            season TEXT NOT NULL,
            minutes_played INTEGER NOT NULL,
            appearances INTEGER NOT NULL,
            goals_per90 REAL NOT NULL,
            assists_per90 REAL NOT NULL,
            xg_per90 REAL NOT NULL,
            xa_per90 REAL NOT NULL,
            key_passes_per90 REAL NOT NULL,
            progressive_actions_per90 REAL NOT NULL,
            defensive_duels_won_pct REAL NOT NULL,
            pos_percentile INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
        """
    )

    # 3. Club squad needs table (Transfer target clubs & incumbent starter status)
    cur.execute(
        """
        CREATE TABLE club_squad_needs (
            need_id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_name TEXT NOT NULL,
            league TEXT NOT NULL,
            country TEXT NOT NULL,
            league_band INTEGER NOT NULL,
            position TEXT NOT NULL,
            current_starter TEXT NOT NULL,
            starter_age INTEGER NOT NULL,
            starter_contract_expires TEXT NOT NULL,
            starter_weekly_wage_eur INTEGER NOT NULL,
            max_transfer_fee_budget_eur INTEGER NOT NULL,
            max_weekly_wage_offer_eur INTEGER NOT NULL,
            wage_budget_tier TEXT NOT NULL,
            non_eu_slots_free INTEGER NOT NULL,
            tactical_style TEXT NOT NULL,
            recruitment_urgency TEXT NOT NULL,
            recruitment_note TEXT NOT NULL
        )
        """
    )

    # -------------------------------------------------------------------------
    # Seed Players: 8 Korean Clients + 18 European Peer Group Players (26 total)
    # -------------------------------------------------------------------------
    players_data = [
        # --- AGENCY CLIENTS (is_agency_client = 1) ---
        (
            "Lee Kang-in", "이강인", 1, "Paris Saint-Germain", "Ligue 1", "RW", "AM,CM",
            24, "South Korea", 0, "2028-06", 30000000, 140000, 1,
            92.0, 68.0, 62.0, 1,
            "탈압박, 왼발 킥 정확도, 기회 창출(Key Passes 상위 4%), 우측 윙어 및 중앙 메짤라 멀티 소화"
        ),
        (
            "Kim Min-jae", "김민재", 1, "Bayern Munich", "Bundesliga", "CB", "LCB,RCB",
            28, "South Korea", 0, "2028-06", 45000000, 230000, 1,
            95.0, 88.0, 82.0, 1,
            "하프라인 뒷공간 커버 스피드, 전진 패스(상위 6%), 공중볼 경합 및 적극적인 대인 방어"
        ),
        (
            "Son Heung-min", "손흥민", 1, "Tottenham Hotspur", "Premier League", "LW", "ST,CF",
            32, "South Korea", 0, "2026-06", 38000000, 225000, 1,
            96.0, 85.0, 88.0, 1,
            "양발 결정력(xG 대비 실제 득점 초과 달성 상위 2%), 오프더볼 침투, 리더십 및 글로벌 상업 가치"
        ),
        (
            "Hwang Hee-chan", "황희찬", 1, "Wolverhampton Wanderers", "Premier League", "LW", "ST,RW",
            29, "South Korea", 0, "2028-06", 22000000, 82000, 1,
            88.0, 0.0, 65.0, 1,
            "박스 안 침투 타이밍, 높은 슈팅 전환율, 직선적인 드리블 돌파 및 전방 압박 에너지"
        ),
        (
            "Seol Young-woo", "설영우", 1, "Crvena Zvezda", "Serbian SuperLiga", "RB", "LB,RWB",
            26, "South Korea", 0, "2027-06", 45000000 // 10, 14000, 1,
            86.0, 90.0, 88.0, 4,
            "좌우 풀백(RB/LB) 완벽 소화, UCL 검증된 전진 패스 및 크로스, A매치 붙박이 주전(GBE 자동 통과)"
        ),
        (
            "Bae Jun-ho", "배준호", 1, "Stoke City", "EFL Championship", "LW", "AM,CM",
            21, "South Korea", 0, "2027-06", 5500000, 15000, 1,
            45.0, 0.0, 84.0, 2,
            "챔피언십 올해의 선수 선정, 좁은 공간 볼 운반(Progressive Carries 상위 8%), 반박자 빠른 전진 패스"
        ),
        (
            "Yang Min-hyuk", "양민혁", 1, "Queens Park Rangers (Loan / Tottenham)", "EFL Championship", "RW", "LW",
            19, "South Korea", 0, "2030-06", 4000000, 12000, 1,
            25.0, 0.0, 78.0, 2,
            "폭발적인 가속도와 1대1 돌파, K리그 영플레이어상 수상 후 영국 무대 적응 중, 높은 잠재 가치"
        ),
        (
            "Eom Ji-sung", "엄지성", 1, "Swansea City", "EFL Championship", "LW", "RW,AM",
            22, "South Korea", 0, "2028-06", 3200000, 11000, 1,
            35.0, 0.0, 74.0, 2,
            "인사이드 커팅 후 감아차기, 세트피스 킥력, 성실한 수비 가담 및 역습 전개"
        ),

        # --- EUROPEAN PEER BENCHMARK GROUP (is_agency_client = 0) ---
        # Peers for Lee Kang-in (RW / AM, Age 22~26, Value €25M~€45M)
        (
            "Takefusa Kubo", "쿠보 다케후사", 0, "Real Sociedad", "La Liga", "RW", "AM",
            23, "Japan", 0, "2029-06", 40000000, 48000, 1,
            85.0, 80.0, 82.0, 1, "우측면 1대1 돌파 및 찬스 메이킹"
        ),
        (
            "Brahim Diaz", "브라힘 디아스", 0, "Real Madrid", "La Liga", "RW", "AM",
            25, "Morocco", 1, "2027-06", 35000000, 140000, 1,
            75.0, 55.0, 52.0, 1, "양발 드리블 및 하프스페이스 침투"
        ),
        (
            "Francisco Conceicao", "프란시스쿠 콘세이상", 0, "Juventus", "Serie A", "RW", "LW",
            22, "Portugal", 1, "2026-06", 32000000, 88000, 1,
            60.0, 72.0, 70.0, 1, "민첩한 측면 파괴력 및 크로스"
        ),
        (
            "Harvey Elliott", "하비 엘리엇", 0, "Liverpool", "Premier League", "RW", "AM,CM",
            22, "England", 1, "2027-06", 35000000, 78000, 1,
            30.0, 50.0, 48.0, 1, "기회 창출 및 전진 패스 빈도 최상위권"
        ),
        (
            "Rayan Cherki", "라얀 셰르키", 0, "Olympique Lyonnais", "Ligue 1", "RW", "AM,LW",
            21, "France", 1, "2026-06", 30000000, 72000, 1,
            25.0, 75.0, 78.0, 1, "창의적인 스루패스와 양발 기술"
        ),

        # Peers for Kim Min-jae (CB, Age 26~30, Value €35M~€55M)
        (
            "Dayot Upamecano", "다요 우파메카노", 0, "Bayern Munich", "Bundesliga", "CB", "RCB",
            26, "France", 1, "2026-06", 45000000, 192000, 1,
            82.0, 85.0, 80.0, 1, "빠른 발과 전진 빌드업 패스"
        ),
        (
            "Cristian Romero", "크리스티안 로메로", 0, "Tottenham Hotspur", "Premier League", "CB", "RCB",
            27, "Argentina", 0, "2027-06", 55000000, 195000, 1,
            90.0, 75.0, 85.0, 1, "강력한 전진 수비와 태클 성공률"
        ),
        (
            "Fikayo Tomori", "피카요 토모리", 0, "AC Milan", "Serie A", "CB", "LCB",
            27, "England", 1, "2027-06", 32000000, 86000, 1,
            25.0, 80.0, 82.0, 1, "스피드 기반 뒷공간 커버"
        ),
        (
            "Nico Schlotterbeck", "니코 슐로터벡", 0, "Borussia Dortmund", "Bundesliga", "CB", "LCB",
            25, "Germany", 1, "2027-06", 40000000, 115000, 1,
            70.0, 90.0, 88.0, 1, "롱패스 빌드업 및 왼발 센터백"
        ),

        # Peers for Son Heung-min & Hwang Hee-chan (LW / ST, Age 27~33, Value €20M~€45M)
        (
            "Mohamed Salah", "모하메드 살라", 0, "Liverpool", "Premier League", "RW", "LW,ST",
            32, "Egypt", 0, "2026-06", 45000000, 410000, 1,
            95.0, 90.0, 92.0, 1, "EPL 최정상 득점 및 도움 생산력"
        ),
        (
            "Leandro Trossard", "레안드로 트로사르", 0, "Arsenal", "Premier League", "LW", "CF,AM",
            30, "Belgium", 1, "2026-06", 30000000, 108000, 1,
            80.0, 70.0, 68.0, 1, "박스 안 결정력과 멀티 포지션 소화"
        ),
        (
            "Kaoru Mitoma", "미토마 가오루", 0, "Brighton & Hove Albion", "Premier League", "LW", "LM",
            27, "Japan", 0, "2027-06", 40000000, 95000, 1,
            85.0, 0.0, 82.0, 1, "측면 드리블 돌파 및 공간 침투"
        ),
        (
            "Yoane Wissa", "요안 위사", 0, "Brentford", "Premier League", "LW", "ST",
            28, "DR Congo", 0, "2026-06", 28000000, 65000, 1,
            75.0, 0.0, 84.0, 1, "높은 오픈플레이 득점 전환율"
        ),

        # Peers for Seol Young-woo (RB / LB, Age 24~28, Value €4M~€12M)
        (
            "Yukinari Sugawara", "스가와라 유키나리", 0, "Southampton", "Premier League", "RB", "RWB",
            24, "Japan", 0, "2028-06", 11000000, 35000, 1,
            75.0, 0.0, 78.0, 1, "오버래핑 및 크로스 능력"
        ),
        (
            "bright Osayi-Samuel", "브라이트 오사이사무엘", 0, "Fenerbahce", "Super Lig", "RB", "RWB",
            27, "Nigeria", 0, "2025-06", 7500000, 42000, 1,
            70.0, 75.0, 80.0, 3, "폭발적인 스피드와 대인 수비"
        ),
        (
            "Anthony Caci", "앙토니 카시", 0, "Mainz 05", "Bundesliga", "RB", "LB,CB",
            27, "France", 1, "2026-06", 7000000, 28000, 1,
            0.0, 0.0, 88.0, 1, "좌우 윙백 및 스토퍼 멀티 소화"
        ),

        # Peers for Bae Jun-ho / Yang Min-hyuk / Eom Ji-sung (Young Championship/5-League Wingers)
        (
            "Wilfried Gnonto", "윌프리드 뇬토", 0, "Leeds United", "EFL Championship", "RW", "LW,AM",
            21, "Italy", 1, "2028-06", 16000000, 32000, 1,
            40.0, 0.0, 82.0, 2, "챔피언십 최상위 드리블 돌파 및 득점력"
        ),
        (
            "Jack Clarke", "잭 클라크", 0, "Ipswich Town", "Premier League", "LW", "RW",
            24, "England", 1, "2029-06", 15000000, 38000, 1,
            0.0, 0.0, 75.0, 1, "챔피언십 평정 후 EPL 진출 성공 사례"
        ),
    ]

    cur.executemany(
        """
        INSERT INTO players (
            name, name_ko, is_agency_client, current_club, league, position, secondary_positions,
            age, nationality, is_eu_citizen, contract_expires, market_value_eur, weekly_wage_eur,
            is_wage_estimated, intl_match_pct, continental_minutes_pct, Domestic_minutes_pct,
            current_league_band, strengths_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        players_data,
    )

    # Map player names to IDs for stats insertion
    cur.execute("SELECT player_id, name FROM players")
    id_map = {name: pid for pid, name in cur.fetchall()}

    # -------------------------------------------------------------------------
    # Seed Player Stats (2024-25 Season Per-90 Metrics)
    # -------------------------------------------------------------------------
    stats_data = [
        # Clients
        (id_map["Lee Kang-in"], "2024-25", 1890, 32, 0.38, 0.33, 0.29, 0.36, 2.85, 8.4, 54.0, 91),
        (id_map["Kim Min-jae"], "2024-25", 2680, 31, 0.10, 0.03, 0.08, 0.04, 0.45, 7.9, 68.5, 89),
        (id_map["Son Heung-min"], "2024-25", 2450, 30, 0.48, 0.37, 0.41, 0.34, 2.35, 6.8, 46.0, 90),
        (id_map["Hwang Hee-chan"], "2024-25", 1620, 25, 0.44, 0.17, 0.36, 0.15, 1.15, 4.9, 49.0, 78),
        (id_map["Seol Young-woo"], "2024-25", 2790, 32, 0.16, 0.26, 0.12, 0.24, 1.85, 7.6, 63.0, 88),
        (id_map["Bae Jun-ho"], "2024-25", 2610, 35, 0.14, 0.24, 0.18, 0.25, 2.10, 8.1, 52.0, 85),
        (id_map["Yang Min-hyuk"], "2024-25", 2520, 34, 0.36, 0.21, 0.31, 0.20, 1.75, 7.2, 48.0, 86),
        (id_map["Eom Ji-sung"], "2024-25", 2150, 30, 0.21, 0.25, 0.22, 0.23, 1.90, 6.7, 51.0, 80),

        # Peers
        (id_map["Takefusa Kubo"], "2024-25", 2380, 31, 0.30, 0.19, 0.27, 0.25, 2.20, 7.8, 47.0, 84),
        (id_map["Brahim Diaz"], "2024-25", 1580, 29, 0.40, 0.28, 0.33, 0.27, 2.15, 7.5, 50.0, 86),
        (id_map["Francisco Conceicao"], "2024-25", 1920, 28, 0.28, 0.24, 0.25, 0.28, 2.05, 8.2, 48.0, 83),
        (id_map["Harvey Elliott"], "2024-25", 1410, 26, 0.25, 0.38, 0.24, 0.35, 2.70, 8.0, 51.0, 87),
        (id_map["Rayan Cherki"], "2024-25", 2100, 29, 0.30, 0.42, 0.26, 0.39, 3.05, 8.9, 44.0, 92),
        (id_map["Dayot Upamecano"], "2024-25", 2540, 29, 0.07, 0.04, 0.06, 0.05, 0.50, 8.1, 66.0, 87),
        (id_map["Cristian Romero"], "2024-25", 2490, 28, 0.14, 0.04, 0.11, 0.03, 0.40, 6.9, 70.0, 90),
        (id_map["Fikayo Tomori"], "2024-25", 2410, 28, 0.08, 0.00, 0.07, 0.02, 0.30, 5.8, 65.0, 81),
        (id_map["Nico Schlotterbeck"], "2024-25", 2790, 31, 0.10, 0.13, 0.09, 0.10, 0.65, 8.3, 67.5, 89),
        (id_map["Mohamed Salah"], "2024-25", 2750, 31, 0.72, 0.45, 0.64, 0.39, 2.60, 7.4, 42.0, 98),
        (id_map["Leandro Trossard"], "2024-25", 2050, 31, 0.44, 0.22, 0.37, 0.24, 1.80, 6.1, 48.0, 84),
        (id_map["Kaoru Mitoma"], "2024-25", 2420, 29, 0.33, 0.26, 0.31, 0.25, 1.95, 8.5, 49.0, 86),
        (id_map["Yoane Wissa"], "2024-25", 2360, 29, 0.52, 0.15, 0.46, 0.14, 1.20, 4.5, 47.0, 83),
        (id_map["Yukinari Sugawara"], "2024-25", 2290, 28, 0.08, 0.16, 0.07, 0.18, 1.50, 6.2, 56.0, 74),
        (id_map["bright Osayi-Samuel"], "2024-25", 2180, 26, 0.12, 0.20, 0.10, 0.19, 1.35, 6.8, 64.0, 79),
        (id_map["Anthony Caci"], "2024-25", 2520, 29, 0.07, 0.21, 0.08, 0.20, 1.60, 6.9, 61.0, 80),
        (id_map["Wilfried Gnonto"], "2024-25", 2480, 34, 0.32, 0.25, 0.30, 0.24, 1.95, 7.9, 50.0, 86),
        (id_map["Jack Clarke"], "2024-25", 1950, 28, 0.28, 0.18, 0.26, 0.19, 1.65, 7.1, 49.0, 78),
    ]

    cur.executemany(
        """
        INSERT INTO player_stats (
            player_id, season, minutes_played, appearances, goals_per90, assists_per90,
            xg_per90, xa_per90, key_passes_per90, progressive_actions_per90,
            defensive_duels_won_pct, pos_percentile
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        stats_data,
    )

    # -------------------------------------------------------------------------
    # Seed Target Club Squad Needs (15 High-Realism European Club Openings)
    # -------------------------------------------------------------------------
    clubs_data = [
        # Target Clubs for RW / AM (Lee Kang-in, Yang Min-hyuk)
        (
            "Newcastle United", "Premier League", "England", 1, "RW",
            "Jacob Murphy", 30, "2027-06", 55000,
            45000000, 165000, "High", 99,
            "High-Intensity Transition & Half-Space Creation", "High",
            "미구엘 알미론 이탈 및 제이콥 머피(30세) 노쇠화로 확실한 왼발 인버티드 우측 윙어(RW) 보강이 구단 최우선 과제"
        ),
        (
            "Arsenal", "Premier League", "England", 1, "RW",
            "Bukayo Saka (No Backup)", 23, "2027-06", 230000,
            40000000, 160000, "High", 99,
            "Positional Play & High Pressing", "High",
            "사카의 혹사 및 부상 리스크를 분담하면서 우측 윙어와 우측 메짤라(8번/10번)를 동시에 소화할 검증된 멀티 자원 탐색 중"
        ),
        (
            "Atletico Madrid", "La Liga", "Spain", 1, "RW",
            "Marcos Llorente (Out of Position)", 30, "2027-06", 160000,
            35000000, 145000, "High", 1,
            "Compact 4-4-2 / 3-5-2 Counter & Creative Playmaking", "Medium",
            "그리즈만(34세)의 점진적 대체 및 우측 하프스페이스에서 창의적 패스를 넣어줄 왼발 플레이메이커 영입 희망 (라리가 적응 완료자 선호)"
        ),
        (
            "SSC Napoli", "Serie A", "Italy", 1, "RW",
            "Matteo Politano", 31, "2027-06", 62000,
            35000000, 130000, "Mid-High", 1,
            "Structured Direct Attack & Wing Play", "High",
            "주전 우측 윙어 폴리타노(31세)의 에이징 커브 대비 주전급 왼발 우측 윙어 영입 추진 중 (비EU 슬롯 1장 여유)"
        ),

        # Target Clubs for RB / LB (Seol Young-woo)
        (
            "West Ham United", "Premier League", "England", 1, "RB",
            "Vladimir Coufal", 32, "2025-06", 45000,
            12000000, 42000, "Mid-High", 99,
            "Balanced Fullback Play & Crossing", "High",
            "32세 주전 라이트백 쿠팔 계약 만료 임박으로 이적료 €10M 이하, 주급 €35k~40k 수준의 즉시전력감 양발 풀백 물색 중"
        ),
        (
            "Mainz 05", "Bundesliga", "Germany", 1, "RB",
            "Silvan Widmer", 32, "2026-06", 30000,
            7000000, 30000, "Mid", 99,
            "3-4-2-1 High Pressing & Wingback Overlap", "High",
            "비드머(32세) 노쇠화 및 한국 선수(이재성, 홍현석) 친화적 구단 기조로 좌우 윙백 멀티 자원 적극 검토"
        ),
        (
            "Sheffield United", "EFL Championship", "England", 2, "RB",
            "Alfie Gilchrist (Loan Expiring)", 21, "2025-06", 18000,
            6000000, 28000, "Mid", 99,
            "Overlapping Fullbacks & Direct Transition", "High",
            "임대 풀백 복귀로 인해 GBE 워크퍼밋이 즉시 발급되는 A매치 주전급 풀백 영입 필요"
        ),

        # Target Clubs for LW / AM / ST (Son Heung-min, Hwang Hee-chan, Bae Jun-ho, Eom Ji-sung)
        (
            "Tottenham Hotspur", "Premier League", "England", 1, "LW",
            "Son Heung-min", 32, "2026-06", 225000,
            50000000, 240000, "High", 99,
            "High-Line Attacking & Inverted Wingers", "High",
            "구단 주장 손흥민의 2026년 계약 만료를 앞두고 재계약(2년+옵션) vs 연장 옵션만 행사 후 세대교체 여부를 놓고 핵심 협상 진행 중"
        ),
        (
            "Borussia Dortmund", "Bundesliga", "Germany", 1, "LW",
            "Donyell Malen ( departed / rotation )", 26, "2026-06", 115000,
            28000000, 105000, "High", 99,
            "Fast Transition & Inside Forward Runs", "High",
            "측면과 최전방을 오가며 분데스리가 검증 경험이 있는 직선적인 침투형 공격수(황희찬 스타일) 또는 2선 유망주(배준호) 관심"
        ),
        (
            "Brighton & Hove Albion", "Premier League", "England", 1, "LW",
            "Kaoru Mitoma (Transfer Courted)", 27, "2027-06", 95000,
            20000000, 55000, "Mid", 99,
            "Data-Driven Moneyball & Progressive Carrying", "Medium",
            "미토마의 빅클럽 이적 대비 챔피언십에서 볼 운반(Progressive Carries) 상위 10%를 기록 중인 20대 초반 크랙(배준호/엄지성) 데이터 스카우팅 완료"
        ),
        (
            "Burnley FC", "EFL Championship", "England", 2, "RW",
            "Luca Koleosho (Injury Prone)", 20, "2029-06", 22000,
            10000000, 26000, "Mid", 99,
            "Possession & Wide 1v1 Dribbling", "High",
            "승격 경쟁 및 측면 강화를 위해 챔피언십 무대 적응력이 검증된 젊은 윙어(양민혁/엄지성) 즉시 전력 보강 추진"
        ),

        # Target Clubs for CB (Kim Min-jae)
        (
            "Bayern Munich", "Bundesliga", "Germany", 1, "CB",
            "Kim Min-jae", 28, "2028-06", 230000,
            60000000, 250000, "High", 99,
            "Ultra High-Line Possession (Kompany System)", "Medium",
            "콤파니 감독의 극단적 하이라인 전술에서 핵심 센터백으로 활약 중이나 출전 혹사 관리 및 성과 보너스 재조정 이슈 존재"
        ),
        (
            "Inter Milan", "Serie A", "Italy", 1, "CB",
            "Francesco Acerbi", 37, "2026-06", 55000,
            40000000, 175000, "High", 1,
            "3-5-2 Elite Defensive Organization", "High",
            "37세 아체르비와 33세 데 브리 노쇠화로 세리에A 최고 수비수 출신(김민재)에 대한 지속적인 복귀/임대 후 완전이적 타진"
        ),
    ]

    cur.executemany(
        """
        INSERT INTO club_squad_needs (
            club_name, league, country, league_band, position,
            current_starter, starter_age, starter_contract_expires, starter_weekly_wage_eur,
            max_transfer_fee_budget_eur, max_weekly_wage_offer_eur, wage_budget_tier,
            non_eu_slots_free, tactical_style, recruitment_urgency, recruitment_note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        clubs_data,
    )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Initialized {DB_PATH} with {len(players_data)} players and {len(clubs_data)} target club profiles.")


if __name__ == "__main__":
    init_db()
