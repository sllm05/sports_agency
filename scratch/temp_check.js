/* mocked */
    // 1. 실제 DB에서 추출된 52명 선수 데이터셋
    const PLAYERS_DATABASE = [{"player_id": 1, "name": "Erling Haaland", "name_ko": "Erling Haaland", "position": "ST", "current_club": "Manchester City", "league": "Premier League", "market_value_eur": 220000000, "tactical_archetype": "박스 안 타점·결정력 집중형 스트라이커 (Box Finisher)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 실제 공격포인트(G+A)(0.82/90 · 포지션 상위 6%), 기대 공격포인트(xG+xAG)(0.9/90 · 포지션 상위 6%), 라인 침투 패스 리시브(8.3회/90 · 포지션 상위 11%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.06/90 · 포지션 하위 25%), 기회 창출(키패스)(0.95회/90 · 포지션 하위 29%)", "progression_tendency": "90분당 전진 패스 2.23회 · 전진 드리블 3.4회 · 라인 침투 리시브 8.3회 · Understat xGChain 0.75/90 · xGBuildup 0.12/90", "finishing_clinicality": "90분당 실득점 0.72골 / 기대득점(xG) 0.78 (xG 대비 -0.06) · 90분당 키패스 0.95회", "goals_per90": 0.72, "assists_per90": 0.1, "xg_per90": 0.78, "xa_per90": 0.12, "key_passes_per90": 0.95, "progressive_actions_per90": 5.63, "defensive_duels_won_pct": 49.0, "pos_percentile": 52}, {"player_id": 2, "name": "Lamine Yamal", "name_ko": "Lamine Yamal", "position": "RW", "current_club": "FC Barcelona", "league": "La Liga", "market_value_eur": 200000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 전진 드리블 운반(5.71회/90 · 포지션 상위 2%), 라인 침투 패스 리시브(13.66회/90 · 포지션 상위 2%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.03/90 · 포지션 하위 33%), 실제 공격포인트(G+A)(0.69/90 · 포지션 하위 92%)", "progression_tendency": "90분당 전진 패스 5.05회 · 전진 드리블 5.71회 · 라인 침투 리시브 13.66회 · Understat xGChain 1.2/90 · xGBuildup 0.56/90", "finishing_clinicality": "90분당 실득점 0.28골 / 기대득점(xG) 0.31 (xG 대비 -0.03) · 90분당 키패스 3.77회", "goals_per90": 0.28, "assists_per90": 0.37, "xg_per90": 0.31, "xa_per90": 0.44, "key_passes_per90": 3.77, "progressive_actions_per90": 10.76, "defensive_duels_won_pct": 50.0, "pos_percentile": 99}, {"player_id": 3, "name": "Kylian Mbappé", "name_ko": "Kylian Mbappé", "position": "ST", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 180000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(1.21/90 · 포지션 상위 2%), 전진 드리블 운반(4.67회/90 · 포지션 상위 3%), 라인 침투 패스 리시브(11.86회/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(1.56회/90 · 포지션 하위 53%), 대인 수비 경합 승리율(49.0% · 포지션 하위 73%)", "progression_tendency": "90분당 전진 패스 5.31회 · 전진 드리블 4.67회 · 라인 침투 리시브 11.86회 · Understat xGChain 1.17/90 · xGBuildup 0.34/90", "finishing_clinicality": "90분당 실득점 0.95골 / 기대득점(xG) 0.92 (xG 대비 +0.03) · 90분당 키패스 1.56회", "goals_per90": 0.95, "assists_per90": 0.25, "xg_per90": 0.92, "xa_per90": 0.29, "key_passes_per90": 1.56, "progressive_actions_per90": 9.98, "defensive_duels_won_pct": 49.0, "pos_percentile": 65}, {"player_id": 5, "name": "Michael Olise", "name_ko": "Michael Olise", "position": "RW", "current_club": "FC Bayern München", "league": "Bundesliga", "market_value_eur": 150000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 실제 공격포인트(G+A)(1.03/90 · 포지션 상위 2%), 기회 창출(키패스)(3.38회/90 · 포지션 상위 2%), 기대 공격포인트(xG+xAG)(0.92/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 70%), 기대득점 대비 결정력(G-xG)(0.08/90 · 포지션 하위 90%)", "progression_tendency": "90분당 전진 패스 9.71회 · 전진 드리블 4.73회 · 라인 침투 리시브 11.62회 · Understat xGChain 1.18/90 · xGBuildup 0.58/90", "finishing_clinicality": "90분당 실득점 0.46골 / 기대득점(xG) 0.38 (xG 대비 +0.08) · 90분당 키패스 3.38회", "goals_per90": 0.46, "assists_per90": 0.57, "xg_per90": 0.38, "xa_per90": 0.54, "key_passes_per90": 3.38, "progressive_actions_per90": 14.44, "defensive_duels_won_pct": 49.0, "pos_percentile": 90}, {"player_id": 4, "name": "Pedri", "name_ko": "Pedri", "position": "CM", "current_club": "FC Barcelona", "league": "La Liga", "market_value_eur": 150000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기회 창출(키패스)(3.52회/90 · 포지션 상위 1%), 전진 패스 전개(11.25회/90 · 포지션 상위 1%), 대인 수비 경합 승리율(50.0% · 포지션 상위 1%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대 공격포인트(xG+xAG)(0.3/90 · 포지션 하위 89%), 파울·카드 관리 안정성(0.944점 · 포지션 하위 93%)", "progression_tendency": "90분당 전진 패스 11.25회 · 전진 드리블 2.88회 · 라인 침투 리시브 4.25회 · Understat xGChain 0.96/90 · xGBuildup 0.72/90", "finishing_clinicality": "90분당 실득점 0.13골 / 기대득점(xG) 0.07 (xG 대비 +0.06) · 90분당 키패스 3.52회", "goals_per90": 0.13, "assists_per90": 0.2, "xg_per90": 0.07, "xa_per90": 0.23, "key_passes_per90": 3.52, "progressive_actions_per90": 14.13, "defensive_duels_won_pct": 50.0, "pos_percentile": 99}, {"player_id": 9, "name": "Khvicha Kvaratskhelia", "name_ko": "Khvicha Kvaratskhelia", "position": "LW", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 140000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 슈팅 볼륨(3.75회/90 · 포지션 상위 3%), 라인 침투 패스 리시브(10.36회/90 · 포지션 상위 9%), 기대득점 대비 결정력(G-xG)(0.06/90 · 포지션 상위 15%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 전진 드리블 운반(2.97회/90 · 포지션 하위 48%), 공격 시퀀스 관여도(xGChain)(0.66/90 · 포지션 하위 51%)", "progression_tendency": "90분당 전진 패스 4.92회 · 전진 드리블 2.97회 · 라인 침투 리시브 10.36회 · Understat xGChain 0.66/90 · xGBuildup 0.27/90", "finishing_clinicality": "90분당 실득점 0.37골 / 기대득점(xG) 0.31 (xG 대비 +0.06) · 90분당 키패스 2.02회", "goals_per90": 0.37, "assists_per90": 0.2, "xg_per90": 0.31, "xa_per90": 0.24, "key_passes_per90": 2.02, "progressive_actions_per90": 7.89, "defensive_duels_won_pct": 49.0, "pos_percentile": 93}, {"player_id": 8, "name": "Joao Neves", "name_ko": "Joao Neves", "position": "CM", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 140000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 공격 시퀀스 관여도(xGChain)(1.08/90 · 포지션 상위 1%), 전진 패스 전개(10.28회/90 · 포지션 상위 2%), 후방·중원 빌드업 기여(xGBuildup)(0.77/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 66%), 기회 창출(키패스)(1.58회/90 · 포지션 하위 85%)", "progression_tendency": "90분당 전진 패스 10.28회 · 전진 드리블 2.34회 · 라인 침투 리시브 5.07회 · Understat xGChain 1.08/90 · xGBuildup 0.77/90", "finishing_clinicality": "90분당 실득점 0.14골 / 기대득점(xG) 0.18 (xG 대비 -0.04) · 90분당 키패스 1.58회", "goals_per90": 0.14, "assists_per90": 0.09, "xg_per90": 0.18, "xa_per90": 0.11, "key_passes_per90": 1.58, "progressive_actions_per90": 12.62, "defensive_duels_won_pct": 49.0, "pos_percentile": 82}, {"player_id": 7, "name": "Vitinha", "name_ko": "Vitinha", "position": "DM", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 140000000, "tactical_archetype": "포백 보호 & 경합 회수 중심 홀딩 미드필더 (Ball-Winning 6)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 드리블 운반(1.9회/90 · 포지션 상위 3%), 파울·카드 관리 안정성(경기당 카드 0.08장 · 포지션 상위 16%), 기회 창출(키패스)(1.14회/90 · 포지션 상위 28%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 후방·중원 빌드업 기여(xGBuildup)(0.11/90 · 포지션 하위 7%), 전진 패스 전개(2.29회/90 · 포지션 하위 10%)", "progression_tendency": "90분당 전진 패스 2.29회 · 전진 드리블 1.9회 · 라인 침투 리시브 6.02회 · Understat xGChain 0.38/90 · xGBuildup 0.11/90", "finishing_clinicality": "90분당 실득점 0.13골 / 기대득점(xG) 0.12 (xG 대비 +0.01) · 90분당 키패스 1.14회", "goals_per90": 0.13, "assists_per90": 0.09, "xg_per90": 0.12, "xa_per90": 0.11, "key_passes_per90": 1.14, "progressive_actions_per90": 4.19, "defensive_duels_won_pct": 62.0, "pos_percentile": 92}, {"player_id": 6, "name": "Vinicius Junior", "name_ko": "Vinicius Junior", "position": "LW", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 140000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(0.85/90 · 포지션 상위 3%), 실제 공격포인트(G+A)(0.76/90 · 포지션 상위 6%), 슈팅 볼륨(3.22회/90 · 포지션 상위 6%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.07/90 · 포지션 하위 15%), 공격 시퀀스 관여도(xGChain)(0.93/90 · 포지션 하위 65%)", "progression_tendency": "90분당 전진 패스 5.52회 · 전진 드리블 4.21회 · 라인 침투 리시브 9.8회 · Understat xGChain 0.93/90 · xGBuildup 0.3/90", "finishing_clinicality": "90분당 실득점 0.44골 / 기대득점(xG) 0.51 (xG 대비 -0.07) · 90분당 키패스 2.3회", "goals_per90": 0.44, "assists_per90": 0.32, "xg_per90": 0.51, "xa_per90": 0.34, "key_passes_per90": 2.3, "progressive_actions_per90": 9.73, "defensive_duels_won_pct": 49.0, "pos_percentile": 76}, {"player_id": 10, "name": "Jude Bellingham", "name_ko": "Jude Bellingham", "position": "AM", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 130000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 후방·중원 빌드업 기여(xGBuildup)(0.55/90 · 포지션 상위 7%), 전진 패스 전개(7.71회/90 · 포지션 상위 10%), 기대 공격포인트(xG+xAG)(0.62/90 · 포지션 상위 10%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.754점 · 포지션 하위 5%), 기회 창출(키패스)(1.54회/90 · 포지션 하위 33%)", "progression_tendency": "90분당 전진 패스 7.71회 · 전진 드리블 2.45회 · 라인 침투 리시브 6.68회 · Understat xGChain 0.89/90 · xGBuildup 0.55/90", "finishing_clinicality": "90분당 실득점 0.32골 / 기대득점(xG) 0.47 (xG 대비 -0.15) · 90분당 키패스 1.54회", "goals_per90": 0.32, "assists_per90": 0.13, "xg_per90": 0.47, "xa_per90": 0.15, "key_passes_per90": 1.54, "progressive_actions_per90": 10.16, "defensive_duels_won_pct": 49.0, "pos_percentile": 66}, {"player_id": 12, "name": "Desire Doue", "name_ko": "Desire Doue", "position": "RW", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 120000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(0.84/90 · 포지션 상위 4%), 기회 창출(키패스)(2.87회/90 · 포지션 상위 4%), 공격 시퀀스 관여도(xGChain)(1.22/90 · 포지션 상위 4%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.01/90 · 포지션 하위 40%), 대인 수비 경합 승리율(49.0% · 포지션 하위 70%)", "progression_tendency": "90분당 전진 패스 9.14회 · 전진 드리블 4.65회 · 라인 침투 리시브 10.05회 · Understat xGChain 1.22/90 · xGBuildup 0.57/90", "finishing_clinicality": "90분당 실득점 0.31골 / 기대득점(xG) 0.32 (xG 대비 -0.01) · 90분당 키패스 2.87회", "goals_per90": 0.31, "assists_per90": 0.44, "xg_per90": 0.32, "xa_per90": 0.52, "key_passes_per90": 2.87, "progressive_actions_per90": 13.79, "defensive_duels_won_pct": 49.0, "pos_percentile": 96}, {"player_id": 11, "name": "Declan Rice", "name_ko": "Declan Rice", "position": "CM", "current_club": "Arsenal FC", "league": "Premier League", "market_value_eur": 120000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기회 창출(키패스)(2.47회/90 · 포지션 상위 4%), 전진 드리블 운반(2.87회/90 · 포지션 상위 4%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.861점 · 포지션 하위 31%), 후방·중원 빌드업 기여(xGBuildup)(0.33/90 · 포지션 하위 36%)", "progression_tendency": "90분당 전진 패스 6.11회 · 전진 드리블 2.87회 · 라인 침투 리시브 2.99회 · Understat xGChain 0.54/90 · xGBuildup 0.33/90", "finishing_clinicality": "90분당 실득점 0.13골 / 기대득점(xG) 0.11 (xG 대비 +0.02) · 90분당 키패스 2.47회", "goals_per90": 0.13, "assists_per90": 0.18, "xg_per90": 0.11, "xa_per90": 0.21, "key_passes_per90": 2.47, "progressive_actions_per90": 8.98, "defensive_duels_won_pct": 50.0, "pos_percentile": 97}, {"player_id": 13, "name": "Bukayo Saka", "name_ko": "Bukayo Saka", "position": "RW", "current_club": "Arsenal FC", "league": "Premier League", "market_value_eur": 110000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(1.05/90 · 포지션 상위 1%), 실제 공격포인트(G+A)(0.82/90 · 포지션 상위 3%), 기회 창출(키패스)(2.96회/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.15/90 · 포지션 하위 10%), 대인 수비 경합 승리율(49.0% · 포지션 하위 70%)", "progression_tendency": "90분당 전진 패스 6.23회 · 전진 드리블 4.16회 · 라인 침투 리시브 11.23회 · Understat xGChain 0.84/90 · xGBuildup 0.31/90", "finishing_clinicality": "90분당 실득점 0.31골 / 기대득점(xG) 0.46 (xG 대비 -0.15) · 90분당 키패스 2.96회", "goals_per90": 0.31, "assists_per90": 0.51, "xg_per90": 0.46, "xa_per90": 0.59, "key_passes_per90": 2.96, "progressive_actions_per90": 10.39, "defensive_duels_won_pct": 49.0, "pos_percentile": 60}, {"player_id": 22, "name": "Ousmane Dembélé", "name_ko": "Ousmane Dembélé", "position": "ST", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 100000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 드리블 운반(7.06회/90 · 포지션 상위 1%), 라인 침투 패스 리시브(14.52회/90 · 포지션 상위 1%), 공격 시퀀스 관여도(xGChain)(1.65/90 · 포지션 상위 1%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 73%), 기대득점 대비 결정력(G-xG)(0.13/90 · 포지션 하위 93%)", "progression_tendency": "90분당 전진 패스 8.58회 · 전진 드리블 7.06회 · 라인 침투 리시브 14.52회 · Understat xGChain 1.65/90 · xGBuildup 0.5/90", "finishing_clinicality": "90분당 실득점 1.08골 / 기대득점(xG) 0.95 (xG 대비 +0.13) · 90분당 키패스 3.14회", "goals_per90": 1.08, "assists_per90": 0.2, "xg_per90": 0.95, "xa_per90": 0.24, "key_passes_per90": 3.14, "progressive_actions_per90": 15.64, "defensive_duels_won_pct": 49.0, "pos_percentile": 92}, {"player_id": 20, "name": "Fermín López", "name_ko": "Fermín López", "position": "AM", "current_club": "FC Barcelona", "league": "La Liga", "market_value_eur": 100000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 공격 시퀀스 관여도(xGChain)(1.15/90 · 포지션 상위 4%), 후방·중원 빌드업 기여(xGBuildup)(0.58/90 · 포지션 상위 5%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.857점 · 포지션 하위 22%), 전진 드리블 운반(2.23회/90 · 포지션 하위 35%)", "progression_tendency": "90분당 전진 패스 5.68회 · 전진 드리블 2.23회 · 라인 침투 리시브 7.77회 · Understat xGChain 1.15/90 · xGBuildup 0.58/90", "finishing_clinicality": "90분당 실득점 0.43골 / 기대득점(xG) 0.41 (xG 대비 +0.02) · 90분당 키패스 2.84회", "goals_per90": 0.43, "assists_per90": 0.24, "xg_per90": 0.41, "xa_per90": 0.28, "key_passes_per90": 2.84, "progressive_actions_per90": 7.91, "defensive_duels_won_pct": 50.0, "pos_percentile": 93}, {"player_id": 19, "name": "Julián Álvarez", "name_ko": "Julián Álvarez", "position": "ST", "current_club": "Club Atlético de Madrid", "league": "La Liga", "market_value_eur": 100000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대득점 대비 결정력(G-xG)(0.1/90 · 포지션 상위 8%), 실제 공격포인트(G+A)(0.74/90 · 포지션 상위 10%), 기대 공격포인트(xG+xAG)(0.73/90 · 포지션 상위 12%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 슈팅 볼륨(2.55회/90 · 포지션 하위 42%), 라인 침투 패스 리시브(7.16회/90 · 포지션 하위 49%)", "progression_tendency": "90분당 전진 패스 5.1회 · 전진 드리블 3.39회 · 라인 침투 리시브 7.16회 · Understat xGChain 0.89/90 · xGBuildup 0.33/90", "finishing_clinicality": "90분당 실득점 0.6골 / 기대득점(xG) 0.5 (xG 대비 +0.10) · 90분당 키패스 1.45회", "goals_per90": 0.6, "assists_per90": 0.14, "xg_per90": 0.5, "xa_per90": 0.23, "key_passes_per90": 1.45, "progressive_actions_per90": 8.49, "defensive_duels_won_pct": 49.0, "pos_percentile": 62}, {"player_id": 18, "name": "Florian Wirtz", "name_ko": "Florian Wirtz", "position": "AM", "current_club": "Liverpool FC", "league": "Premier League", "market_value_eur": 100000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 드리블 운반(5.02회/90 · 포지션 상위 1%), 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기회 창출(키패스)(2.97회/90 · 포지션 상위 7%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.891점 · 포지션 하위 37%), 공격 시퀀스 관여도(xGChain)(0.79/90 · 포지션 하위 63%)", "progression_tendency": "90분당 전진 패스 6.74회 · 전진 드리블 5.02회 · 라인 침투 리시브 11.84회 · Understat xGChain 0.79/90 · xGBuildup 0.42/90", "finishing_clinicality": "90분당 실득점 0.38골 / 기대득점(xG) 0.36 (xG 대비 +0.02) · 90분당 키패스 2.97회 · PK 득점 2골", "goals_per90": 0.38, "assists_per90": 0.23, "xg_per90": 0.36, "xa_per90": 0.27, "key_passes_per90": 2.97, "progressive_actions_per90": 11.76, "defensive_duels_won_pct": 50.0, "pos_percentile": 98}, {"player_id": 17, "name": "Dominik Szoboszlai", "name_ko": "Dominik Szoboszlai", "position": "AM", "current_club": "Liverpool FC", "league": "Premier League", "market_value_eur": 100000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 후방·중원 빌드업 기여(xGBuildup)(0.56/90 · 포지션 상위 7%), 기회 창출(키패스)(2.61회/90 · 포지션 상위 15%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.879점 · 포지션 하위 29%), 전진 패스 전개(4.73회/90 · 포지션 하위 45%)", "progression_tendency": "90분당 전진 패스 4.73회 · 전진 드리블 2.6회 · 라인 침투 리시브 4.58회 · Understat xGChain 0.98/90 · xGBuildup 0.56/90", "finishing_clinicality": "90분당 실득점 0.22골 / 기대득점(xG) 0.27 (xG 대비 -0.05) · 90분당 키패스 2.61회", "goals_per90": 0.22, "assists_per90": 0.23, "xg_per90": 0.27, "xa_per90": 0.27, "key_passes_per90": 2.61, "progressive_actions_per90": 7.33, "defensive_duels_won_pct": 50.0, "pos_percentile": 42}, {"player_id": 16, "name": "Cole Palmer", "name_ko": "Cole Palmer", "position": "AM", "current_club": "Chelsea FC", "league": "Premier League", "market_value_eur": 100000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(0.8/90 · 포지션 상위 3%), 기회 창출(키패스)(2.43회/90 · 포지션 상위 18%), 전진 드리블 운반(4.02회/90 · 포지션 상위 25%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.855점 · 포지션 하위 20%), 후방·중원 빌드업 기여(xGBuildup)(0.27/90 · 포지션 하위 41%)", "progression_tendency": "90분당 전진 패스 5.29회 · 전진 드리블 4.02회 · 라인 침투 리시브 10.56회 · Understat xGChain 0.84/90 · xGBuildup 0.27/90", "finishing_clinicality": "90분당 실득점 0.42골 / 기대득점(xG) 0.44 (xG 대비 -0.02) · 90분당 키패스 2.43회", "goals_per90": 0.42, "assists_per90": 0.31, "xg_per90": 0.44, "xa_per90": 0.36, "key_passes_per90": 2.43, "progressive_actions_per90": 9.31, "defensive_duels_won_pct": 49.0, "pos_percentile": 57}, {"player_id": 15, "name": "Moisés Caicedo", "name_ko": "Moisés Caicedo", "position": "DM", "current_club": "Chelsea FC", "league": "Premier League", "market_value_eur": 100000000, "tactical_archetype": "후방 1차 빌드업 기점 & 탈압박형 수비형 미드필더 (Press-Resistant Pivot)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 팀 내 주전 선발 가동률(98.0% · 포지션 상위 8%), 후방·중원 빌드업 기여(xGBuildup)(0.47/90 · 포지션 상위 12%), 전진 패스 전개(6.1회/90 · 포지션 상위 15%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.712점 · 포지션 하위 8%), 기회 창출(키패스)(0.77회/90 · 포지션 하위 33%)", "progression_tendency": "90분당 전진 패스 6.1회 · 전진 드리블 0.73회 · 라인 침투 리시브 2.24회 · Understat xGChain 0.53/90 · xGBuildup 0.47/90", "finishing_clinicality": "90분당 실득점 0.03골 / 기대득점(xG) 0.02 (xG 대비 +0.01) · 90분당 키패스 0.77회", "goals_per90": 0.03, "assists_per90": 0.09, "xg_per90": 0.02, "xa_per90": 0.11, "key_passes_per90": 0.77, "progressive_actions_per90": 6.83, "defensive_duels_won_pct": 62.0, "pos_percentile": 75}, {"player_id": 14, "name": "William Saliba", "name_ko": "William Saliba", "position": "CB", "current_club": "Arsenal FC", "league": "Premier League", "market_value_eur": 100000000, "tactical_archetype": "전진 패스 & 후방 빌드업 주도형 볼플레잉 센터백 (Ball-Playing CB)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(64.0% · 포지션 상위 1%), 팀 내 주전 선발 가동률(100.0% · 포지션 상위 1%), 후방·중원 빌드업 기여(xGBuildup)(0.42/90 · 포지션 상위 10%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 전진 드리블 운반(0.47회/90 · 포지션 하위 34%), 전진 패스 전개(4.08회/90 · 포지션 하위 50%)", "progression_tendency": "90분당 전진 패스 4.08회 · 전진 드리블 0.47회 · 라인 침투 리시브 0.18회 · Understat xGChain 0.42/90 · xGBuildup 0.42/90", "finishing_clinicality": "90분당 실득점 0.06골 / 기대득점(xG) 0.07 (xG 대비 -0.01) · 90분당 키패스 0.93회", "goals_per90": 0.06, "assists_per90": 0.03, "xg_per90": 0.07, "xa_per90": 0.03, "key_passes_per90": 0.93, "progressive_actions_per90": 4.55, "defensive_duels_won_pct": 64.0, "pos_percentile": 33}, {"player_id": 29, "name": "Aleksandar Pavlović", "name_ko": "Aleksandar Pavlović", "position": "DM", "current_club": "FC Bayern München", "league": "Bundesliga", "market_value_eur": 90000000, "tactical_archetype": "후방 1차 빌드업 기점 & 탈압박형 수비형 미드필더 (Press-Resistant Pivot)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 패스 전개(9.93회/90 · 포지션 상위 2%), 후방·중원 빌드업 기여(xGBuildup)(0.83/90 · 포지션 상위 2%), 파울·카드 관리 안정성(경기당 카드 0.14장 · 포지션 상위 39%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(0.43회/90 · 포지션 하위 11%), 전진 드리블 운반(0.4회/90 · 포지션 하위 12%)", "progression_tendency": "90분당 전진 패스 9.93회 · 전진 드리블 0.4회 · 라인 침투 리시브 1.73회 · Understat xGChain 0.84/90 · xGBuildup 0.83/90", "finishing_clinicality": "90분당 실득점 0.06골 / 기대득점(xG) 0.04 (xG 대비 +0.02) · 90분당 키패스 0.43회", "goals_per90": 0.06, "assists_per90": 0.09, "xg_per90": 0.04, "xa_per90": 0.11, "key_passes_per90": 0.43, "progressive_actions_per90": 10.33, "defensive_duels_won_pct": 62.0, "pos_percentile": 88}, {"player_id": 28, "name": "Yan Diomandé", "name_ko": "Yan Diomandé", "position": "LW", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 90000000, "tactical_archetype": "터치라인 1대1 드리블 돌파 & 인사이드 커터 (1v1 Dribbler & Inside Forward)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 전진 드리블 운반(6.07회/90 · 포지션 상위 2%), 라인 침투 패스 리시브(10.49회/90 · 포지션 상위 8%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(1.38회/90 · 포지션 하위 33%), 슈팅 볼륨(1.82회/90 · 포지션 하위 33%)", "progression_tendency": "90분당 전진 패스 2.62회 · 전진 드리블 6.07회 · 라인 침투 리시브 10.49회 · Understat xGChain 0.6/90 · xGBuildup 0.43/90", "finishing_clinicality": "90분당 실득점 0.33골 / 기대득점(xG) 0.24 (xG 대비 +0.09) · 90분당 키패스 1.38회", "goals_per90": 0.33, "assists_per90": 0.12, "xg_per90": 0.24, "xa_per90": 0.14, "key_passes_per90": 1.38, "progressive_actions_per90": 8.69, "defensive_duels_won_pct": 50.0, "pos_percentile": 38}, {"player_id": 27, "name": "Arda Guler", "name_ko": "Arda Guler", "position": "AM", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 90000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(0.73/90 · 포지션 상위 5%), 기회 창출(키패스)(2.8회/90 · 포지션 상위 11%), 전진 패스 전개(6.66회/90 · 포지션 상위 15%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 59%), 후방·중원 빌드업 기여(xGBuildup)(0.36/90 · 포지션 하위 60%)", "progression_tendency": "90분당 전진 패스 6.66회 · 전진 드리블 4.11회 · 라인 침투 리시브 9.8회 · Understat xGChain 0.9/90 · xGBuildup 0.36/90", "finishing_clinicality": "90분당 실득점 0.22골 / 기대득점(xG) 0.29 (xG 대비 -0.07) · 90분당 키패스 2.8회", "goals_per90": 0.22, "assists_per90": 0.37, "xg_per90": 0.29, "xa_per90": 0.44, "key_passes_per90": 2.8, "progressive_actions_per90": 10.77, "defensive_duels_won_pct": 49.0, "pos_percentile": 66}, {"player_id": 26, "name": "Federico Valverde", "name_ko": "Federico Valverde", "position": "CM", "current_club": "Real Madrid CF", "league": "La Liga", "market_value_eur": 90000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 패스 전개(8.98회/90 · 포지션 상위 3%), 공격 시퀀스 관여도(xGChain)(0.83/90 · 포지션 상위 4%), 후방·중원 빌드업 기여(xGBuildup)(0.69/90 · 포지션 상위 4%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 전진 드리블 운반(1.33회/90 · 포지션 하위 27%), 파울·카드 관리 안정성(0.904점 · 포지션 하위 44%)", "progression_tendency": "90분당 전진 패스 8.98회 · 전진 드리블 1.33회 · 라인 침투 리시브 5.07회 · Understat xGChain 0.83/90 · xGBuildup 0.69/90", "finishing_clinicality": "90분당 실득점 0.18골 / 기대득점(xG) 0.07 (xG 대비 +0.11) · 90분당 키패스 1.16회", "goals_per90": 0.18, "assists_per90": 0.09, "xg_per90": 0.07, "xa_per90": 0.11, "key_passes_per90": 1.16, "progressive_actions_per90": 10.31, "defensive_duels_won_pct": 49.0, "pos_percentile": 50}, {"player_id": 25, "name": "Rayan Cherki", "name_ko": "Rayan Cherki", "position": "AM", "current_club": "Manchester City FC", "league": "Premier League", "market_value_eur": 90000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 드리블 운반(4.28회/90 · 포지션 상위 3%), 공격 시퀀스 관여도(xGChain)(1.05/90 · 포지션 상위 7%), 기대 공격포인트(xG+xAG)(0.62/90 · 포지션 상위 10%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 59%), 파울·카드 관리 안정성(0.939점 · 포지션 하위 70%)", "progression_tendency": "90분당 전진 패스 6.26회 · 전진 드리블 4.28회 · 라인 침투 리시브 8.26회 · Understat xGChain 1.05/90 · xGBuildup 0.38/90", "finishing_clinicality": "90분당 실득점 0.41골 / 기대득점(xG) 0.38 (xG 대비 +0.03) · 90분당 키패스 2.1회", "goals_per90": 0.41, "assists_per90": 0.2, "xg_per90": 0.38, "xa_per90": 0.24, "key_passes_per90": 2.1, "progressive_actions_per90": 10.54, "defensive_duels_won_pct": 49.0, "pos_percentile": 59}, {"player_id": 24, "name": "Enzo Fernández", "name_ko": "Enzo Fernández", "position": "CM", "current_club": "Manchester City FC", "league": "Premier League", "market_value_eur": 90000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기회 창출(키패스)(2.36회/90 · 포지션 상위 5%), 전진 드리블 운반(2.81회/90 · 포지션 상위 5%), 기대 공격포인트(xG+xAG)(0.43/90 · 포지션 상위 5%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.783점 · 포지션 하위 8%), 후방·중원 빌드업 기여(xGBuildup)(0.33/90 · 포지션 하위 36%)", "progression_tendency": "90분당 전진 패스 5.92회 · 전진 드리블 2.81회 · 라인 침투 리시브 6.85회 · Understat xGChain 0.64/90 · xGBuildup 0.33/90", "finishing_clinicality": "90분당 실득점 0.18골 / 기대득점(xG) 0.19 (xG 대비 -0.01) · 90분당 키패스 2.36회", "goals_per90": 0.18, "assists_per90": 0.2, "xg_per90": 0.19, "xa_per90": 0.24, "key_passes_per90": 2.36, "progressive_actions_per90": 8.73, "defensive_duels_won_pct": 49.0, "pos_percentile": 40}, {"player_id": 23, "name": "Morgan Rogers", "name_ko": "Morgan Rogers", "position": "AM", "current_club": "Chelsea FC", "league": "Premier League", "market_value_eur": 90000000, "tactical_archetype": "박스 타격 & 세컨드 스트라이커형 공격형 미드필더 (Shadow Striker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(49.0% · 포지션 상위 41%), 기대 공격포인트(xG+xAG)(0.46/90 · 포지션 상위 53%), 전진 드리블 운반(2.44회/90 · 포지션 상위 54%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.798점 · 포지션 하위 5%), 기회 창출(키패스)(1.44회/90 · 포지션 하위 29%)", "progression_tendency": "90분당 전진 패스 4.17회 · 전진 드리블 2.44회 · 라인 침투 리시브 5.25회 · Understat xGChain 0.6/90 · xGBuildup 0.25/90", "finishing_clinicality": "90분당 실득점 0.23골 / 기대득점(xG) 0.23 (xG 대비 +0.00) · 90분당 키패스 1.44회", "goals_per90": 0.23, "assists_per90": 0.2, "xg_per90": 0.23, "xa_per90": 0.23, "key_passes_per90": 1.44, "progressive_actions_per90": 6.61, "defensive_duels_won_pct": 49.0, "pos_percentile": 56}, {"player_id": 31, "name": "Lautaro Martínez", "name_ko": "Lautaro Martínez", "position": "ST", "current_club": "FC Internazionale Milano", "league": "Serie A", "market_value_eur": 85000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 라인 침투 패스 리시브(8.74회/90 · 포지션 상위 9%), 슈팅 볼륨(3.52회/90 · 포지션 상위 11%), 기대 공격포인트(xG+xAG)(0.7/90 · 포지션 상위 15%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.11/90 · 포지션 하위 18%), 실제 공격포인트(G+A)(0.51/90 · 포지션 하위 38%)", "progression_tendency": "90분당 전진 패스 2.88회 · 전진 드리블 3.29회 · 라인 침투 리시브 8.74회 · Understat xGChain 0.71/90 · xGBuildup 0.15/90", "finishing_clinicality": "90분당 실득점 0.41골 / 기대득점(xG) 0.52 (xG 대비 -0.11) · 90분당 키패스 1.28회", "goals_per90": 0.41, "assists_per90": 0.15, "xg_per90": 0.52, "xa_per90": 0.18, "key_passes_per90": 1.28, "progressive_actions_per90": 6.17, "defensive_duels_won_pct": 49.0, "pos_percentile": 73}, {"player_id": 30, "name": "Alexander Isak", "name_ko": "Alexander Isak", "position": "ST", "current_club": "Liverpool FC", "league": "Premier League", "market_value_eur": 85000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 실제 공격포인트(G+A)(0.95/90 · 포지션 상위 5%), 기대 공격포인트(xG+xAG)(0.8/90 · 포지션 상위 9%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 전진 드리블 운반(2.71회/90 · 포지션 하위 47%), 라인 침투 패스 리시브(7.09회/90 · 포지션 하위 49%)", "progression_tendency": "90분당 전진 패스 2.88회 · 전진 드리블 2.71회 · 라인 침투 리시브 7.09회 · Understat xGChain 0.84/90 · xGBuildup 0.11/90", "finishing_clinicality": "90분당 실득점 0.75골 / 기대득점(xG) 0.66 (xG 대비 +0.09) · 90분당 키패스 1.43회 · PK 득점 4골", "goals_per90": 0.75, "assists_per90": 0.2, "xg_per90": 0.66, "xa_per90": 0.14, "key_passes_per90": 1.43, "progressive_actions_per90": 5.59, "defensive_duels_won_pct": 50.0, "pos_percentile": 46}, {"player_id": 42, "name": "Warren Zaïre-Emery", "name_ko": "Warren Zaïre-Emery", "position": "CM", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 80000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 패스 전개(10.14회/90 · 포지션 상위 2%), 공격 시퀀스 관여도(xGChain)(0.96/90 · 포지션 상위 2%), 후방·중원 빌드업 기여(xGBuildup)(0.82/90 · 포지션 상위 2%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(0.79회/90 · 포지션 하위 12%), 전진 드리블 운반(1.1회/90 · 포지션 하위 20%)", "progression_tendency": "90분당 전진 패스 10.14회 · 전진 드리블 1.1회 · 라인 침투 리시브 2.67회 · Understat xGChain 0.96/90 · xGBuildup 0.82/90", "finishing_clinicality": "90분당 실득점 0.04골 / 기대득점(xG) 0.1 (xG 대비 -0.06) · 90분당 키패스 0.79회", "goals_per90": 0.04, "assists_per90": 0.09, "xg_per90": 0.1, "xa_per90": 0.11, "key_passes_per90": 0.79, "progressive_actions_per90": 11.24, "defensive_duels_won_pct": 49.0, "pos_percentile": 82}, {"player_id": 41, "name": "Nuno Mendes", "name_ko": "Nuno Mendes", "position": "LB", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 80000000, "tactical_archetype": "중원 빌드업 합류 & 패스 전개형 풀백 (Inverted / Build-up Full-Back)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 패스 전개(11.91회/90 · 포지션 상위 2%), 후방·중원 빌드업 기여(xGBuildup)(0.91/90 · 포지션 상위 2%), 기회 창출(키패스)(1.61회/90 · 포지션 상위 19%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.862점 · 포지션 하위 46%), 대인 수비 경합 승리율(62.0% · 포지션 하위 54%)", "progression_tendency": "90분당 전진 패스 11.91회 · 전진 드리블 2.14회 · 라인 침투 리시브 4.7회 · Understat xGChain 1.17/90 · xGBuildup 0.91/90", "finishing_clinicality": "90분당 실득점 0.11골 / 기대득점(xG) 0.09 (xG 대비 +0.02) · 90분당 키패스 1.61회", "goals_per90": 0.11, "assists_per90": 0.09, "xg_per90": 0.09, "xa_per90": 0.11, "key_passes_per90": 1.61, "progressive_actions_per90": 14.05, "defensive_duels_won_pct": 62.0, "pos_percentile": 89}, {"player_id": 40, "name": "Achraf Hakimi", "name_ko": "Achraf Hakimi", "position": "RB", "current_club": "Paris Saint-Germain FC", "league": "Ligue 1", "market_value_eur": 80000000, "tactical_archetype": "중원 빌드업 합류 & 패스 전개형 풀백 (Inverted / Build-up Full-Back)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 전진 패스 전개(12.22회/90 · 포지션 상위 1%), 후방·중원 빌드업 기여(xGBuildup)(0.89/90 · 포지션 상위 2%), 기회 창출(키패스)(2.21회/90 · 포지션 상위 5%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.835점 · 포지션 하위 36%), 대인 수비 경합 승리율(62.0% · 포지션 하위 53%)", "progression_tendency": "90분당 전진 패스 12.22회 · 전진 드리블 2.5회 · 라인 침투 리시브 6.18회 · Understat xGChain 1.15/90 · xGBuildup 0.89/90", "finishing_clinicality": "90분당 실득점 0.17골 / 기대득점(xG) 0.18 (xG 대비 -0.01) · 90분당 키패스 2.21회", "goals_per90": 0.17, "assists_per90": 0.09, "xg_per90": 0.18, "xa_per90": 0.11, "key_passes_per90": 2.21, "progressive_actions_per90": 14.72, "defensive_duels_won_pct": 62.0, "pos_percentile": 94}, {"player_id": 39, "name": "Nico Paz", "name_ko": "Nico Paz", "position": "AM", "current_club": "Como 1907", "league": "Serie A", "market_value_eur": 80000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(49.0% · 포지션 상위 41%), 전진 드리블 운반(2.75회/90 · 포지션 상위 45%), 기대 공격포인트(xG+xAG)(0.51/90 · 포지션 상위 47%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.859점 · 포지션 하위 23%), 후방·중원 빌드업 기여(xGBuildup)(0.19/90 · 포지션 하위 24%)", "progression_tendency": "90분당 전진 패스 3.81회 · 전진 드리블 2.75회 · 라인 침투 리시브 9.83회 · Understat xGChain 0.56/90 · xGBuildup 0.19/90", "finishing_clinicality": "90분당 실득점 0.2골 / 기대득점(xG) 0.33 (xG 대비 -0.13) · 90분당 키패스 1.8회", "goals_per90": 0.2, "assists_per90": 0.15, "xg_per90": 0.33, "xa_per90": 0.18, "key_passes_per90": 1.8, "progressive_actions_per90": 6.56, "defensive_duels_won_pct": 49.0, "pos_percentile": 77}, {"player_id": 38, "name": "Pau Cubarsí", "name_ko": "Pau Cubarsí", "position": "CB", "current_club": "FC Barcelona", "league": "La Liga", "market_value_eur": 80000000, "tactical_archetype": "전진 패스 & 후방 빌드업 주도형 볼플레잉 센터백 (Ball-Playing CB)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(64.0% · 포지션 상위 1%), 기회 창출(키패스)(1.57회/90 · 포지션 상위 2%), 후방·중원 빌드업 기여(xGBuildup)(0.59/90 · 포지션 상위 4%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.866점 · 포지션 하위 50%), 전진 드리블 운반(0.89회/90 · 포지션 하위 52%)", "progression_tendency": "90분당 전진 패스 6.56회 · 전진 드리블 0.89회 · 라인 침투 리시브 0.21회 · Understat xGChain 0.59/90 · xGBuildup 0.59/90", "finishing_clinicality": "90분당 실득점 0.0골 / 기대득점(xG) 0.03 (xG 대비 -0.03) · 90분당 키패스 1.57회", "goals_per90": 0.0, "assists_per90": 0.05, "xg_per90": 0.03, "xa_per90": 0.06, "key_passes_per90": 1.57, "progressive_actions_per90": 7.45, "defensive_duels_won_pct": 64.0, "pos_percentile": 55}, {"player_id": 37, "name": "Sandro Tonali", "name_ko": "Sandro Tonali", "position": "DM", "current_club": "Tottenham Hotspur FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "포백 보호 & 경합 회수 중심 홀딩 미드필더 (Ball-Winning 6)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(64.0% · 포지션 상위 1%), 후방·중원 빌드업 기여(xGBuildup)(0.38/90 · 포지션 상위 22%), 기회 창출(키패스)(1.24회/90 · 포지션 상위 24%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.81점 · 포지션 하위 39%), 전진 패스 전개(4.38회/90 · 포지션 하위 51%)", "progression_tendency": "90분당 전진 패스 4.38회 · 전진 드리블 1.27회 · 라인 침투 리시브 1.82회 · Understat xGChain 0.53/90 · xGBuildup 0.38/90", "finishing_clinicality": "90분당 실득점 0.14골 / 기대득점(xG) 0.15 (xG 대비 -0.01) · 90분당 키패스 1.24회", "goals_per90": 0.14, "assists_per90": 0.06, "xg_per90": 0.15, "xa_per90": 0.07, "key_passes_per90": 1.24, "progressive_actions_per90": 5.65, "defensive_duels_won_pct": 64.0, "pos_percentile": 45}, {"player_id": 36, "name": "Antoine Semenyo", "name_ko": "Antoine Semenyo", "position": "RW", "current_club": "Manchester City FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "터치라인 1대1 드리블 돌파 & 인사이드 커터 (1v1 Dribbler & Inside Forward)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 슈팅 볼륨(3.52회/90 · 포지션 상위 4%), 기대득점 대비 결정력(G-xG)(0.03/90 · 포지션 상위 21%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(1.59회/90 · 포지션 하위 47%), 실제 공격포인트(G+A)(0.45/90 · 포지션 하위 52%)", "progression_tendency": "90분당 전진 패스 3.06회 · 전진 드리블 3.93회 · 라인 침투 리시브 7.92회 · Understat xGChain 0.73/90 · xGBuildup 0.22/90", "finishing_clinicality": "90분당 실득점 0.31골 / 기대득점(xG) 0.28 (xG 대비 +0.03) · 90분당 키패스 1.59회", "goals_per90": 0.31, "assists_per90": 0.14, "xg_per90": 0.28, "xa_per90": 0.16, "key_passes_per90": 1.59, "progressive_actions_per90": 6.99, "defensive_duels_won_pct": 50.0, "pos_percentile": 34}, {"player_id": 35, "name": "Hugo Ekitike", "name_ko": "Hugo Ekitike", "position": "ST", "current_club": "Liverpool FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기대 공격포인트(xG+xAG)(1.0/90 · 포지션 상위 4%), 공격 시퀀스 관여도(xGChain)(1.1/90 · 포지션 상위 5%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기대득점 대비 결정력(G-xG)(-0.23/90 · 포지션 하위 7%), 라인 침투 패스 리시브(7.54회/90 · 포지션 하위 52%)", "progression_tendency": "90분당 전진 패스 1.86회 · 전진 드리블 3.26회 · 라인 침투 리시브 7.54회 · Understat xGChain 1.1/90 · xGBuildup 0.23/90", "finishing_clinicality": "90분당 실득점 0.53골 / 기대득점(xG) 0.76 (xG 대비 -0.23) · 90분당 키패스 1.89회 · PK 득점 1골", "goals_per90": 0.53, "assists_per90": 0.2, "xg_per90": 0.76, "xa_per90": 0.24, "key_passes_per90": 1.89, "progressive_actions_per90": 5.12, "defensive_duels_won_pct": 50.0, "pos_percentile": 47}, {"player_id": 34, "name": "Ryan Gravenberch", "name_ko": "Ryan Gravenberch", "position": "DM", "current_club": "Liverpool FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "후방 1차 빌드업 기점 & 탈압박형 수비형 미드필더 (Press-Resistant Pivot)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(64.0% · 포지션 상위 1%), 팀 내 주전 선발 가동률(100.0% · 포지션 상위 1%), 전진 드리블 운반(1.99회/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 전진 패스 전개(5.16회/90 · 포지션 하위 64%), 파울·카드 관리 안정성(0.874점 · 포지션 하위 66%)", "progression_tendency": "90분당 전진 패스 5.16회 · 전진 드리블 1.99회 · 라인 침투 리시브 1.57회 · Understat xGChain 0.6/90 · xGBuildup 0.54/90", "finishing_clinicality": "90분당 실득점 0.0골 / 기대득점(xG) 0.03 (xG 대비 -0.03) · 90분당 키패스 1.51회", "goals_per90": 0.0, "assists_per90": 0.08, "xg_per90": 0.03, "xa_per90": 0.09, "key_passes_per90": 1.51, "progressive_actions_per90": 7.15, "defensive_duels_won_pct": 64.0, "pos_percentile": 61}, {"player_id": 33, "name": "Estevao", "name_ko": "Estevao", "position": "RW", "current_club": "Chelsea FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 공격 시퀀스 관여도(xGChain)(1.05/90 · 포지션 상위 7%), 실제 공격포인트(G+A)(0.67/90 · 포지션 상위 10%), 전진 드리블 운반(4.28회/90 · 포지션 상위 10%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 70%), 기대득점 대비 결정력(G-xG)(0.03/90 · 포지션 하위 79%)", "progression_tendency": "90분당 전진 패스 6.26회 · 전진 드리블 4.28회 · 라인 침투 리시브 8.26회 · Understat xGChain 1.05/90 · xGBuildup 0.38/90", "finishing_clinicality": "90분당 실득점 0.41골 / 기대득점(xG) 0.38 (xG 대비 +0.03) · 90분당 키패스 2.1회", "goals_per90": 0.41, "assists_per90": 0.26, "xg_per90": 0.38, "xa_per90": 0.24, "key_passes_per90": 2.1, "progressive_actions_per90": 10.54, "defensive_duels_won_pct": 49.0, "pos_percentile": 64}, {"player_id": 32, "name": "João Pedro", "name_ko": "João Pedro", "position": "ST", "current_club": "Chelsea FC", "league": "Premier League", "market_value_eur": 80000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 실제 공격포인트(G+A)(0.73/90 · 포지션 상위 10%), 기대득점 대비 결정력(G-xG)(0.06/90 · 포지션 상위 14%), 기대 공격포인트(xG+xAG)(0.66/90 · 포지션 상위 17%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 슈팅 볼륨(2.14회/90 · 포지션 하위 23%), 라인 침투 패스 리시브(6.26회/90 · 포지션 하위 38%)", "progression_tendency": "90분당 전진 패스 5.26회 · 전진 드리블 2.53회 · 라인 침투 리시브 6.26회 · Understat xGChain 0.73/90 · xGBuildup 0.35/90", "finishing_clinicality": "90분당 실득점 0.46골 / 기대득점(xG) 0.4 (xG 대비 +0.06) · 90분당 키패스 1.37회", "goals_per90": 0.46, "assists_per90": 0.27, "xg_per90": 0.4, "xa_per90": 0.26, "key_passes_per90": 1.37, "progressive_actions_per90": 7.79, "defensive_duels_won_pct": 49.0, "pos_percentile": 51}, {"player_id": 21, "name": "Jamal Musiala", "name_ko": "Jamal Musiala", "position": "AM", "current_club": "FC 바이에른 뮌헨", "league": "분데스리가", "market_value_eur": 80000000, "tactical_archetype": "라인 브레이킹 스루패스 & 찬스메이킹 10번 (Advanced Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대 공격포인트(xG+xAG)(0.83/90 · 포지션 상위 2%), 공격 시퀀스 관여도(xGChain)(1.16/90 · 포지션 상위 3%), 전진 패스 전개(7.81회/90 · 포지션 상위 9%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(2.03회/90 · 포지션 하위 54%), 대인 수비 경합 승리율(49.0% · 포지션 하위 59%)", "progression_tendency": "90분당 전진 패스 7.81회 · 전진 드리블 4.1회 · 라인 침투 리시브 9.63회 · Understat xGChain 1.16/90 · xGBuildup 0.52/90", "finishing_clinicality": "90분당 실득점 0.59골 / 기대득점(xG) 0.55 (xG 대비 +0.04) · 90분당 키패스 2.03회", "goals_per90": 0.59, "assists_per90": 0.24, "xg_per90": 0.55, "xa_per90": 0.28, "key_passes_per90": 2.03, "progressive_actions_per90": 11.91, "defensive_duels_won_pct": 49.0, "pos_percentile": 81}, {"player_id": 49, "name": "Kenan Yıldız", "name_ko": "Kenan Yıldız", "position": "LW", "current_club": "Juventus FC", "league": "Serie A", "market_value_eur": 75000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 공격 시퀀스 관여도(xGChain)(1.05/90 · 포지션 상위 5%), 기대 공격포인트(xG+xAG)(0.62/90 · 포지션 상위 8%), 실제 공격포인트(G+A)(0.67/90 · 포지션 상위 9%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 대인 수비 경합 승리율(49.0% · 포지션 하위 74%), 기대득점 대비 결정력(G-xG)(0.03/90 · 포지션 하위 81%)", "progression_tendency": "90분당 전진 패스 6.26회 · 전진 드리블 4.28회 · 라인 침투 리시브 8.26회 · Understat xGChain 1.05/90 · xGBuildup 0.38/90", "finishing_clinicality": "90분당 실득점 0.41골 / 기대득점(xG) 0.38 (xG 대비 +0.03) · 90분당 키패스 2.1회", "goals_per90": 0.41, "assists_per90": 0.26, "xg_per90": 0.38, "xa_per90": 0.24, "key_passes_per90": 2.1, "progressive_actions_per90": 10.54, "defensive_duels_won_pct": 49.0, "pos_percentile": 83}, {"player_id": 48, "name": "Benjamin Šeško", "name_ko": "Benjamin Šeško", "position": "ST", "current_club": "Manchester United FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "박스 안 타점·결정력 집중형 스트라이커 (Box Finisher)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대득점 대비 결정력(G-xG)(0.08/90 · 포지션 상위 10%), 대인 수비 경합 승리율(49.0% · 포지션 상위 27%), 실제 공격포인트(G+A)(0.66/90 · 포지션 상위 45%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(0.7회/90 · 포지션 하위 18%), 공격 시퀀스 관여도(xGChain)(0.55/90 · 포지션 하위 31%)", "progression_tendency": "90분당 전진 패스 2.58회 · 전진 드리블 2.13회 · 라인 침투 리시브 5.89회 · Understat xGChain 0.55/90 · xGBuildup 0.17/90", "finishing_clinicality": "90분당 실득점 0.48골 / 기대득점(xG) 0.4 (xG 대비 +0.08) · 90분당 키패스 0.7회", "goals_per90": 0.48, "assists_per90": 0.18, "xg_per90": 0.4, "xa_per90": 0.24, "key_passes_per90": 0.7, "progressive_actions_per90": 4.71, "defensive_duels_won_pct": 49.0, "pos_percentile": 53}, {"player_id": 47, "name": "Matheus Cunha", "name_ko": "Matheus Cunha", "position": "ST", "current_club": "Manchester United FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "하프스페이스 연계 & 찬스메이킹 겸비 스트라이커 (Complete Link-Up 9)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기대득점 대비 결정력(G-xG)(0.22/90 · 포지션 상위 3%), 기회 창출(키패스)(2.65회/90 · 포지션 상위 3%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 라인 침투 패스 리시브(5.57회/90 · 포지션 하위 30%), 공격 시퀀스 관여도(xGChain)(0.62/90 · 포지션 하위 38%)", "progression_tendency": "90분당 전진 패스 4.98회 · 전진 드리블 3.88회 · 라인 침투 리시브 5.57회 · Understat xGChain 0.62/90 · xGBuildup 0.24/90", "finishing_clinicality": "90분당 실득점 0.52골 / 기대득점(xG) 0.3 (xG 대비 +0.22) · 90분당 키패스 2.65회", "goals_per90": 0.52, "assists_per90": 0.23, "xg_per90": 0.3, "xa_per90": 0.27, "key_passes_per90": 2.65, "progressive_actions_per90": 8.86, "defensive_duels_won_pct": 50.0, "pos_percentile": 98}, {"player_id": 46, "name": "Bryan Mbeumo", "name_ko": "Bryan Mbeumo", "position": "RW", "current_club": "Manchester United FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기대득점 대비 결정력(G-xG)(0.21/90 · 포지션 상위 4%), 실제 공격포인트(G+A)(0.71/90 · 포지션 상위 6%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 공격 시퀀스 관여도(xGChain)(0.64/90 · 포지션 하위 49%), 슈팅 볼륨(2.26회/90 · 포지션 하위 57%)", "progression_tendency": "90분당 전진 패스 3.72회 · 전진 드리블 3.43회 · 라인 침투 리시브 9.26회 · Understat xGChain 0.64/90 · xGBuildup 0.25/90", "finishing_clinicality": "90분당 실득점 0.53골 / 기대득점(xG) 0.32 (xG 대비 +0.21) · 90분당 키패스 2.1회 · PK 득점 5골", "goals_per90": 0.53, "assists_per90": 0.18, "xg_per90": 0.32, "xa_per90": 0.22, "key_passes_per90": 2.1, "progressive_actions_per90": 7.15, "defensive_duels_won_pct": 50.0, "pos_percentile": 47}, {"player_id": 45, "name": "Jeremy Doku", "name_ko": "Jeremy Doku", "position": "LW", "current_club": "Manchester City FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 기대득점 대비 결정력(G-xG)(0.07/90 · 포지션 상위 14%), 대인 수비 경합 승리율(49.0% · 포지션 상위 26%), 실제 공격포인트(G+A)(0.54/90 · 포지션 상위 43%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 슈팅 볼륨(1.72회/90 · 포지션 하위 27%), 전진 드리블 운반(2.44회/90 · 포지션 하위 34%)", "progression_tendency": "90분당 전진 패스 5.62회 · 전진 드리블 2.44회 · 라인 침투 리시브 6.31회 · Understat xGChain 0.63/90 · xGBuildup 0.34/90", "finishing_clinicality": "90분당 실득점 0.18골 / 기대득점(xG) 0.11 (xG 대비 +0.07) · 90분당 키패스 1.9회", "goals_per90": 0.18, "assists_per90": 0.36, "xg_per90": 0.11, "xa_per90": 0.24, "key_passes_per90": 1.9, "progressive_actions_per90": 8.06, "defensive_duels_won_pct": 49.0, "pos_percentile": 67}, {"player_id": 44, "name": "Elliot Anderson", "name_ko": "Elliot Anderson", "position": "CM", "current_club": "Manchester City FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "중원 템포 조절 & 전진 패스 배급형 미드필더 (Deep-Lying Passer)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 기회 창출(키패스)(1.56회/90 · 포지션 상위 16%), 전진 드리블 운반(1.72회/90 · 포지션 상위 59%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 공격 시퀀스 관여도(xGChain)(0.32/90 · 포지션 하위 16%), 후방·중원 빌드업 기여(xGBuildup)(0.21/90 · 포지션 하위 20%)", "progression_tendency": "90분당 전진 패스 4.72회 · 전진 드리블 1.72회 · 라인 침투 리시브 3.1회 · Understat xGChain 0.32/90 · xGBuildup 0.21/90", "finishing_clinicality": "90분당 실득점 0.07골 / 기대득점(xG) 0.07 (xG 대비 +0.00) · 90분당 키패스 1.56회", "goals_per90": 0.07, "assists_per90": 0.09, "xg_per90": 0.07, "xa_per90": 0.11, "key_passes_per90": 1.56, "progressive_actions_per90": 6.44, "defensive_duels_won_pct": 50.0, "pos_percentile": 31}, {"player_id": 43, "name": "Martín Zubimendi", "name_ko": "Martín Zubimendi", "position": "DM", "current_club": "Arsenal FC", "league": "Premier League", "market_value_eur": 75000000, "tactical_archetype": "후방 1차 빌드업 기점 & 탈압박형 수비형 미드필더 (Press-Resistant Pivot)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(64.0% · 포지션 상위 1%), 전진 패스 전개(5.93회/90 · 포지션 상위 16%), 팀 내 주전 선발 가동률(92.0% · 포지션 상위 19%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 파울·카드 관리 안정성(0.811점 · 포지션 하위 41%), 후방·중원 빌드업 기여(xGBuildup)(0.3/90 · 포지션 하위 49%)", "progression_tendency": "90분당 전진 패스 5.93회 · 전진 드리블 1.16회 · 라인 침투 리시브 1.31회 · Understat xGChain 0.4/90 · xGBuildup 0.3/90", "finishing_clinicality": "90분당 실득점 0.06골 / 기대득점(xG) 0.08 (xG 대비 -0.02) · 90분당 키패스 1.26회", "goals_per90": 0.06, "assists_per90": 0.03, "xg_per90": 0.08, "xa_per90": 0.03, "key_passes_per90": 1.26, "progressive_actions_per90": 7.09, "defensive_duels_won_pct": 64.0, "pos_percentile": 57}, {"player_id": 64, "name": "Luis Díaz", "name_ko": "Luis Díaz", "position": "LW", "current_club": "FC Bayern München", "league": "Bundesliga", "market_value_eur": 70000000, "tactical_archetype": "측면 플레이메이커 & 기회 창출형 윙어 (Wide Playmaker)", "strengths_tags": "[Opta/FBref·Understat 실측 강점] 대인 수비 경합 승리율(50.0% · 포지션 상위 1%), 라인 침투 패스 리시브(10.97회/90 · 포지션 상위 6%), 실제 공격포인트(G+A)(0.68/90 · 포지션 상위 8%)", "weaknesses_tags": "[Opta/FBref·Understat 실측 보완점] 기회 창출(키패스)(1.98회/90 · 포지션 하위 61%), 전진 드리블 운반(4.04회/90 · 포지션 하위 64%)", "progression_tendency": "90분당 전진 패스 4.12회 · 전진 드리블 4.04회 · 라인 침투 리시브 10.97회 · Understat xGChain 1.0/90 · xGBuildup 0.38/90", "finishing_clinicality": "90분당 실득점 0.49골 / 기대득점(xG) 0.45 (xG 대비 +0.04) · 90분당 키패스 1.98회", "goals_per90": 0.49, "assists_per90": 0.19, "xg_per90": 0.45, "xa_per90": 0.19, "key_passes_per90": 1.98, "progressive_actions_per90": 8.16, "defensive_duels_won_pct": 50.0, "pos_percentile": 53}];

    // 공식 유튜브 하이라이트 매핑
    const YT_MAP = {
      '손흥민': 'YhEcyglkOx0',
      'Heung-min Son': 'YhEcyglkOx0',
      '이강인': '2Ec8VofpRmo',
      'Kang-in Lee': '2Ec8VofpRmo',
      '김민재': '38LUvS2jOOU',
      'Min-Jae Kim': '38LUvS2jOOU',
      '황희찬': 'DVNwiAPuPTY',
      'Hwang Heechan': 'DVNwiAPuPTY',
      'Erling Haaland': '8cfwD8ybFfw',
      'Kevin De Bruyne': 'Tw1fCcNaKhc',
      'Rodri': 'Lpz4PUPJ5kM',
      'Kylian Mbappe': '6VC5VHn5EQM',
      'Jude Bellingham': 'kNwOJ-BJcPk',
      'Bukayo Saka': '9ogC38l8nTU',
      'Virgil van Dijk': '38LUvS2jOOU',
      'Bruno Fernandes': 'h2EwOys6evI',
      'Mohamed Salah': 'DvEMr0reE7Y',
      'Young-woo Seol': 'DVNwiAPuPTY',
      '설영우': 'DVNwiAPuPTY',
      '조현우': 'DVNwiAPuPTY',
      '황인범': 'DVNwiAPuPTY'
    };

    // 상태 관리
    let currentPlayer = null;
    let currentActionIdx = 0;
    let isPlaying = true;
    let currentTime = 0; // 0.0 ~ 8.0초
    let playbackSpeed = 1.0;
    const TOTAL_DURATION = 8.0;

    const canvas = document.getElementById('pitchCanvas');
    const ctx = canvas.getContext('2d');

    const MARGIN = 36;
    const PITCH_W = canvas.width - MARGIN * 2;   // 1008
    const PITCH_H = canvas.height - MARGIN * 2;  // 608

    function toPixel(gx, gy) {
      // gx: 0~18 (가로 그리드), gy: 0~12 (세로 그리드)
      return {
        x: MARGIN + (gx / 18) * PITCH_W,
        y: MARGIN + (gy / 12) * PITCH_H
      };
    }

    // =========================================================================
    // 2. 선수별 고유 시그니처 액션 정의 엔진 (DB 스탯 기반 결정론적 키프레임)
    // =========================================================================
    function generatePlayerActions(p) {
      const pos = (p.position || 'ST').toUpperCase();
      const archetype = p.tactical_archetype || '';
      const name = p.name_ko || p.name;
      const xg = p.xg_per90 ? p.xg_per90.toFixed(2) : '0.45';
      const kp = p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '2.1';
      const defPct = p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '60';

      // 1) 손흥민 시그니처
      if (name.includes('손흥민') || p.name.includes('Son')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '득점',
            title: `[손흥민 존] 하프스페이스 컷인 & 파포스트 감아차기 골`,
            desc: `하프스페이스 뒷공간으로 34.2km/h 스프린트 후 수비수 1명을 제치고 골대 구석으로 휘어 차는 시그니처 득점 (xG ${xg} / 전환율 +32%)`,
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 3.5, ball: 'target', status: '하프라인 부근에서 침투 각도 형성', metric: '속도: 18.5 km/h' },
              { t: 2.2, targetGx: 13.5, targetGy: 4.2, ball: 'target', status: '⚡ 폭발적 라인 브레이킹 스프린트!', metric: '속도: 34.2 km/h (순간 최고속)' },
              { t: 4.5, targetGx: 14.8, targetGy: 5.2, ball: 'target', status: '수비수를 안쪽으로 제쳐내며 슈팅 각도 확보', metric: '탈압박 성공 · 감아차기 준비' },
              { t: 5.8, targetGx: 15.0, targetGy: 5.3, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.0 }, status: '⚽ 환상적인 인프런트 감아차기 슈팅!', metric: `xG: ${xg} · 회전 감아차기` },
              { t: 8.0, targetGx: 15.2, targetGy: 5.4, ball: 'goal', status: '🎉 골망 구석을 가르는 완벽한 골인!!', metric: '결정력 전환율 +32% 입증' }
            ]
          },
          {
            type: 'PASS', tag: 'pass', tagText: '찬스메이킹',
            title: `[폭풍 질주 후 컷백] 40m 카운터어택 & 킬러 패스`,
            desc: `역습 상황에서 폭발적인 가속도로 터치라인을 찢은 뒤 박스 안 동료에게 정확히 연결한 컷백 어시스트`,
            phases: [
              { t: 0.0, targetGx: 8.0, targetGy: 2.0, ball: 'target', status: '하프라인 왼쪽 측면에서 볼 수신', metric: '가속 시작' },
              { t: 3.0, targetGx: 14.2, targetGy: 2.2, ball: 'target', status: '측면 수비수를 스피드로 완벽히 무력화', metric: '속도: 33.1 km/h' },
              { t: 5.0, targetGx: 16.0, targetGy: 3.0, ball: 'target', status: '골라인 직전 감속 후 문전 동료 확인', metric: '시야 확보' },
              { t: 6.2, targetGx: 16.0, targetGy: 3.0, ball: 'pass', passTarget: { gx: 15.5, gy: 6.0 }, status: '🎯 쇄도하는 스트라이커 발밑으로 핀포인트 컷백!', metric: 'xA: 0.35 찬스 메이킹' },
              { t: 8.0, targetGx: 16.0, targetGy: 3.0, ball: 'finish', status: '동료의 논스톱 슈팅 마무리 연결', metric: '키패스 성공' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '단독 돌파',
            title: `[단독 드리블 돌파] 수비 2명 사이를 뚫는 저돌적 역습`,
            desc: `수비수 2명의 협력 압박 사이를 순간적인 바디페인팅과 주력으로 돌파하는 크랙 플레이`,
            phases: [
              { t: 0.0, targetGx: 9.0, targetGy: 4.5, ball: 'target', status: '중원 압박 사이에서 볼 키핑', metric: '무게중심 전환' },
              { t: 2.5, targetGx: 11.8, targetGy: 3.8, ball: 'target', status: '상대 센터백의 발을 빼앗는 넛메그 돌파', metric: '수비수 역동작 유발' },
              { t: 5.0, targetGx: 14.5, targetGy: 4.5, ball: 'target', status: '아크 정면까지 35m 전진 드리블 완료', metric: '전진 캐리 성공' },
              { t: 8.0, targetGx: 15.5, targetGy: 5.2, ball: 'target', status: '위협적인 유효 슈팅 연결로 코너킥 획득', metric: '슈팅 창출' }
            ]
          }
        ];
      }

      // 2) 이강인 시그니처
      if (name.includes('이강인') || p.name.includes('Kang-in')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: '킬패스',
            title: `[La Pausa 스루패스] 수비 라인 찢는 35m 핀포인트 킬러 패스`,
            desc: `상대 미드필더 2명을 끌어당기며 템포를 조절한 뒤 침투하는 공격수에게 배달된 레이저 패스 (키패스 90분당 ${kp}회 상위 5%)`,
            phases: [
              { t: 0.0, targetGx: 8.5, targetGy: 4.0, ball: 'target', status: '볼을 밟으며 템포 조절 (La Pausa)', metric: '압박 유인 중' },
              { t: 2.5, targetGx: 9.2, targetGy: 4.8, ball: 'target', status: '상대 수비수 2명의 압박을 등지고 시야 확보', metric: '시야각(FOV) 전방 120° 개방' },
              { t: 4.8, targetGx: 9.8, targetGy: 5.0, ball: 'pass', passTarget: { gx: 15.2, gy: 5.8 }, status: '🎯 수비수 3명 사이 빈틈을 가르는 35m 킬패스 투입!', metric: `전진 패스 지표: 상위 2%` },
              { t: 6.5, targetGx: 10.2, targetGy: 5.0, ball: 'receive', status: '침투한 공격수가 완벽한 1:1 찬스에서 볼 리시브', metric: 'xA: 0.42 기대 어시스트' },
              { t: 8.0, targetGx: 10.5, targetGy: 5.0, ball: 'goal', status: '침투 공격수의 침착한 마무리로 득점 완성!', metric: '빅찬스 생성 완료' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '탈압박',
            title: `[바디페인팅 턴] 2인 압박 무력화 & 반대편 40m 대각선 전환`,
            desc: `상대의 강한 전방 압박을 특유의 상체 페인팅 턴으로 벗겨낸 뒤 비어있는 반대편으로 단숨에 전환하는 플레이메이킹`,
            phases: [
              { t: 0.0, targetGx: 7.5, targetGy: 8.5, ball: 'target', status: '터치라인 부근에서 상대 2명의 샌드위치 압박 직면', metric: '압박 강도 95%' },
              { t: 2.2, targetGx: 7.2, targetGy: 7.5, ball: 'target', status: '몸을 회전하며 상체 페인팅으로 수비수 무게중심 붕괴', metric: '탈압박 성공 (100%)' },
              { t: 4.5, targetGx: 8.2, targetGy: 6.8, ball: 'target', status: '중원으로 빠져나오며 반대편 오픈 공간 탐색', metric: 'xGBuildup: 0.68 기여' },
              { t: 6.0, targetGx: 8.5, targetGy: 6.8, ball: 'pass', passTarget: { gx: 13.0, gy: 2.0 }, status: '📐 반대편 윙어를 향한 정확한 40m 대각선 롱 체인지 패스!', metric: '전환 패스 성공' },
              { t: 8.0, targetGx: 8.8, targetGy: 6.8, ball: 'finish', status: '반대편 측면에서 즉각적인 크로스 찬스로 연결', metric: '공격 전개 완성' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '득점',
            title: `[아크 정면 왼발 프리킥/중거리포] 골문 상단 구석 궤적골`,
            desc: `박스 바깥 아크 정면에서 수비 벽을 넘겨 골키퍼 손이 닿지 않는 상단 구석을 찌르는 정밀 왼발 슈팅`,
            phases: [
              { t: 0.0, targetGx: 12.0, targetGy: 5.5, ball: 'target', status: '아크 정면 좋은 위치에서 볼 소유', metric: '슈팅 거리 22m' },
              { t: 2.5, targetGx: 12.8, targetGy: 5.2, ball: 'target', status: '왼발 슈팅 각도를 만들기 위한 한 박자 터치', metric: '각도 45° 정렬' },
              { t: 4.8, targetGx: 13.2, targetGy: 5.0, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 환상적인 궤적으로 휘어 들어가는 왼발 슈팅!', metric: `xG: ${xg} 정밀 타격` },
              { t: 8.0, targetGx: 13.2, targetGy: 5.0, ball: 'goal', status: '⚽ 크로스바 하단을 맞고 골망을 흔드는 원더골!', metric: '득점 성공' }
            ]
          }
        ];
      }

      // 3) 김민재 시그니처
      if (name.includes('김민재') || p.name.includes('Min-Jae') || p.name.includes('van Dijk')) {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '스토퍼 태클',
            title: `[스토퍼 전진 인터셉트 & 롱패스] 상대 역습 차단 & 45m 다이렉트 배달`,
            desc: `상대 패스 길목을 예측하여 라인을 깨고 전진해 볼을 가로챈 뒤, 반대편 공격수 발밑으로 45m 전진 롱패스 (전진패스 90분당 ${kp}회 상위 3%)`,
            phases: [
              { t: 0.0, targetGx: 4.5, targetGy: 5.5, ball: 'away', status: '상대 공격진의 역습 전개 및 전진 패스 시도', metric: '위험 지역 차단 모드' },
              { t: 2.2, targetGx: 6.8, targetGy: 5.8, ball: 'target', status: '🛡️ 과감한 전진 스텝으로 상대 패스 완벽 인터셉트!', metric: `대인 경합 승리율: ${defPct}%` },
              { t: 4.2, targetGx: 7.2, targetGy: 5.6, ball: 'target', status: '탈환 후 고개를 들어 전방 빈 공간 포착', metric: '빌드업 시야 확보' },
              { t: 5.8, targetGx: 7.5, targetGy: 5.5, ball: 'pass', passTarget: { gx: 14.5, gy: 2.5 }, status: '🚀 전방 윙어를 향해 정확히 꽂히는 45m 레이저 롱패스!', metric: '전진 패스 성공 (상위 3%)' },
              { t: 8.0, targetGx: 6.5, targetGy: 5.5, ball: 'finish', status: '단숨에 우리 팀의 결정적인 득점 기회로 전환!', metric: '공수 전환 성공' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '커버 태클',
            title: `[괴물 피지컬 리커버리] 1:1 결정적 슬라이딩 태클 슈퍼세이브`,
            desc: `뒷공간으로 쇄도하는 상대 공격수를 압도적인 주력으로 추격하여 박스 진입 직전 공만 걷어내는 완벽한 태클`,
            phases: [
              { t: 0.0, targetGx: 5.5, targetGy: 7.0, ball: 'away', status: '상대 윙어의 뒷공간 단독 돌파 발생', metric: '추격 속도: 22.0 km/h' },
              { t: 2.5, targetGx: 4.0, targetGy: 6.5, ball: 'away', status: '순간 속도 34.0km/h로 전력 질주하며 각도 좁히기', metric: '속도: 34.1 km/h 스프린트' },
              { t: 4.8, targetGx: 2.8, targetGy: 6.0, ball: 'target', status: '⚔️ 위험 지역 진입 직전 오차 없는 슬라이딩 태클 성공!', metric: '클리어링 100%' },
              { t: 8.0, targetGx: 3.2, targetGy: 6.0, ball: 'target', status: '위기를 완벽히 탈출하며 동료 골키퍼에게 안정적 연결', metric: '위기 소멸' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '세트피스',
            title: `[타점 높은 제공권 헤더] 코너킥 상황 압도적 타점 헤더 골`,
            desc: `코너킥 상황에서 상대 수비수 2명을 힘으로 누르고 타점 높은 헤더로 골망을 가르는 세트피스 득점`,
            phases: [
              { t: 0.0, targetGx: 14.0, targetGy: 5.0, ball: 'corner', status: '코너 플래그에서 크로스 준비', metric: '세트피스 전술 대형' },
              { t: 2.5, targetGx: 15.5, targetGy: 5.5, ball: 'corner_flight', status: '수비수를 따돌리며 박스 중앙으로 강력한 쇄도', metric: '제공권 경합 준비' },
              { t: 4.8, targetGx: 16.5, targetGy: 5.5, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.3 }, status: '💥 타점 높은 점프로 골문 구석을 찌르는 헤더 강타!', metric: `헤더 경합 승리율 78%` },
              { t: 8.0, targetGx: 16.5, targetGy: 5.5, ball: 'goal', status: '⚽ 골키퍼 손을 스치며 골망을 가르는 득점 완성!', metric: '세트피스 득점' }
            ]
          }
        ];
      }

      // 4) 엘링 홀란드 시그니처 (Box Finisher)
      if (name.includes('Haaland') || archetype.includes('타점·결정력 집중형 스트라이커')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '원터치 피니시',
            title: `[라인 침투 맹폭] 센터백 사이 공간 침투 & 원터치 피니시`,
            desc: `라인 침투 패스 리시브 8.3회(상위 11%)를 증명하는 번개같은 침투와 골문 구석 원터치 마무리 (xG ${xg})`,
            phases: [
              { t: 0.0, targetGx: 12.5, targetGy: 5.5, ball: 'mid', status: '상대 센터백 2명 사이에서 오프사이드 라인 주시', metric: '스프린트 타이밍 조율' },
              { t: 2.2, targetGx: 14.8, targetGy: 5.2, ball: 'pass_flight', status: '⚡ 수비수 어깨를 누르며 폭발적으로 뒷공간 쇄도!', metric: '속도: 34.8 km/h' },
              { t: 4.5, targetGx: 16.2, targetGy: 5.5, ball: 'target', status: '전방 스루패스를 완벽하게 발밑에 터치', metric: '리시브 성공' },
              { t: 5.6, targetGx: 16.5, targetGy: 5.5, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.8 }, status: '💥 골문 구석으로 벼락같은 논스톱 강슛!', metric: `xG: ${xg} 확실한 결정력` },
              { t: 8.0, targetGx: 16.8, targetGy: 5.5, ball: 'goal', status: '⚽ 골문 그물을 찢을 듯한 완벽한 득점!!', metric: 'G+A 0.82/90 상위 6%' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '타점 피니시',
            title: `[박스 안 피지컬 타점] 크로스를 밀어 넣는 공중제비 발리`,
            desc: `측면 크로스 상황에서 상대 센터백과의 몸싸움을 완벽히 이겨내고 타점 높은 발리로 마무리`,
            phases: [
              { t: 0.0, targetGx: 13.5, targetGy: 4.0, ball: 'wing', status: '측면 풀백의 크로스 타이밍 감지', metric: '박스 안 자리싸움' },
              { t: 2.5, targetGx: 15.8, targetGy: 4.8, ball: 'cross', status: '상대 수비를 힘으로 밀어내며 니어포스트 쇄도', metric: '피지컬 우위' },
              { t: 4.8, targetGx: 16.8, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.1 }, status: '💥 허공에서 발을 뻗어 문전으로 꽂아 넣는 아크로바틱 피니시!', metric: '유효슈팅' },
              { t: 8.0, targetGx: 16.8, targetGy: 5.2, ball: 'goal', status: '골키퍼가 반응조차 하지 못한 원더골!', metric: '득점 완성' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '돌파',
            title: `[괴물 폭주 돌파] 하프라인 볼 탈환 후 30m 단독 불도저 질주`,
            desc: `상대 볼을 끊어낸 뒤 압도적인 피지컬과 속도로 수비수를 밀쳐내며 박스까지 도달`,
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 6.0, ball: 'target', status: '경합 상황에서 공을 몸으로 소유', metric: '볼 소유 안정' },
              { t: 3.0, targetGx: 13.0, targetGy: 5.5, ball: 'target', status: '상대 수비수의 어깨 싸움을 버텨내며 직진 돌파', metric: '속도: 33.2 km/h' },
              { t: 5.5, targetGx: 15.5, targetGy: 5.2, ball: 'target', status: '골키퍼와 1:1 찬스 직면', metric: '슈팅 각 확보' },
              { t: 8.0, targetGx: 16.0, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.0 }, status: '강력한 슈팅으로 코너킥 찬스 창출', metric: '찬스 창출' }
            ]
          }
        ];
      }

      // 5) 로드리 시그니처 (Press-Resistant Pivot)
      if (name.includes('Rodri') || archetype.includes('탈압박형 수비형 미드필더')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: '빌드업 조율',
            title: `[후방 1차 탈압박 기점] 상대 전방 압박 무력화 & 35m 전진 배급`,
            desc: `대인 수비 경합 승리율 64%(상위 1%)와 xGBuildup 0.8(상위 3%)을 증명하는 완벽한 피벗 플레이`,
            phases: [
              { t: 0.0, targetGx: 6.0, targetGy: 6.0, ball: 'target', status: '상대 공격수 2명의 강한 전방 압박을 등지고 볼 수신', metric: '경합 승리율: 64%' },
              { t: 2.2, targetGx: 6.5, targetGy: 5.2, ball: 'target', status: '원터치 턴으로 상대 압박 라인을 완전히 무력화', metric: '탈압박 성공 (상위 1%)' },
              { t: 4.5, targetGx: 7.2, targetGy: 5.5, ball: 'pass', passTarget: { gx: 12.5, gy: 2.5 }, status: '📐 전방 윙어를 향해 정확한 중장거리 전진 패스 배급!', metric: '전진 패스: 6.15회/90' },
              { t: 8.0, targetGx: 7.8, targetGy: 5.5, ball: 'finish', status: '팀 전체의 공격 템포를 한 단계 끌어올리는 완벽한 기점', metric: 'xGBuildup: 0.80 상위 3%' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '중거리 원더골',
            title: `[아크 정면 세컨볼 레이저포] 박스 밖 25m 논스톱 중거리포 득점`,
            desc: `상대 수비가 걷어낸 세컨볼을 지체 없이 오른발 인스텝으로 감아 차 골대 구석을 찌르는 중거리포`,
            phases: [
              { t: 0.0, targetGx: 11.0, targetGy: 6.0, ball: 'clear', status: '상대 수비가 박스 밖으로 걷어낸 공 감지', metric: '세컨볼 낙하지점 포착' },
              { t: 2.5, targetGx: 12.2, targetGy: 5.8, ball: 'target', status: '공의 바운드를 맞추며 슈팅 타이밍 정렬', metric: '무게중심 안착' },
              { t: 4.8, targetGx: 12.8, targetGy: 5.8, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 낮고 빠르게 깔려 들어가는 오른발 대포알 중거리 슈팅!', metric: '슈팅 속도: 112 km/h' },
              { t: 8.0, targetGx: 13.0, targetGy: 5.8, ball: 'goal', status: '⚽ 수비수들 틈을 뚫고 골망 구석을 흔드는 원더골!', metric: '골인!' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '볼위닝',
            title: `[하프라인 완벽한 볼위닝] 대인 경합 승리 & 즉각적인 역습 개시`,
            desc: `상대의 중원 역습 전개를 거친 몸싸움으로 제압하여 볼을 탈환한 뒤 전방으로 즉각 배급`,
            phases: [
              { t: 0.0, targetGx: 8.0, targetGy: 6.5, ball: 'away', status: '상대 공격형 미드필더의 턴 시도 포착', metric: '압박 개시' },
              { t: 2.5, targetGx: 8.5, targetGy: 6.2, ball: 'target', status: '🛡️ 강력한 어깨 싸움으로 파울 없이 볼 완벽 탈환!', metric: '경합 승리 (64%)' },
              { t: 5.0, targetGx: 9.0, targetGy: 5.8, ball: 'pass', passTarget: { gx: 13.5, gy: 8.5 }, status: '탈환 즉시 침투하는 윙어에게 원터치 스루패스 투입', metric: '역습 개시' },
              { t: 8.0, targetGx: 9.2, targetGy: 5.8, ball: 'finish', status: '위기를 기회로 바꾼 결정적 수비 공헌', metric: '수비 기여 완료' }
            ]
          }
        ];
      }

      // 6) 일반 포지션/아키타입 범용 고유 모션 (다른 모든 선수 대상)
      if (pos === 'CB' || pos === 'LB' || pos === 'RB') {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '수비 인터셉트',
            title: `[포지션 정밀 수비] 상대 침투 패스 예측 차단 & 40m 빌드업`,
            desc: `DB 실측 경합 승리율 ${defPct}%를 기반으로 한 오차 없는 차단 및 전방 빌드업 배급`,
            phases: [
              { t: 0.0, targetGx: 4.5, targetGy: 5.0, ball: 'away', status: '수비 라인 정렬 및 상대 패스 대기', metric: `경합률: ${defPct}%` },
              { t: 2.5, targetGx: 6.2, targetGy: 5.2, ball: 'target', status: '전진 가로채기 성공', metric: '볼 소유권 탈환' },
              { t: 5.0, targetGx: 6.8, targetGy: 5.2, ball: 'pass', passTarget: { gx: 13.0, gy: 3.0 }, status: '측면으로 열어주는 정확한 빌드업 패스', metric: '패스 성공' },
              { t: 8.0, targetGx: 6.8, targetGy: 5.2, ball: 'finish', status: '공격 전개 안정화', metric: '빌드업 완성' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '1:1 차단',
            title: `[박스 안 결정적 블록] 상대 슈팅 궤적을 몸으로 막아내는 육탄 방어`,
            desc: `상대의 위협적인 유효 슈팅 코스를 슬라이딩 블록으로 걷어내는 결정적 수비`,
            phases: [
              { t: 0.0, targetGx: 4.0, targetGy: 6.0, ball: 'away', status: '상대 공격수의 박스 침투 감지', metric: '위험 차단' },
              { t: 2.8, targetGx: 3.2, targetGy: 5.8, ball: 'target', status: '슈팅 각도를 좁히며 몸을 날리는 슬라이딩 블록', metric: '블록 성공' },
              { t: 5.5, targetGx: 3.0, targetGy: 5.8, ball: 'clear', status: '터치라인 밖으로 안전하게 걷어내기', metric: '위기 모면' },
              { t: 8.0, targetGx: 3.0, targetGy: 5.8, ball: 'finish', status: '실점 위기 방어 완료', metric: '클리어링' }
            ]
          },
          {
            type: 'PASS', tag: 'pass', tagText: '전진 패스',
            title: `[후방 롱 빌드업] 반대편 공간을 찢는 대각선 전환 패스`,
            desc: `후방에서 상대 압박을 피해 반대편 풀백의 발밑으로 정확히 배달되는 롱패스`,
            phases: [
              { t: 0.0, targetGx: 3.8, targetGy: 4.0, ball: 'target', status: '후방에서 볼 소유 및 압박 관찰', metric: '시야 확보' },
              { t: 2.5, targetGx: 4.2, targetGy: 4.5, ball: 'target', status: '전방 선수들의 움직임 확인', metric: '패스길 선택' },
              { t: 5.0, targetGx: 4.5, targetGy: 4.8, ball: 'pass', passTarget: { gx: 12.0, gy: 9.0 }, status: '📐 반대편 측면으로 날카로운 롱패스 전개', metric: '전진 패스 성공' },
              { t: 8.0, targetGx: 4.5, targetGy: 4.8, ball: 'finish', status: '측면 공격 기회 창출', metric: '전개 완료' }
            ]
          }
        ];
      }

      // 기본 미드필더/공격수
      return [
        {
          type: 'GOAL', tag: 'goal', tagText: '득점',
          title: `[시그니처 결정력] 박스 침투 원터치 피니시 득점 (xG ${xg})`,
          desc: `상대 수비 틈새를 파고들어 정교한 원터치 슈팅으로 골망을 가르는 득점`,
          phases: [
            { t: 0.0, targetGx: 11.5, targetGy: 5.0, ball: 'mid', status: '패스 전개를 기다리며 침투 각도 조율', metric: '오프더볼' },
            { t: 2.5, targetGx: 14.0, targetGy: 5.2, ball: 'pass_flight', status: '수비 뒷공간으로 순간 가속 침투', metric: '속도: 29.5 km/h' },
            { t: 4.8, targetGx: 15.5, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.5 }, status: '💥 골문 구석으로 정확한 원터치 슈팅!', metric: `xG: ${xg}` },
            { t: 8.0, targetGx: 15.8, targetGy: 5.2, ball: 'goal', status: '⚽ 침착한 마무리로 득점 성공!', metric: '골인' }
          ]
        },
        {
          type: 'PASS', tag: 'pass', tagText: '찬스메이킹',
          title: `[날카로운 키패스] 수비 라인 사이 공간을 가르는 스루패스 (KP ${kp}회)`,
          desc: `상대 수비 라인의 균열을 포착하고 침투하는 동료 발밑에 찔러준 결정적 패스`,
          phases: [
            { t: 0.0, targetGx: 9.0, targetGy: 5.0, ball: 'target', status: '중원에서 볼 소유 및 패스길 탐색', metric: '키패스 준비' },
            { t: 2.5, targetGx: 9.8, targetGy: 5.2, ball: 'target', status: '동료의 침투 타이밍에 맞춰 한 박자 킬패스', metric: `키패스 90분당 ${kp}회` },
            { t: 5.0, targetGx: 10.2, targetGy: 5.2, ball: 'pass', passTarget: { gx: 15.0, gy: 3.5 }, status: '🎯 뒷공간을 향한 핀포인트 스루패스!', metric: '패스 성공' },
            { t: 8.0, targetGx: 10.5, targetGy: 5.2, ball: 'finish', status: '동료의 완벽한 슈팅 찬스로 연결', metric: '찬스메이킹 완료' }
          ]
        },
        {
          type: 'DRIBBLE', tag: 'dribble', tagText: '돌파',
          title: `[탈압박 전진] 1:1 대인 돌파 후 박스 진입`,
          desc: `순간적인 방향 전환으로 상대 마크맨을 제치고 공격 공간을 열어내는 전진 드리블`,
          phases: [
            { t: 0.0, targetGx: 10.0, targetGy: 3.0, ball: 'target', status: '측면에서 볼을 잡고 수비수와 1:1 대치', metric: '드리블 개시' },
            { t: 2.8, targetGx: 12.5, targetGy: 3.8, ball: 'target', status: '바디페인팅으로 수비수를 완전히 제쳐냄', metric: '돌파 성공' },
            { t: 5.5, targetGx: 14.2, targetGy: 4.5, ball: 'target', status: '박스 안쪽으로 진입하며 컷백 준비', metric: '위험 지역 진입' },
            { t: 8.0, targetGx: 14.8, targetGy: 4.8, ball: 'pass', passTarget: { gx: 15.5, gy: 6.0 }, status: '중앙 동료에게 안전한 컷백 연결', metric: '전개 완료' }
          ]
        }
      ];
    }

    // =========================================================================
    // 3. 22명 전원의 팀 전술 대형 및 상호작용 피직스 (난수 0% 결정론적 엔진)
    // =========================================================================
    // 기본 4-2-3-1 (홈 파랑) vs 4-3-3 (어웨이 빨강)
    const BASE_HOME_11 = [
      { id: 'H1',  pos: 'GK', gx: 0.8,  gy: 6.0, name: 'GK' },
      { id: 'H2',  pos: 'RB', gx: 3.5,  gy: 1.8, name: 'RB' },
      { id: 'H3',  pos: 'CB', gx: 3.0,  gy: 4.2, name: 'CB' },
      { id: 'H4',  pos: 'CB', gx: 3.0,  gy: 7.8, name: 'CB' },
      { id: 'H5',  pos: 'LB', gx: 3.5,  gy: 10.2,name: 'LB' },
      { id: 'H6',  pos: 'DM', gx: 6.5,  gy: 4.5, name: 'DM' },
      { id: 'H7',  pos: 'DM', gx: 6.5,  gy: 7.5, name: 'DM' },
      { id: 'H8',  pos: 'RW', gx: 10.5, gy: 2.5, name: 'RW' },
      { id: 'H9',  pos: 'AM', gx: 9.8,  gy: 6.0, name: 'AM' },
      { id: 'H10', pos: 'LW', gx: 10.5, gy: 9.5, name: 'LW' },
      { id: 'H11', pos: 'ST', gx: 13.5, gy: 6.0, name: 'ST' },
    ];

    const BASE_AWAY_11 = [
      { id: 'A1',  pos: 'GK', gx: 17.2, gy: 6.0, name: 'GK' },
      { id: 'A2',  pos: 'RB', gx: 14.5, gy: 10.2,name: 'RB' },
      { id: 'A3',  pos: 'CB', gx: 15.0, gy: 7.5, name: 'CB' },
      { id: 'A4',  pos: 'CB', gx: 15.0, gy: 4.5, name: 'CB' },
      { id: 'A5',  pos: 'LB', gx: 14.5, gy: 1.8, name: 'LB' },
      { id: 'A6',  pos: 'DM', gx: 11.5, gy: 6.0, name: 'DM' },
      { id: 'A7',  pos: 'CM', gx: 9.5,  gy: 7.8, name: 'CM' },
      { id: 'A8',  pos: 'CM', gx: 9.5,  gy: 4.2, name: 'CM' },
      { id: 'A9',  pos: 'RW', gx: 7.5,  gy: 9.5, name: 'RW' },
      { id: 'A10', pos: 'LW', gx: 7.5,  gy: 2.5, name: 'LW' },
      { id: 'A11', pos: 'ST', gx: 5.5,  gy: 6.0, name: 'ST' },
    ];

    function calculate22Positions(action, t) {
      const phases = action.phases;
      // 현재 t에 해당하는 phase 보간
      let pA = phases[0];
      let pB = phases[phases.length - 1];
      for (let i = 0; i < phases.length - 1; i++) {
        if (t >= phases[i].t && t <= phases[i + 1].t) {
          pA = phases[i];
          pB = phases[i + 1];
          break;
        }
      }

      const ratio = pB.t === pA.t ? 0 : Math.max(0, Math.min(1, (t - pA.t) / (pB.t - pA.t)));
      // 부드러운 스무스스텝 보간
      const smooth = ratio * ratio * (3 - 2 * ratio);

      // 1. 주인공 선수 좌표 계산
      const heroGx = pA.targetGx + (pB.targetGx - pA.targetGx) * smooth;
      const heroGy = pA.targetGy + (pB.targetGy - pA.targetGy) * smooth;

      // 2. 볼 좌표 계산
      let ballGx = heroGx + 0.2;
      let ballGy = heroGy;

      if (pA.ball === 'shot' || pB.ball === 'shot') {
        const shotTarget = pB.shotTarget || { gx: 18.0, gy: 6.0 };
        ballGx = heroGx + (shotTarget.gx - heroGx) * smooth;
        ballGy = heroGy + (shotTarget.gy - heroGy) * smooth;
      } else if (pA.ball === 'pass' || pB.ball === 'pass') {
        const passTarget = pB.passTarget || { gx: 15.0, gy: 6.0 };
        ballGx = heroGx + (passTarget.gx - heroGx) * smooth;
        ballGy = heroGy + (passTarget.gy - heroGy) * smooth;
      } else if (pA.ball === 'goal' || pB.ball === 'goal') {
        ballGx = 18.0;
        ballGy = (pB.shotTarget ? pB.shotTarget.gy : 6.0);
      }

      // 3. 나머지 21명 선수의 전술 반응 (라인 시프트, 침투, 압박)
      // 볼 전진도에 따라 상대 수비 라인은 뒤로 물러서고, 아군 라인은 올라감
      const shiftX = (ballGx - 9.0) * 0.45;
      const shiftY = (ballGy - 6.0) * 0.35;

      const homePlayers = BASE_HOME_11.map((p, idx) => {
        if (idx === 0) {
          // 주인공 선수는 8번 슬롯(LW/AM/RW/ST 대체)에 매핑
          return { ...p, gx: heroGx, gy: heroGy, isHero: true, name: currentPlayer.name_ko || currentPlayer.name };
        }
        // 나머지 아군: 볼 진행 방향으로 유기적 서포트 침투 및 라인 전진
        let gx = p.gx + shiftX;
        let gy = p.gy + shiftY * 0.6;
        if (p.pos === 'ST' && !action.title.includes('손흥민')) {
          // 공격수는 배후 침투
          gx += Math.min(2.5, smooth * 3.0);
        }
        if (p.pos === 'RB' || p.pos === 'LB') {
          // 풀백 오버래핑
          gx += Math.min(2.0, smooth * 2.2);
        }
        return { ...p, gx: Math.max(0.5, Math.min(17.5, gx)), gy: Math.max(0.8, Math.min(11.2, gy)), isHero: false };
      });

      const awayPlayers = BASE_AWAY_11.map(p => {
        // 상대 수비: 볼 쪽으로 압박 및 오프사이드 라인 조율
        let gx = p.gx + shiftX * 0.6;
        let gy = p.gy + shiftY * 0.7;

        // 볼 소유자와 가까운 센터백/수미 2명은 적극 압박 전진
        const dist = Math.hypot(p.gx - heroGx, p.gy - heroGy);
        if (dist < 4.0 && p.pos !== 'GK') {
          gx += (heroGx - p.gx) * 0.45;
          gy += (heroGy - p.gy) * 0.45;
        }

        // 골키퍼는 슈팅 각도 좁히기
        if (p.pos === 'GK') {
          gx = 17.2 - Math.min(1.2, (ballGx / 18.0) * 1.5);
          gy = 6.0 + (ballGy - 6.0) * 0.25;
        }

        return { ...p, gx: Math.max(0.5, Math.min(17.8, gx)), gy: Math.max(0.8, Math.min(11.2, gy)) };
      });

      return {
        hero: { gx: heroGx, gy: heroGy },
        ball: { gx: ballGx, gy: ballGy },
        home: homePlayers,
        away: awayPlayers,
        currentPhase: pB
      };
    }

    // =========================================================================
    // 4. 화면 렌더링 루프
    // =========================================================================
    function renderPitch() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 피치 외곽 테두리
      ctx.fillStyle = '#062817';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // 체커보드 바둑판 잔디 타일
      const cols = 18;
      const rows = 12;
      const cellW = PITCH_W / cols;
      const cellH = PITCH_H / rows;

      for (let c = 0; c < cols; c++) {
        for (let r = 0; r < rows; r++) {
          const isEven = (c + r) % 2 === 0;
          ctx.fillStyle = isEven ? '#0f4225' : '#124d2c';
          ctx.fillRect(MARGIN + c * cellW, MARGIN + r * cellH, cellW, cellH);
        }
      }

      // 바둑판 격자 라인
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let c = 0; c <= cols; c++) {
        ctx.beginPath();
        ctx.moveTo(MARGIN + c * cellW, MARGIN);
        ctx.lineTo(MARGIN + c * cellW, MARGIN + PITCH_H);
        ctx.stroke();
      }
      for (let r = 0; r <= rows; r++) {
        ctx.beginPath();
        ctx.moveTo(MARGIN, MARGIN + r * cellH);
        ctx.lineTo(MARGIN + PITCH_W, MARGIN + r * cellH);
        ctx.stroke();
      }

      // 정규 축구장 라인 (센터서클, 페널티박스, 골라인)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.55)';
      ctx.lineWidth = 2;
      ctx.strokeRect(MARGIN, MARGIN, PITCH_W, PITCH_H);

      // 센터라인 & 센터서클
      ctx.beginPath();
      ctx.moveTo(MARGIN + PITCH_W / 2, MARGIN);
      ctx.lineTo(MARGIN + PITCH_W / 2, MARGIN + PITCH_H);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(MARGIN + PITCH_W / 2, MARGIN + PITCH_H / 2, 60, 0, Math.PI * 2);
      ctx.stroke();

      // 좌우 페널티 박스
      const boxW = cellW * 3;
      const boxH = cellH * 6;
      const boxY = MARGIN + (PITCH_H - boxH) / 2;
      ctx.strokeRect(MARGIN, boxY, boxW, boxH);
      ctx.strokeRect(MARGIN + PITCH_W - boxW, boxY, boxW, boxH);

      // 골문
      ctx.strokeRect(MARGIN - 10, boxY + boxH * 0.3, 10, boxH * 0.4);
      ctx.strokeRect(MARGIN + PITCH_W, boxY + boxH * 0.3, 10, boxH * 0.4);

      if (!currentPlayer) return;

      const actions = generatePlayerActions(currentPlayer);
      const action = actions[currentActionIdx] || actions[0];
      const state = calculate22Positions(action, currentTime);

      // 시야각(FOV) 부채꼴 시각화 (주인공 선수)
      const heroPt = toPixel(state.hero.gx, state.hero.gy);
      ctx.save();
      const fovAngle = (state.hero.gx > 9) ? 0 : 0;
      ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
      ctx.beginPath();
      ctx.moveTo(heroPt.x, heroPt.y);
      ctx.arc(heroPt.x, heroPt.y, 110, -0.4, 0.4);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 패스/슈팅 궤적 렌더링
      const ballPt = toPixel(state.ball.gx, state.ball.gy);
      if (Math.hypot(heroPt.x - ballPt.x, heroPt.y - ballPt.y) > 15) {
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(heroPt.x, heroPt.y);
        ctx.lineTo(ballPt.x, ballPt.y);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // 22명 선수 렌더링 (바둑알)
      // 1) 어웨이 선수 (빨강)
      state.away.forEach(p => {
        const pt = toPixel(p.gx, p.gy);
        ctx.fillStyle = '#dc2626';
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fca5a5';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 9px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.pos, pt.x, pt.y);
      });

      // 2) 홈 선수 (파랑)
      state.home.forEach(p => {
        const pt = toPixel(p.gx, p.gy);
        if (p.isHero) {
          // 주인공 선수: 화려한 금빛 테두리 + 하이라이트 펄스
          ctx.save();
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 18;
          ctx.fillStyle = '#2563eb';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 16, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 3.5;
          ctx.stroke();
          ctx.restore();

          // 이름 뱃지
          ctx.fillStyle = '#fff';
          ctx.font = '900 11px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(p.name.slice(0, 3), pt.x, pt.y);

          // 상단 왕관 마커
          ctx.fillStyle = '#fbbf24';
          ctx.font = 'bold 12px sans-serif';
          ctx.fillText('★', pt.x, pt.y - 20);
        } else {
          ctx.fillStyle = '#2563eb';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 12, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#93c5fd';
          ctx.lineWidth = 1.5;
          ctx.stroke();

          ctx.fillStyle = '#fff';
          ctx.font = 'bold 9px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(p.pos, pt.x, pt.y);
        }
      });

      // 축구공 렌더링
      ctx.save();
      ctx.shadowColor = '#000';
      ctx.shadowBlur = 8;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(ballPt.x, ballPt.y, 6.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#000000';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.restore();

      // HUD 업데이트
      const phase = state.currentPhase;
      document.getElementById('hudActionText').innerText = phase.status || action.title;
      document.getElementById('hudMetricText').innerText = phase.metric || `진행: ${currentTime.toFixed(1)}s`;
      document.getElementById('timeLabel').innerText = `${currentTime.toFixed(1)}s / ${TOTAL_DURATION.toFixed(1)}s`;
      document.getElementById('timeSlider').value = currentTime;
    }

    // =========================================================================
    // 5. 시뮬레이션 루프 & 컨트롤러
    // =========================================================================
    let lastTime = performance.now();
    function animationLoop(now) {
      const dt = (now - lastTime) / 1000;
      lastTime = now;

      if (isPlaying) {
        currentTime += dt * playbackSpeed;
        if (currentTime >= TOTAL_DURATION) {
          currentTime = 0; // 자동 무한 루프
        }
      }

      renderPitch();
      requestAnimationFrame(animationLoop);
    }

    function togglePlay() {
      isPlaying = !isPlaying;
      const btn = document.getElementById('btnPlayPause');
      btn.innerText = isPlaying ? '⏸ 일시정지' : '▶ 재생';
      btn.className = isPlaying ? 't-btn play' : 't-btn';
    }

    function setSpeed(spd) {
      playbackSpeed = spd;
      document.querySelectorAll('.timeline-bar .t-btn').forEach(b => {
        if (b.innerText.includes(`${spd.toFixed(1)}x`) || b.innerText.includes(`${spd}x`)) {
          b.classList.add('active');
        } else if (b.innerText.includes('x')) {
          b.classList.remove('active');
        }
      });
    }

    function resetCurrentAction() {
      currentTime = 0;
    }

    function onSeekTime(val) {
      currentTime = parseFloat(val);
      renderPitch();
    }

    function selectAction(idx) {
      currentActionIdx = idx;
      currentTime = 0;
      updateActionCardsUI();
      renderPitch();
    }

    function updateActionCardsUI() {
      const cards = document.querySelectorAll('.action-card');
      cards.forEach((c, idx) => {
        if (idx === currentActionIdx) c.classList.add('active');
        else c.classList.remove('active');
      });
    }

    // =========================================================================
    // 6. 선수 변경 및 UI 동기화
    // =========================================================================
    function onSelectPlayer(playerId) {
      const p = PLAYERS_DATABASE.find(item => String(item.player_id) === String(playerId));
      if (!p) return;
      currentPlayer = p;
      currentActionIdx = 0;
      currentTime = 0;

      // 1) 좌측 프로필 카드 갱신 (DB 실측 값 반영)
      document.getElementById('pCardName').innerText = p.name_ko || p.name;
      document.getElementById('pCardPos').innerText = p.position || 'ST';
      document.getElementById('pCardClub').innerText = `${p.current_club || '소속팀 미상'} · ${p.league || ''}`;
      document.getElementById('pCardArchetype').innerText = p.tactical_archetype || '전술 스페셜리스트';
      document.getElementById('pCardStrengths').innerText = p.strengths_tags || '탁월한 경기 영향력 및 실측 데이터 우수';

      document.getElementById('pStatGoals').innerText = p.goals_per90 ? `${p.goals_per90.toFixed(2)}골` : '-';
      document.getElementById('pStatXg').innerText = p.xg_per90 ? `${p.xg_per90.toFixed(2)}` : '-';
      document.getElementById('pStatKp').innerText = p.key_passes_per90 ? `${p.key_passes_per90.toFixed(1)}회` : '-';
      document.getElementById('pStatProg').innerText = p.progressive_actions_per90 ? `${p.progressive_actions_per90.toFixed(1)}회` : '-';
      document.getElementById('pStatDef').innerText = p.defensive_duels_won_pct ? `${p.defensive_duels_won_pct.toFixed(0)}%` : '-';
      document.getElementById('pStatPctl').innerText = p.pos_percentile ? `상위 ${100 - p.pos_percentile}%` : '상위권';

      // 2) 유튜브 버튼 연동
      const ytId = YT_MAP[p.name_ko] || YT_MAP[p.name] || 'YhEcyglkOx0';
      document.getElementById('ytSyncBtn').href = `https://www.youtube.com/watch?v=${ytId}`;

      // 3) 우측 고유 액션 리스트 생성
      const actions = generatePlayerActions(p);
      const listContainer = document.getElementById('actionList');
      listContainer.innerHTML = '';

      actions.forEach((act, idx) => {
        const div = document.createElement('div');
        div.className = `action-card ${idx === 0 ? 'active' : ''}`;
        div.onclick = () => selectAction(idx);
        div.innerHTML = `
          <span class="act-tag ${act.tag}">${act.tagText}</span>
          <div class="act-title">${act.title}</div>
          <div class="act-desc">${act.desc}</div>
        `;
        listContainer.appendChild(div);
      });

      renderPitch();
    }

    // 초기화
    function init() {
      const select = document.getElementById('playerSelect');
      PLAYERS_DATABASE.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.player_id;
        opt.innerText = `${p.name_ko || p.name} (${p.position}) — ${p.current_club || ''}`;
        select.appendChild(opt);
      });

      // 기본 선택: 손흥민 또는 첫 번째 선수
      const defaultPlayer = PLAYERS_DATABASE.find(p => (p.name_ko && p.name_ko.includes('손흥민')) || p.name.includes('Son')) || PLAYERS_DATABASE[0];
      select.value = defaultPlayer.player_id;
      onSelectPlayer(defaultPlayer.player_id);

      requestAnimationFrame(animationLoop);
    }

    window.onload = init;
  