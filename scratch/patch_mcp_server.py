import re

path = 'mcp_server/football_mcp_server.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update simulate_client_club_renewal_pipeline
old_renew_return = """    return {
        "status": "evaluated",
        "client_id": client_id,
        "client_name": name,
        "client_name_ko": name_ko,
        "club": club,
        "current_weekly_wage_eur": curr_wage,
        "requested_weekly_wage_eur": requested_weekly_wage_eur,
        "wage_increase_pct": wage_increase_pct,
        "annual_cost_delta_eur": annual_cost_delta,
        "club_psr_headroom_eur": psr_headroom_eur,
        "headroom_usage_pct": headroom_usage_pct,
        "decision": decision,
        "decision_label": decision_label,
        "status_message": status_msg,
        "counter_offer": counter_offer,
        "contract_years": contract_years,
        "requested_buyout_eur": requested_buyout_eur,
        "signing_bonus_eur": signing_bonus_eur,
    }"""

new_renew_return = """    counter_terms = None
    if counter_offer:
        counter_terms = {
            "offered_weekly_wage_eur": counter_offer.get("offered_weekly_wage_eur", agreed_wage),
            "performance_bonus_per_week_eur": counter_offer.get("performance_bonus_per_match", 0),
            "signing_loyalty_bonus_eur": round((signing_bonus_eur or 0) * 0.5),
            "proposed_buyout_eur": counter_offer.get("demanded_buyout_eur"),
            "rationale_ko": counter_offer.get("incentive_description", status_msg)
        }

    return {
        "status": "evaluated",
        "client_id": client_id,
        "client_name": name,
        "client_name_ko": name_ko,
        "club": club,
        "current_weekly_wage_eur": curr_wage,
        "requested_weekly_wage_eur": requested_weekly_wage_eur,
        "wage_increase_pct": wage_increase_pct,
        "wage_hike_pct": wage_increase_pct,
        "annual_cost_delta_eur": annual_cost_delta,
        "club_psr_headroom_eur": psr_headroom_eur,
        "headroom_usage_pct": headroom_usage_pct,
        "decision": decision,
        "decision_label": decision_label,
        "status_message": status_msg,
        "director_notes": status_msg,
        "counter_offer": counter_offer,
        "counter_offer_terms": counter_terms,
        "contract_years": contract_years,
        "requested_buyout_eur": requested_buyout_eur,
        "signing_bonus_eur": signing_bonus_eur or 0,
        "requested_terms": {
            "weekly_wage_eur": requested_weekly_wage_eur,
            "contract_years": contract_years,
            "annual_gross_wage_eur": requested_weekly_wage_eur * 52,
            "buyout_clause_eur": requested_buyout_eur,
            "signing_bonus_eur": signing_bonus_eur or 0
        }
    }"""

if old_renew_return in content:
    content = content.replace(old_renew_return, new_renew_return)
    print("Successfully replaced renew_return in mcp_server/football_mcp_server.py")
else:
    print("Could not find old_renew_return!")

# 2. Update simulate_client_club_transfer_pipeline
old_transfer_action = """    if action == "EXECUTE_TRANSFER":
        if not all_cleared:
            return {"error": "이적 게이트웨이 심사를 통과하지 못했습니다."}
        return negotiate_client_club_transfer(
            client_id=client_id,
            client_type=client_type,
            destination_club=destination_club,
            destination_league=destination_league,
            transfer_fee_eur=offered_transfer_fee_eur,
            new_weekly_wage_eur=offered_weekly_wage_eur,
            contract_years=contract_years
        )

    return {
        "status": "simulated",
        "client_id": client_id,
        "client_name": name,
        "client_name_ko": name_ko,
        "from_club": current_club,
        "to_club": destination_club,
        "to_league": destination_league,
        "transfer_fee_eur": offered_transfer_fee_eur,
        "weekly_wage_eur": offered_weekly_wage_eur,
        "contract_years": contract_years,
        "all_stages_cleared": all_cleared,
        "stages": [
            {"stage": 1, "title": "구단 간 이적료 및 셀온 조항 합의", "status": stage1_status, "code": stage1_code, "detail": stage1_detail},
            {"stage": 2, "title": "UK FA GBE 워크퍼밋 및 비자 승인", "status": stage2_status, "code": stage2_code, "detail": stage2_detail},
            {"stage": 3, "title": "공식 정밀 메디컬 & 피지컬 테스트", "status": stage3_status, "code": stage3_code, "detail": stage3_detail},
            {"stage": 4, "title": "FIFA TMS(이적매칭시스템) 증명서 발급", "status": stage4_status, "code": stage4_code, "detail": stage4_detail},
        ],
        "tms_certificate_id": tms_id,
        "solidarity_contribution_eur": solidarity_eur,
        "fifa_agent_commission_eur": agent_commission_eur,
    }"""

new_transfer_action = """    if action in ("EXECUTE_TRANSFER", "FORCE_EXECUTE"):
        exec_res = negotiate_client_club_transfer(
            client_id=client_id,
            client_type=client_type,
            destination_club=destination_club,
            destination_league=destination_league,
            transfer_fee_eur=offered_transfer_fee_eur,
            new_weekly_wage_eur=offered_weekly_wage_eur,
            contract_years=contract_years
        )
        if "error" in exec_res:
            return exec_res
        return {
            "status": "executed",
            "message": f"🏛️ FIFA TMS 공식 발효 완료: {name_ko or name} 선수가 {destination_club} ({destination_league})으로 공식 이적 체결되었습니다!",
            "client_id": client_id,
            "client_name": name,
            "client_name_ko": name_ko,
            "destination_club": destination_club,
            "destination_league": destination_league,
            "agreed_transfer_fee_eur": offered_transfer_fee_eur,
            "new_weekly_wage_eur": offered_weekly_wage_eur,
            "contract_years": contract_years,
            "agent_commission_eur": agent_commission_eur,
            "tms_certificate_id": tms_id,
            "exec_details": exec_res
        }

    return {
        "status": "simulated",
        "client_id": client_id,
        "client_name": name,
        "client_name_ko": name_ko,
        "from_club": current_club,
        "to_club": destination_club,
        "destination_club": destination_club,
        "to_league": destination_league,
        "destination_league": destination_league,
        "transfer_fee_eur": offered_transfer_fee_eur,
        "agreed_transfer_fee_eur": offered_transfer_fee_eur,
        "weekly_wage_eur": offered_weekly_wage_eur,
        "new_weekly_wage_eur": offered_weekly_wage_eur,
        "contract_years": contract_years,
        "all_stages_cleared": all_cleared,
        "stages": [
            {"stage": 1, "title": "구단 간 이적료 및 셀온 조항 합의", "status": stage1_status, "code": stage1_code, "detail": stage1_detail},
            {"stage": 2, "title": "UK FA GBE 워크퍼밋 및 비자 승인", "status": stage2_status, "code": stage2_code, "detail": stage2_detail},
            {"stage": 3, "title": "공식 정밀 메디컬 & 피지컬 테스트", "status": stage3_status, "code": stage3_code, "detail": stage3_detail},
            {"stage": 4, "title": "FIFA TMS(이적매칭시스템) 증명서 발급", "status": stage4_status, "code": stage4_code, "detail": stage4_detail},
        ],
        "stage_1_fee_and_buyout": {
            "agreed_transfer_fee_eur": offered_transfer_fee_eur,
            "sell_on_deduction_eur": solidarity_eur,
            "summary": stage1_detail,
            "status": stage1_status
        },
        "stage_2_gbe_and_visa": {
            "status": stage2_status,
            "regulatory_summary": stage2_code,
            "notes": stage2_detail
        },
        "stage_3_medical_exam": {
            "status": stage3_status,
            "medical_summary": stage3_code,
            "insurance_status": stage3_detail
        },
        "stage_4_fifa_tms_clearing": {
            "tms_certificate_id": tms_id,
            "tms_summary": stage4_code,
            "solidarity_contribution_ko": stage4_detail
        },
        "tms_certificate_id": tms_id,
        "solidarity_contribution_eur": solidarity_eur,
        "fifa_agent_commission_eur": agent_commission_eur,
        "agent_commission_eur": agent_commission_eur,
    }"""

if old_transfer_action in content:
    content = content.replace(old_transfer_action, new_transfer_action)
    print("Successfully replaced transfer_action in mcp_server/football_mcp_server.py")
else:
    print("Could not find old_transfer_action!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated mcp_server/football_mcp_server.py")
