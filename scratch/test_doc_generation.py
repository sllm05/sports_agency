import json, sys, os
sys.path.insert(0, os.path.abspath("."))
from sports_agency.agents.document_writer import DocumentWriterAgent
from sports_agency.schemas.agent_schemas import AgencyGraphState

# Create mock/real state for Haaland
sample_state: AgencyGraphState = {
    "player_name": "Erling Haaland",
    "track_mode": "TRACK_A_TRANSFER",
    "target_wage_increase_pct": 20.0,
    "priority_goal": "SALARY_MAXIMIZATION",
    "player_profile": {
        "player_id": "haaland_e_01",
        "name": "Erling Haaland",
        "name_ko": "엘링 홀란",
        "current_club": "Manchester City FC",
        "league": "Premier League",
        "position": "ST",
        "secondary_positions": "CF,LW",
        "age": 25,
        "market_value_eur": 200000000,
        "weekly_wage_eur": 450000,
        "contract_expires": "2034-06",
        "minutes_played": 3131,
        "goals_per90": 0.72,
        "assists_per90": 0.18,
        "progressive_actions_per90": 5.63,
        "key_passes_per90": 0.95,
        "xg_per90": 0.74,
        "xa_per90": 0.16,
        "defensive_duels_won_pct": 58.5,
        "pos_percentile": 99,
        "strengths_summary": "90분당 전진액션 5.63회, 키패스 0.95회, xG+xAG/90 0.90",
        "playstyle_and_tendencies": {
            "tactical_archetype": "엘리트 타깃 피니셔 & 박스 침투형 스트라이커",
            "strengths_tags": "박스 안 원터치 피니시, 가공할 공중볼 장악력, 스프린트 라인 침투",
            "weaknesses_tags": "낮은 블록 밀집 수비 시 연계 빈도",
            "durability_and_availability_note": "시즌 3,131분 주전 소화, 가용률 94%",
        },
        "career_and_ucl": {
            "career_matches": 310,
            "career_goals": 260,
            "ucl_matches": 42,
            "ucl_goals": 44,
            "ucl_assists": 6,
        },
        "valuation_and_profile": {
            "highest_market_value_eur": 200000000,
            "international_caps": 39,
        }
    },
    "peer_wage_band": {
        "wage_band_eur": {
            "q25_conservative": 380000,
            "median_fair": 450000,
            "q75_ambitious": 550000,
        },
        "peers": [
            {"name": "Kylian Mbappé", "name_ko": "킬리안 음바페", "current_club": "Real Madrid", "league": "La Liga", "age": 26, "market_value_eur": 180000000, "weekly_wage_eur": 600000, "pos_percentile": 99},
            {"name": "Harry Kane", "name_ko": "해리 케인", "current_club": "Bayern Munich", "league": "Bundesliga", "age": 31, "market_value_eur": 90000000, "weekly_wage_eur": 480000, "pos_percentile": 97},
        ]
    },
    "matched_clubs": [
        {
            "club_name": "Real Madrid",
            "league": "La Liga",
            "manager_name": "카를로 안첼로티",
            "manager_preferred_formation": "4-3-3",
            "current_starter": "호드리구",
            "starter_age": 24,
            "starter_contract_expires": "2028-06",
            "starter_weekly_wage_eur": 240000,
            "max_weekly_wage_offer_eur": 650000,
            "manager_position_requirement": "압도적인 골 결정력의 월드클래스 No.9"
        }
    ],
    "tactical_vector_matches": [
        {"club_name": "Real Madrid", "league": "La Liga", "tactical_similarity_score": 0.94, "embedding_model": "text-embedding-004"}
    ],
    "live_club_news": {
        "source": "Opta & Fabrizio Romano",
        "headline": "레알 마드리드, No.9 득점력 강화를 위한 갈락티코 플랜 수립",
        "tactical_context": "챔피언스리그 득점 전환율 제고"
    },
    "career_strategy": {
        "path_label": "ELITE_EXTENDED_PEAK",
        "contract_leverage": "2034년 장기 계약 기반 메가 릴리즈 조항 및 최상위 주급 밴드 사수",
        "career_agent_briefing": "세계 최고의 골게터로서 골든부트 및 발롱도르 컨텐더 지위 확립",
        "three_year_roadmap": [
            {"year": "Year 1 (2025-26)", "phase": "UCL 및 리그 트레블 수성 및 득점왕"},
            {"year": "Year 2 (2026-27)", "phase": "글로벌 브랜드 가치 극대화 및 발롱도르 수상"},
            {"year": "Year 3 (2027-28)", "phase": "역대 최고 주급 갱신 및 레코드 바이아웃 조항 재조정"}
        ]
    },
    "rag_legal_review": {
        "gbe_work_permit_result": "노르웨이 A대표팀 출전율 95%로 영국 FA GBE 15점 자동 통과 (Auto-Pass)",
        "gbe_source": "The FA Men's Players Point-Based System Guidelines (2024-2026)",
        "non_eu_quota_result": "라리가 Non-EU 3인 쿼터 및 EPL 비홈그로운 스쿼드 등록 요건 완전 충족",
        "non_eu_source": "UEFA & RFEF Player Registration Guidelines",
        "ffar_fee_guidance": "Circular 1873 및 마인츠 법원 효력정지에 따라 에이전트 수수료 6.5% 적법",
        "ffar_source": "FIFA Circular No. 1873 (2023.12.30)",
        "psr_source": "Premier League Profitability and Sustainability Rules (PSR 5년 상각 상한)"
    },
    "negotiation_metrics": {
        "target_club_name": "Real Madrid",
        "opening_ask_wage": 600000,
        "club_counter_wage": 500000,
        "agreed_base_wage": 550000,
        "agreed_bonus_wage": 80000,
        "release_clause_eur": 250000000,
        "agreed_fee_pct": 6.5,
        "fallback_floor_wage": 480000,
        "human_strategy_label": "공격적 앵커링 전략",
    },
    "psr_and_tax_breakdown": {
        "league": "Premier League",
        "country": "England",
        "negotiation_basis": "GROSS_WEEKLY",
        "contract_years": 5,
        "amortization_years_applied": 5,
        "weekly_gross_wage_eur": 550000,
        "weekly_net_wage_eur": 302500,
        "annual_gross_wage_eur": 28600000,
        "annual_net_wage_eur": 15730000,
        "employer_social_tax_annual_eur": 3946800,
        "top_income_tax_rate_pct": 45.0,
        "employer_social_rate_pct": 13.8,
        "transfer_fee_eur": 180000000,
        "annual_transfer_amortization_eur": 36000000,
        "agent_fee_pct": 6.5,
        "agent_commission_total_eur": 15145000,
        "signing_bonus_eur": 10000000,
        "annual_psr_book_cost_eur": 73575800,
        "total_deal_package_cost_eur": 367879000,
        "mandatory_release_clause": False,
        "tax_regime_note": "영국 세제 기준: 45% 최고세율 적용 및 최대 5년 균등 상각"
    },
    "sparring_transcript": [
        {"round": 1, "speaker": "에이전트", "content": "홀란의 Opta 90분당 득점력과 글로벌 상업성을 감안하여 주급 €600,000을 요구합니다."},
        {"round": 1, "speaker": "구단 디렉터", "content": "주급 체계 안정성을 고려하여 기본급 €500,000에 득점 보너스를 제안합니다."},
        {"round": 2, "speaker": "에이전트", "content": "기본급 €550,000에 우승 및 득점왕 보너스 패키지로 타결을 제안합니다."},
        {"round": 2, "speaker": "구단 디렉터", "content": "동의합니다. 5년 계약에 바이아웃 €250,000,000으로 최종 승인합니다."}
    ],
    "hermes_tool_trace": [],
    "model_usage_log": []
}

agent = DocumentWriterAgent()
result = agent.run(sample_state)

print("Document generation successful!")
print("Saved files:", result.get("saved_files"))
print("Pitch deck contains SVG Radar:", "<svg" in result.get("pitch_deck_md", ""))
print("Pitch deck contains DataMB bars:", "DataMB 실측 벤치마크" in result.get("pitch_deck_md", ""))
print("Pitch deck contains PSR gauge:", "연간 장부 비용" in result.get("pitch_deck_md", ""))
print("Pitch deck contains Term sheet:", "최종 합의 Term Sheet" in result.get("pitch_deck_md", ""))
