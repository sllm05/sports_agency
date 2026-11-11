# -*- coding: utf-8 -*-
"""
Seed Test League (테스트 리그) with virtual test players and managers
Designed for user testing of scouting, DataMB peer comparison, recruitment deal memos, and contract signing.
"""
import sqlite3
import json

DB_PATH = "data/agency_desk.db"

def seed_test_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Cleaning any existing test records (ID >= 90000)...")
    cur.execute("DELETE FROM players WHERE player_id >= 90000")
    cur.execute("DELETE FROM player_stats WHERE player_id >= 90000")
    cur.execute("DELETE FROM market_value_history WHERE player_id >= 90000")
    cur.execute("DELETE FROM player_playstyle_and_tendencies WHERE player_id >= 90000")
    cur.execute("DELETE FROM managers WHERE manager_id >= 90000")
    cur.execute("DELETE FROM agency_recruitment_targets WHERE target_id >= 90000")
    cur.execute("DELETE FROM agency_contracts WHERE client_id >= 90000")

    # 1. TEST PLAYERS
    test_players = [
        {
            "player_id": 90001,
            "name": "Leo Park",
            "name_ko": "박레오",
            "is_agency_client": 0,
            "current_club": "한양 시티 FC",
            "league": "테스트 리그 (Test League)",
            "position": "ST",
            "secondary_positions": "CF, LW",
            "age": 20,
            "nationality": "South Korea",
            "is_eu_citizen": 0,
            "contract_expires": "2027-06-30",
            "market_value_eur": 15000000,
            "weekly_wage_eur": 25000,
            "is_wage_estimated": 0,
            "intl_match_pct": 55.0,
            "continental_minutes_pct": 60.0,
            "Domestic_minutes_pct": 85.0,
            "current_league_band": 2,
            "strengths_summary": "폭발적인 가속도와 양발 슈팅 결정력. 오프더볼 침투와 전방 압박 능력이 뛰어난 한국형 컴플리트 포워드 유망주.",
            "estimated_buyout_eur": 35000000,
            "cies_fair_value_min_eur": 13500000,
            "cies_fair_value_avg_eur": 16200000,
            "cies_fair_value_max_eur": 19800000,
            "experience_capital_score": 78.5,
            "impact_score": 82.0,
            # stats
            "minutes_played": 1850,
            "appearances": 22,
            "goals_per90": 0.68,
            "assists_per90": 0.24,
            "xg_per90": 0.62,
            "xa_per90": 0.20,
            "key_passes_per90": 1.45,
            "progressive_actions_per90": 4.8,
            "defensive_duels_won_pct": 48.0,
            "pos_percentile": 88,
            "xt_expected_threat": 0.28,
            "direct_speed_mps": 2.4,
            "shot_conversion_pct": 21.5,
            "touches_in_box_per90": 6.8,
            # playstyle
            "tactical_archetype": "Advanced Forward / Poacher",
            "strengths_tags": "양발 결정력, 박스 침투, 민첩성, 스프린트",
            "weaknesses_tags": "공중볼 경합, 연계 플레이",
            "height_cm": 183,
            "preferred_foot": "Both"
        },
        {
            "player_id": 90002,
            "name": "David Han",
            "name_ko": "한다윗",
            "is_agency_client": 0,
            "current_club": "한양 시티 FC",
            "league": "테스트 리그 (Test League)",
            "position": "CM",
            "secondary_positions": "DM, AM",
            "age": 22,
            "nationality": "South Korea",
            "is_eu_citizen": 0,
            "contract_expires": "2028-06-30",
            "market_value_eur": 12000000,
            "weekly_wage_eur": 20000,
            "is_wage_estimated": 0,
            "intl_match_pct": 45.0,
            "continental_minutes_pct": 50.0,
            "Domestic_minutes_pct": 90.0,
            "current_league_band": 2,
            "strengths_summary": "탈압박과 전진 패스 시야가 독보적인 플레이메이커. 경기 템포 조율과 전진 드리블 능력 우수.",
            "estimated_buyout_eur": 28000000,
            "cies_fair_value_min_eur": 10500000,
            "cies_fair_value_avg_eur": 12800000,
            "cies_fair_value_max_eur": 15400000,
            "experience_capital_score": 75.0,
            "impact_score": 80.5,
            # stats
            "minutes_played": 2100,
            "appearances": 25,
            "goals_per90": 0.18,
            "assists_per90": 0.38,
            "xg_per90": 0.15,
            "xa_per90": 0.32,
            "key_passes_per90": 2.65,
            "progressive_actions_per90": 7.2,
            "defensive_duels_won_pct": 58.5,
            "pos_percentile": 85,
            "xt_expected_threat": 0.34,
            "direct_speed_mps": 1.8,
            "shot_conversion_pct": 12.0,
            "touches_in_box_per90": 2.4,
            # playstyle
            "tactical_archetype": "Deep-Lying Playmaker / Mezzala",
            "strengths_tags": "탈압박, 전진패스, 시야, 롱패스",
            "weaknesses_tags": "피지컬 몸싸움, 제공권",
            "height_cm": 178,
            "preferred_foot": "Right"
        },
        {
            "player_id": 90003,
            "name": "Marcus Vance",
            "name_ko": "마커스 밴스",
            "is_agency_client": 0,
            "current_club": "메트로폴리스 FC",
            "league": "테스트 리그 (Test League)",
            "position": "CB",
            "secondary_positions": "DM",
            "age": 24,
            "nationality": "England",
            "is_eu_citizen": 0,
            "contract_expires": "2027-06-30",
            "market_value_eur": 18000000,
            "weekly_wage_eur": 35000,
            "is_wage_estimated": 0,
            "intl_match_pct": 20.0,
            "continental_minutes_pct": 40.0,
            "Domestic_minutes_pct": 92.0,
            "current_league_band": 2,
            "strengths_summary": "192cm의 압도적인 공중볼 장악력과 1대1 대인 방어. 후방 롱패스 빌드업에 능한 잉글랜드 정통 센터백.",
            "estimated_buyout_eur": 40000000,
            "cies_fair_value_min_eur": 16000000,
            "cies_fair_value_avg_eur": 19000000,
            "cies_fair_value_max_eur": 23000000,
            "experience_capital_score": 81.0,
            "impact_score": 83.5,
            # stats
            "minutes_played": 2350,
            "appearances": 27,
            "goals_per90": 0.08,
            "assists_per90": 0.04,
            "xg_per90": 0.07,
            "xa_per90": 0.03,
            "key_passes_per90": 0.45,
            "progressive_actions_per90": 3.8,
            "defensive_duels_won_pct": 74.8,
            "pos_percentile": 84,
            "xt_expected_threat": 0.12,
            "direct_speed_mps": 1.5,
            "shot_conversion_pct": 8.0,
            "touches_in_box_per90": 1.2,
            # playstyle
            "tactical_archetype": "Ball-Playing Defender",
            "strengths_tags": "제공권, 대인마크, 가로채기, 롱볼빌드업",
            "weaknesses_tags": "순간 가속도, 민첩성",
            "height_cm": 192,
            "preferred_foot": "Right"
        },
        {
            "player_id": 90004,
            "name": "Lucas Silva",
            "name_ko": "루카스 실바",
            "is_agency_client": 0,
            "current_club": "솔라리스 시티 FC",
            "league": "테스트 리그 (Test League)",
            "position": "RW",
            "secondary_positions": "LW, AM",
            "age": 19,
            "nationality": "Brazil",
            "is_eu_citizen": 0,
            "contract_expires": "2028-06-30",
            "market_value_eur": 22000000,
            "weekly_wage_eur": 30000,
            "is_wage_estimated": 0,
            "intl_match_pct": 30.0,
            "continental_minutes_pct": 55.0,
            "Domestic_minutes_pct": 80.0,
            "current_league_band": 2,
            "strengths_summary": "화려한 삼바 드리블과 1대1 돌파, 컷인 슈팅이 위협적인 브라질 인버티드 윙어 원더키드.",
            "estimated_buyout_eur": 50000000,
            "cies_fair_value_min_eur": 20000000,
            "cies_fair_value_avg_eur": 24000000,
            "cies_fair_value_max_eur": 29000000,
            "experience_capital_score": 76.0,
            "impact_score": 86.0,
            # stats
            "minutes_played": 1680,
            "appearances": 20,
            "goals_per90": 0.48,
            "assists_per90": 0.42,
            "xg_per90": 0.44,
            "xa_per90": 0.38,
            "key_passes_per90": 2.2,
            "progressive_actions_per90": 8.5,
            "defensive_duels_won_pct": 42.0,
            "pos_percentile": 91,
            "xt_expected_threat": 0.42,
            "direct_speed_mps": 2.8,
            "shot_conversion_pct": 18.0,
            "touches_in_box_per90": 5.8,
            # playstyle
            "tactical_archetype": "Inverted Winger / Trickster",
            "strengths_tags": "드리블 성공률, 컷인 슈팅, 기회창출, 순간가속",
            "weaknesses_tags": "수비 가담, 피지컬 경합",
            "height_cm": 175,
            "preferred_foot": "Left"
        },
        {
            "player_id": 90005,
            "name": "Alexandre Dubois",
            "name_ko": "알렉상드르 뒤부아",
            "is_agency_client": 0,
            "current_club": "네오 뮌헨 FC",
            "league": "테스트 리그 (Test League)",
            "position": "LB",
            "secondary_positions": "LWB, LM",
            "age": 23,
            "nationality": "France",
            "is_eu_citizen": 1,
            "contract_expires": "2027-06-30",
            "market_value_eur": 14000000,
            "weekly_wage_eur": 28000,
            "is_wage_estimated": 0,
            "intl_match_pct": 15.0,
            "continental_minutes_pct": 65.0,
            "Domestic_minutes_pct": 88.0,
            "current_league_band": 2,
            "strengths_summary": "폭발적인 오버래핑과 정교한 왼발 크로스 능력. 왕성한 활동량으로 공수를 오가는 프랑스 공격형 풀백.",
            "estimated_buyout_eur": 32000000,
            "cies_fair_value_min_eur": 12500000,
            "cies_fair_value_avg_eur": 14800000,
            "cies_fair_value_max_eur": 17500000,
            "experience_capital_score": 79.0,
            "impact_score": 81.0,
            # stats
            "minutes_played": 2050,
            "appearances": 24,
            "goals_per90": 0.09,
            "assists_per90": 0.31,
            "xg_per90": 0.08,
            "xa_per90": 0.28,
            "key_passes_per90": 1.85,
            "progressive_actions_per90": 6.5,
            "defensive_duels_won_pct": 64.0,
            "pos_percentile": 82,
            "xt_expected_threat": 0.26,
            "direct_speed_mps": 2.2,
            "shot_conversion_pct": 10.0,
            "touches_in_box_per90": 2.1,
            # playstyle
            "tactical_archetype": "Attacking Wing-Back",
            "strengths_tags": "크로스, 오버래핑, 스태미너, 전진 패스",
            "weaknesses_tags": "배후 공간 수비",
            "height_cm": 180,
            "preferred_foot": "Left"
        },
        {
            "player_id": 90006,
            "name": "Jan Novak",
            "name_ko": "얀 노바크",
            "is_agency_client": 0,
            "current_club": "메트로폴리스 FC",
            "league": "테스트 리그 (Test League)",
            "position": "GK",
            "secondary_positions": "",
            "age": 25,
            "nationality": "Czech Republic",
            "is_eu_citizen": 1,
            "contract_expires": "2027-06-30",
            "market_value_eur": 10000000,
            "weekly_wage_eur": 18000,
            "is_wage_estimated": 0,
            "intl_match_pct": 40.0,
            "continental_minutes_pct": 50.0,
            "Domestic_minutes_pct": 95.0,
            "current_league_band": 2,
            "strengths_summary": "초인적인 반사신경과 1대1 슈팅 방어, 페널티킥 선방에 특화된 체코 국가대표 주전 골키퍼.",
            "estimated_buyout_eur": 25000000,
            "cies_fair_value_min_eur": 9000000,
            "cies_fair_value_avg_eur": 11000000,
            "cies_fair_value_max_eur": 13500000,
            "experience_capital_score": 82.0,
            "impact_score": 84.0,
            # stats
            "minutes_played": 2520,
            "appearances": 28,
            "goals_per90": 0.0,
            "assists_per90": 0.0,
            "xg_per90": 0.0,
            "xa_per90": 0.0,
            "key_passes_per90": 0.1,
            "progressive_actions_per90": 1.2,
            "defensive_duels_won_pct": 72.0,
            "pos_percentile": 80,
            "xt_expected_threat": 0.02,
            "direct_speed_mps": 0.5,
            "shot_conversion_pct": 0.0,
            "touches_in_box_per90": 0.0,
            # playstyle
            "tactical_archetype": "Shot-Stopper / Modern Sweeper Keeper",
            "strengths_tags": "반사신경, 1대1 선방, 공중볼 캐칭, PK 방어",
            "weaknesses_tags": "발밑 패스 정확도",
            "height_cm": 190,
            "preferred_foot": "Right"
        },
        {
            "player_id": 90101,
            "name": "Jin-hyuk Kim (감독)",
            "name_ko": "김진혁 (감독)",
            "is_agency_client": 0,
            "current_club": "한양 시티 FC",
            "league": "테스트 리그 (Test League)",
            "position": "MGR",
            "secondary_positions": "4-2-3-1",
            "age": 48,
            "nationality": "South Korea",
            "is_eu_citizen": 0,
            "contract_expires": "2026-06-30",
            "market_value_eur": 3500000,
            "weekly_wage_eur": 45000,
            "is_wage_estimated": 0,
            "intl_match_pct": 0.0,
            "continental_minutes_pct": 0.0,
            "Domestic_minutes_pct": 100.0,
            "current_league_band": 2,
            "strengths_summary": "[사령탑: 한양 시티 FC] 주포메이션 4-2-3-1 (보조 4-3-3) · 실측 120경기 승률 62.5% (PPG 2.08) · 게겐프레싱 & 고강도 전환 빌드업",
            "estimated_buyout_eur": 3500000,
            "cies_fair_value_min_eur": 3000000,
            "cies_fair_value_avg_eur": 3500000,
            "cies_fair_value_max_eur": 4200000,
            "experience_capital_score": 85.0,
            "impact_score": 90.0,
            # stats
            "minutes_played": 10800,
            "appearances": 120,
            "goals_per90": 2.1,
            "assists_per90": 0.0,
            "xg_per90": 2.08,
            "xa_per90": 0.0,
            "key_passes_per90": 0.0,
            "progressive_actions_per90": 0.0,
            "defensive_duels_won_pct": 62.5,
            "pos_percentile": 63,
            "xt_expected_threat": 0.0,
            "direct_speed_mps": 0.0,
            "shot_conversion_pct": 0.0,
            "touches_in_box_per90": 0.0,
            # playstyle
            "tactical_archetype": "Gegenpressing Tactical Innovator",
            "strengths_tags": "게겐프레싱, 전환 빌드업, 유망주 기용, 라커룸 장악",
            "weaknesses_tags": "로테이션 부족",
            "height_cm": 181,
            "preferred_foot": "Right"
        },
        {
            "player_id": 90102,
            "name": "Sebastian Kurz (감독)",
            "name_ko": "제바스티안 쿠르츠 (감독)",
            "is_agency_client": 0,
            "current_club": "네오 뮌헨 FC",
            "league": "테스트 리그 (Test League)",
            "position": "MGR",
            "secondary_positions": "3-4-2-1",
            "age": 42,
            "nationality": "Germany",
            "is_eu_citizen": 1,
            "contract_expires": "2027-06-30",
            "market_value_eur": 4000000,
            "weekly_wage_eur": 50000,
            "is_wage_estimated": 0,
            "intl_match_pct": 0.0,
            "continental_minutes_pct": 0.0,
            "Domestic_minutes_pct": 100.0,
            "current_league_band": 2,
            "strengths_summary": "[사령탑: 네오 뮌헨 FC] 주포메이션 3-4-2-1 (보조 3-5-2) · 실측 95경기 승률 58.3% (PPG 1.95) · 하프스페이스 오버로드 & 포지셔널 플레이",
            "estimated_buyout_eur": 4000000,
            "cies_fair_value_min_eur": 3500000,
            "cies_fair_value_avg_eur": 4000000,
            "cies_fair_value_max_eur": 4800000,
            "experience_capital_score": 83.0,
            "impact_score": 88.0,
            # stats
            "minutes_played": 8550,
            "appearances": 95,
            "goals_per90": 1.9,
            "assists_per90": 0.0,
            "xg_per90": 1.95,
            "xa_per90": 0.0,
            "key_passes_per90": 0.0,
            "progressive_actions_per90": 0.0,
            "defensive_duels_won_pct": 58.3,
            "pos_percentile": 58,
            "xt_expected_threat": 0.0,
            "direct_speed_mps": 0.0,
            "shot_conversion_pct": 0.0,
            "touches_in_box_per90": 0.0,
            # playstyle
            "tactical_archetype": "Positional Play Strategist",
            "strengths_tags": "포지셔널 플레이, 하프스페이스 공략, 수비 조직력",
            "weaknesses_tags": "플랜 B 부재",
            "height_cm": 184,
            "preferred_foot": "Right"
        }
    ]

    for p in test_players:
        cur.execute("""
            INSERT INTO players (
                player_id, name, name_ko, is_agency_client, current_club, league,
                position, secondary_positions, age, nationality, is_eu_citizen,
                contract_expires, market_value_eur, weekly_wage_eur, is_wage_estimated,
                intl_match_pct, continental_minutes_pct, Domestic_minutes_pct, current_league_band,
                strengths_summary, is_injured, estimated_buyout_eur, cies_fair_value_min_eur,
                cies_fair_value_avg_eur, cies_fair_value_max_eur, experience_capital_score, impact_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?)
        """, (
            p["player_id"], p["name"], p["name_ko"], p["is_agency_client"], p["current_club"], p["league"],
            p["position"], p["secondary_positions"], p["age"], p["nationality"], p["is_eu_citizen"],
            p["contract_expires"], p["market_value_eur"], p["weekly_wage_eur"], p["is_wage_estimated"],
            p["intl_match_pct"], p["continental_minutes_pct"], p["Domestic_minutes_pct"], p["current_league_band"],
            p["strengths_summary"], p["estimated_buyout_eur"], p["cies_fair_value_min_eur"],
            p["cies_fair_value_avg_eur"], p["cies_fair_value_max_eur"], p["experience_capital_score"], p["impact_score"]
        ))

        cur.execute("""
            INSERT INTO player_stats (
                player_id, season, minutes_played, appearances, goals_per90, assists_per90,
                xg_per90, xa_per90, key_passes_per90, progressive_actions_per90,
                defensive_duels_won_pct, pos_percentile, xt_expected_threat, direct_speed_mps,
                shot_conversion_pct, touches_in_box_per90
            ) VALUES (?, '25/26', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["player_id"], p["minutes_played"], p["appearances"], p["goals_per90"], p["assists_per90"],
            p["xg_per90"], p["xa_per90"], p["key_passes_per90"], p["progressive_actions_per90"],
            p["defensive_duels_won_pct"], p["pos_percentile"], p["xt_expected_threat"], p["direct_speed_mps"],
            p["shot_conversion_pct"], p["touches_in_box_per90"]
        ))

        cur.execute("""
            INSERT INTO market_value_history (
                player_id, player_name, current_club, current_market_value_eur,
                highest_market_value_eur, peak_date, previous_market_value_eur,
                valuation_change_pct, height_cm, preferred_foot, international_caps,
                international_goals, agency_name, recent_history_json
            ) VALUES (?, ?, ?, ?, ?, '2025-01-01', ?, 25.0, ?, ?, 8, 3, '자유 계약 (FA/협상 중)', '[]')
        """, (
            p["player_id"], p["name"], p["current_club"], p["market_value_eur"],
            p["market_value_eur"], int(p["market_value_eur"] * 0.8), p["height_cm"], p["preferred_foot"]
        ))

        cur.execute("""
            INSERT INTO player_playstyle_and_tendencies (
                player_id, player_name, current_club, position, tactical_archetype,
                strengths_tags, weaknesses_tags, progression_tendency, finishing_clinicality,
                temperament_and_discipline, loyalty_and_mobility, big_game_and_leadership,
                starter_ratio_pct, minutes_availability_pct, durability_and_availability_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, '전진 침투형', '상위 10%', '프로페셔널', '유럽 진출 선호', '클러치 기질', 92.0, 95.0, '완벽한 피지컬 상태 유지')
        """, (
            p["player_id"], p["name"], p["current_club"], p["position"], p["tactical_archetype"],
            p["strengths_tags"], p["weaknesses_tags"]
        ))

    print(f"Successfully seeded {len(test_players)} virtual test players.")

    # 2. TEST MANAGERS
    sample_profiles_json = json.dumps({
        "ST": "최전방 압박 리더이자 박스 안 결정력(xG/90)과 연계(xAG)를 겸비한 완성형 9번",
        "LW": "터치라인 폭을 넓히거나 안쪽으로 파고들어 1대1 돌파·슈팅을 마무리하는 인버티드 윙어",
        "RW": "빠른 전환 스피드와 컷인 슈팅/키패스 생산력이 높은 우측 크랙형 윙어",
        "AM": "상대 포켓 공간(Half-space)에서 라인 브레이킹 패스를 공급하는 공격형 메짤라",
        "CM": "높은 위치에서 압박과 볼 순환, 박스 타격을 동시에 수행하는 하이브리드 8번",
        "DM": "단독 6번으로서 탈압박, 전진 패스, 역습 저지 능력이 최상급인 홀딩 미드필더",
        "CB": "높은 수비라인 뒷공간 커버와 빌드업 패스 성공률이 높은 볼플레잉 센터백",
        "RB": "중원 숫자 싸움에 가담하는 인버티드 풀백 또는 오버래핑 풀백",
        "LB": "빌드업 시 3백 형성 또는 중원 합류가 가능한 전술 지능형 좌측 풀백"
    }, ensure_ascii=False)

    test_managers = [
        {
            "manager_id": 90001,
            "name": "Jin-hyuk Kim",
            "name_ko": "김진혁 (감독)",
            "is_agency_client": 0,
            "current_club": "한양 시티 FC",
            "league": "테스트 리그 (Test League)",
            "country": "South Korea",
            "age": 48,
            "nationality": "South Korea",
            "is_eu_citizen": 0,
            "contract_expires": "2026-06-30",
            "preferred_formation": "4-2-3-1",
            "secondary_formation": "4-3-3",
            "top_formations_summary": "4-2-3-1 (65%), 4-3-3 (35%)",
            "games_analyzed": 120,
            "win_rate_pct": 62.5,
            "points_per_game": 2.08,
            "avg_goals_for": 2.1,
            "avg_goals_against": 0.95,
            "tactical_style": "게겐프레싱 & 고강도 전환 빌드업",
            "estimated_buyout_eur": 3500000,
            "weekly_wage_eur": 45000,
            "tactical_flexibility_score": 88,
            "attacking_coaching_score": 91,
            "defensive_coaching_score": 86,
            "youth_trust_score": 93,
            "in_game_management_score": 87,
            "leadership_personality": "카리스마적 전술 혁신가, 적극적 소통형 라커룸 장악"
        },
        {
            "manager_id": 90002,
            "name": "Sebastian Kurz",
            "name_ko": "제바스티안 쿠르츠 (감독)",
            "is_agency_client": 0,
            "current_club": "네오 뮌헨 FC",
            "league": "테스트 리그 (Test League)",
            "country": "Germany",
            "age": 42,
            "nationality": "Germany",
            "is_eu_citizen": 1,
            "contract_expires": "2027-06-30",
            "preferred_formation": "3-4-2-1",
            "secondary_formation": "3-5-2",
            "top_formations_summary": "3-4-2-1 (70%), 3-5-2 (30%)",
            "games_analyzed": 95,
            "win_rate_pct": 58.3,
            "points_per_game": 1.95,
            "avg_goals_for": 1.9,
            "avg_goals_against": 1.05,
            "tactical_style": "하프스페이스 오버로드 & 포지셔널 플레이",
            "estimated_buyout_eur": 4000000,
            "weekly_wage_eur": 50000,
            "tactical_flexibility_score": 92,
            "attacking_coaching_score": 89,
            "defensive_coaching_score": 85,
            "youth_trust_score": 87,
            "in_game_management_score": 90,
            "leadership_personality": "분석적 데이터 축구 추구, 정밀한 위치선정 코칭"
        }
    ]

    for m in test_managers:
        cur.execute("""
            INSERT INTO managers (
                manager_id, name, current_club, league, country, age, nationality, is_eu_citizen,
                contract_expires, preferred_formation, secondary_formation, top_formations_summary,
                games_analyzed, win_rate_pct, points_per_game, avg_goals_for, avg_goals_against,
                tactical_style, estimated_buyout_eur, weekly_wage_eur, tactical_flexibility_score,
                attacking_coaching_score, defensive_coaching_score, youth_trust_score,
                in_game_management_score, leadership_personality, preferred_player_profiles_json,
                name_ko, is_agency_client
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["manager_id"], m["name"], m["current_club"], m["league"], m["country"], m["age"],
            m["nationality"], m["is_eu_citizen"], m["contract_expires"], m["preferred_formation"],
            m["secondary_formation"], m["top_formations_summary"], m["games_analyzed"], m["win_rate_pct"],
            m["points_per_game"], m["avg_goals_for"], m["avg_goals_against"], m["tactical_style"],
            m["estimated_buyout_eur"], m["weekly_wage_eur"], m["tactical_flexibility_score"],
            m["attacking_coaching_score"], m["defensive_coaching_score"], m["youth_trust_score"],
            m["in_game_management_score"], m["leadership_personality"], sample_profiles_json,
            m["name_ko"], m["is_agency_client"]
        ))

    print(f"Successfully seeded {len(test_managers)} virtual test managers.")

    # 3. RECRUITMENT TARGETS (Targeted, NOT Signed)
    recruitment_targets = [
        {
            "target_type": "PLAYER",
            "target_id": 90001,
            "name": "Leo Park",
            "name_ko": "박레오",
            "category": "STEP_UP_PROSPECT",
            "current_agency": "가족 대리 (협상 오픈)",
            "agency_contract_expires": "2025-06-30",
            "scouting_status": "TARGETED",
            "potential_ceiling_score": 93.0,
            "stardom_commercial_score": 88.0,
            "agency_fit_score": 95.0,
            "projected_5yr_valuation_eur": 65000000,
            "projected_agency_roi_eur": 4500000,
            "recruitment_pitch_rationale": "20세 한국형 완성형 스트라이커. 유럽 빅5 스텝업 및 상업적 가치 극대화 최적 타깃."
        },
        {
            "target_type": "PLAYER",
            "target_id": 90002,
            "name": "David Han",
            "name_ko": "한다윗",
            "category": "BOSMAN_D6",
            "current_agency": "로컬 에이전시 (만료 임박)",
            "agency_contract_expires": "2025-06-30",
            "scouting_status": "TARGETED",
            "potential_ceiling_score": 89.0,
            "stardom_commercial_score": 84.0,
            "agency_fit_score": 92.0,
            "projected_5yr_valuation_eur": 45000000,
            "projected_agency_roi_eur": 3200000,
            "recruitment_pitch_rationale": "22세 테크니컬 미드필더. 유럽 중상위권 리그 주전 도약 및 FA 이적 시세차익 유력."
        },
        {
            "target_type": "MANAGER",
            "target_id": 90001,
            "name": "Jin-hyuk Kim",
            "name_ko": "김진혁 (감독)",
            "category": "FA_MANAGER",
            "current_agency": "직접 교섭 (자유 계약)",
            "agency_contract_expires": "2025-06-30",
            "scouting_status": "TARGETED",
            "potential_ceiling_score": 90.0,
            "stardom_commercial_score": 85.0,
            "agency_fit_score": 94.0,
            "projected_5yr_valuation_eur": 15000000,
            "projected_agency_roi_eur": 1200000,
            "recruitment_pitch_rationale": "통산 승률 62.5%, 현대적 압박 전술가. 아시아 챔피언스리그 및 유럽 무대 사령탑 추천 타깃."
        }
    ]

    for t in recruitment_targets:
        cur.execute("""
            INSERT INTO agency_recruitment_targets (
                target_type, target_id, name, name_ko, category, current_agency,
                agency_contract_expires, scouting_status, potential_ceiling_score,
                stardom_commercial_score, agency_fit_score, projected_5yr_valuation_eur,
                projected_agency_roi_eur, recruitment_pitch_rationale
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t["target_type"], t["target_id"], t["name"], t["name_ko"], t["category"],
            t["current_agency"], t["agency_contract_expires"], t["scouting_status"],
            t["potential_ceiling_score"], t["stardom_commercial_score"], t["agency_fit_score"],
            t["projected_5yr_valuation_eur"], t["projected_agency_roi_eur"], t["recruitment_pitch_rationale"]
        ))

    print(f"Successfully seeded {len(recruitment_targets)} targeted candidates.")

    # 4. AGENCY CONTRACTS CHECK
    cur.execute("SELECT COUNT(*) FROM agency_contracts")
    contract_count = cur.fetchone()[0]
    print(f"Current agency_contracts count: {contract_count} (Ensuring 0 for fresh testing)")

    conn.commit()
    conn.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_test_data()
