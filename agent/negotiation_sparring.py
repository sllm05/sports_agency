"""
Negotiation Sparring Simulator Agent (`src/sports_agency/agents/negotiation_sparring.py`)

Responsible for Node 4A (Round 1 Opening Sparring) and Node 4B (Round 2 HITL Counter Sparring).
Simulates realistic adversary negotiations between Player Agent AI and Opposing Club Sporting Director AI,
factoring in Opta percentiles, PSR squad cost, release clauses, and Human-in-the-Loop strategic interventions.
"""

from __future__ import annotations

import json
from typing import Any

from sports_agency.agents.base import BaseAgent, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import (
    AgencyGraphState,
    SparringRound1Schema,
    SparringRound2Schema,
)


class NegotiationSparringAgent(BaseAgent):
    """
    Negotiation Sparring Simulator Agent (powered by gemini-3.8-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Negotiation Sparring Simulator",
            role_description="에이전트 AI vs 상대 구단 디렉터 AI 간 다자간 대립 모의 협상 및 HITL 전략 시뮬레이터",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        """Default run delegates to round 1."""
        return self.run_round_1(state)

    def run_round_1(self, state: AgencyGraphState) -> dict[str, Any]:
        logs = list(state.get("model_usage_log", []))
        p = state["player_profile"]
        band = state["peer_wage_band"]["wage_band_eur"]
        clubs = state.get("matched_clubs", [])
        track_mode = state["track_mode"]
        legal = state["rag_legal_review"]
        psr = state.get("psr_and_tax_breakdown", {})

        cur_wage = p["weekly_wage_eur"]
        desired_wage = int(cur_wage * (1 + state["target_wage_increase_pct"] / 100.0))
        ref_opening_ask = max(desired_wage, band["median_fair"])
        ref_club_counter = int((cur_wage + ref_opening_ask) / 2)

        top_club = clubs[0] if (track_mode == "TRACK_A_TRANSFER" and clubs) else {}
        target_club_name = top_club.get("club_name", p["current_club"])
        starter_context = (
            f"현 주전 {top_club['current_starter']}({top_club['starter_age']}세, 만료 {top_club['starter_contract_expires']}, 주급 €{top_club['starter_weekly_wage_eur']:,})"
            if top_club
            else f"현 소속 구단({p['current_club']}) 핵심 전력 유지 및 동급 대체자 이적료(€{p['market_value_eur']:,}+) 절감"
        )

        tend = p.get("playstyle_and_tendencies", {})
        ucl = p.get("career_and_ucl", {})
        vp = p.get("valuation_and_profile", {})
        mgr_context = (
            f"타겟 구단 감독: {top_club.get('manager_name', '')} (포메이션 {top_club.get('manager_preferred_formation', '')}, "
            f"포지션 전술 요구사항: {top_club.get('manager_position_requirement', '')})"
            if top_club.get("manager_name")
            else f"현 소속팀 감독 전술 시스템 핵심 적합 자원"
        )
        club_fin = top_club.get("club_live_standing") or p.get("club_standing_and_finance") or {}
        club_fin_str = (
            f"리그 {club_fin.get('rank_position', '-')}위 ({club_fin.get('points', 0)}점), 구장 {club_fin.get('stadium_seats', 45000):,}석, 최근 순이적지출 {club_fin.get('net_transfer_record', '€0')}"
            if club_fin else ""
        )

        prompt = (
            f"유럽 축구 이적/재계약 협상 테이블의 1라운드 공방을 JSON 객체로 작성하세요.\n"
            f"[1. 선수 및 Opta/Understat 실측 심층 데이터]\n"
            f"- 선수: {p['name_ko']} ({p['name']}), 나이 {p['age']}세, 계약만료 {p['contract_expires']}, 시세 €{p['market_value_eur']:,} (커리어 피크 €{vp.get('highest_market_value_eur', p['market_value_eur']):,})\n"
            f"- 전술 아키타입: {tend.get('tactical_archetype', '')}\n"
            f"- 에이전트 공격 무기 (실측 강점 백분위 & UCL 경력): {tend.get('strengths_tags', p['strengths_summary'])} | 통산 {ucl.get('career_matches', 0)}경기 (UCL/유럽대항전 {ucl.get('ucl_matches', 0)}경기 {ucl.get('ucl_goals', 0)}골 {ucl.get('ucl_assists', 0)}도움)\n"
            f"- 구단 디렉터 압박 무기 (실측 약점 백분위 & 내구성/가용률): {tend.get('weaknesses_tags', '')} | {tend.get('durability_and_availability_note', '')}\n\n"
            f"[2. 구단 전술·재정 및 PSR/세제 데이터]\n"
            f"- 상대 구단: {target_club_name} ({starter_context}) | {club_fin_str}\n"
            f"- 감독 전술 적합도: {mgr_context}\n"
            f"- 비교군 주급 밴드: Q25 €{band['q25_conservative']:,} ~ 중앙값 €{band['median_fair']:,} ~ Q75 €{band['q75_ambitious']:,} (현재 주급 €{cur_wage:,}/주)\n"
            f"- 구단 PSR 장부 총비용 시뮬레이션({psr.get('league', p['league'])}, {psr.get('negotiation_basis', 'GROSS_WEEKLY')}): "
            f"요구 주급 기준 연간 구단 PSR 장부 총비용(이적료 감가상각 €{psr.get('annual_transfer_amortization_eur', 0):,}/년 + 세전 연봉 €{psr.get('annual_gross_wage_eur', 0):,}/년 + 사회보장세/수수료) = 연 €{psr.get('annual_psr_book_cost_eur', 0):,}/년 (세후 주급 약 €{psr.get('weekly_net_wage_eur', 0):,}/주)\n"
            f"- 워크퍼밋/규정 검증: {legal['gbe_work_permit_result']} | {legal['non_eu_quota_result']}\n\n"
            f"[3. 협상 수치 및 대사 생성 지침]\n"
            f"- 에이전트 희망 1차 요구 주급(opening_ask_wage_eur, 기준선 약 €{ref_opening_ask:,}/주 내외)과 구단 디렉터의 1차 역제안 주급(club_counter_wage_eur, 기준선 약 €{ref_club_counter:,}/주 내외)을 선수 백분위와 구단 재정 상황에 맞춰 정수로 산출하고 대사에 정확히 일치시켜 인용하세요.\n"
            f"- 'agent_r1': Opta 상위 백분위 강점, 감독 포메이션 요구사항 부합도, 비교군 주급 중앙값/Q75, 그리고 구단 주전 대체/이적료 절감 효과를 근거로 opening_ask_wage_eur 및 에이전트 수수료 {p.get('agent_fee_target_pct', 7.0)}%를 당당히 요구하세요.\n"
            f"- 'director_r1': 선수의 Opta 하위 백분위 보완점 또는 시즌 가용률(출전 분수), 구단 연간 PSR 장부 총비용(연 €{psr.get('annual_psr_book_cost_eur', 0):,}) 부담, FIFA FFAR 제15조 원안(3% 상한)을 근거로 club_counter_wage_eur를 역제안하며 날카롭게 압박하세요."
        )

        parsed, model_used = ROUTER.generate_structured(
            prompt,
            SparringRound1Schema,
            system_instruction="실제 유럽 축구 협상 테이블의 에이전트와 구단 스포츠 디렉터 화법으로 Opta 백분위, 감독 전술, PSR 감가상각 수치를 정확히 인용해 작성하세요.",
            use_light_model=False,
            temperature=0.35,
        )
        logs.append({"node": "Node 4A: Sparring Simulator (Round 1)", "model": model_used})

        opening_ask_wage = int(parsed.opening_ask_wage_eur or ref_opening_ask)
        club_counter_wage = int(parsed.club_counter_wage_eur or ref_club_counter)

        transcript = [
            {"round": "Round 1", "speaker": "선수 에이전트 AI", "message": parsed.agent_r1},
            {
                "round": "Round 1",
                "speaker": f"{target_club_name} 디렉터 AI",
                "message": parsed.director_r1,
            },
        ]

        negotiation_metrics = {
            "target_club_name": target_club_name,
            "cur_wage": cur_wage,
            "opening_ask_wage": opening_ask_wage,
            "club_counter_wage": club_counter_wage,
            "fallback_floor_wage": band["q25_conservative"],
        }

        log_work_event(
            "LANGGRAPH_NODE_4A",
            f"Sparring Round 1 completed vs {target_club_name} (ask=€{opening_ask_wage:,}, counter=€{club_counter_wage:,})",
        )
        return {
            "negotiation_metrics": negotiation_metrics,
            "sparring_transcript": transcript,
            "model_usage_log": logs,
        }

    def run_round_2(self, state: AgencyGraphState) -> dict[str, Any]:
        logs = list(state.get("model_usage_log", []))
        tool_trace = list(state.get("hermes_tool_trace", []))
        p = state["player_profile"]
        legal = state["rag_legal_review"]
        psr = state.get("psr_and_tax_breakdown", {})
        metrics = dict(state["negotiation_metrics"])
        transcript = list(state.get("sparring_transcript", []))
        choice = state.get("human_action_choice", "OPTION_2_BONUS_AND_RELEASE_CLAUSE")

        target_club_name = metrics["target_club_name"]
        opening_ask_wage = metrics["opening_ask_wage"]
        club_counter_wage = metrics["club_counter_wage"]
        tend = p.get("playstyle_and_tendencies", {})

        if choice == "OPTION_1_HOLD_BASE_WAGE":
            ref_base = opening_ask_wage
            ref_bonus = int(opening_ask_wage * 0.05)
            ref_rc = int(p["market_value_eur"] * 1.8)
            strategy_label = "전략 1: 기본급 원안 강행 + Opta 상위 백분위 스탯 및 대체자 비용 비교 압박"
        elif choice == "OPTION_3_LOWER_RELEASE_FOR_CLUB_OFFER":
            ref_base = club_counter_wage
            ref_bonus = int(opening_ask_wage * 0.12)
            ref_rc = int(p["market_value_eur"] * 1.25)
            strategy_label = "전략 3: 구단 기본급 수용 + 바이아웃(Release Clause) 대폭 하향 및 셀온/인센티브 실리 확보"
        else:
            ref_base = int((opening_ask_wage + club_counter_wage) / 2)
            ref_bonus = int(opening_ask_wage * 0.15)
            ref_rc = int(p["market_value_eur"] * 1.45)
            strategy_label = "전략 2: 기본급 절충 + 가용률 연동 출전/공격포인트 보너스 신설(PSR 고정비 완화) + FFAR 유예 조항 수수료 방어"

        prompt = (
            f"수석 에이전트(사람)가 선택한 개입 전략('{strategy_label}')을 반영하여 2라운드 최종 타결 수치와 대화를 JSON 객체로 작성하세요.\n"
            f"- 1라운드 요약: 에이전트 요구 €{opening_ask_wage:,}/주 vs 구단 역제안 €{club_counter_wage:,}/주\n"
            f"- 선수 내구성/가용률 방어 논리: {tend.get('durability_and_availability_note', '')}\n"
            f"- 구단 세제 및 PSR 규칙: {psr.get('tax_regime_note', '')}\n"
            f"- 가이드라인 타결 수치(전략 반영): 기본 주급(agreed_base_wage_eur) 약 €{ref_base:,}/주 내외, "
            f"주간 환산 출전/성과 보너스(agreed_bonus_wage_eur) 약 +€{ref_bonus:,}/주 상당(공식전 20경기 출전 달성 시 발동하여 구단 PSR 고정비 리스크 헷지), "
            f"바이아웃(release_clause_eur) 약 €{ref_rc:,} 내외, 에이전트 수수료(agreed_fee_pct) 약 6.0~7.0%\n"
            f"- 에이전트 수수료 방어 근거: {legal['ffar_source']} ({legal['ffar_fee_guidance']})\n"
            f"- 재정 규정 근거: {legal['psr_source']}\n"
            f"작성 지침:\n"
            f"- 'agent_r2': 수석 에이전트의 전략('{strategy_label}'), FIFA Circular No. 1873 수수료 상한 유예 근거, 그리고 PSR 고정비 부담을 낮추는 조건부 보너스/바이아웃 구조를 제시하세요.\n"
            f"- 'director_r2': 에이전트의 PSR 회계 배려 및 전술 적합성에 동의하며 최종 합의된 수치(agreed_base_wage_eur, agreed_bonus_wage_eur, release_clause_eur, agreed_fee_pct)로 Term Sheet 서명을 수락하세요."
        )

        parsed, model_used = ROUTER.generate_structured(
            prompt,
            SparringRound2Schema,
            system_instruction="수석 에이전트의 전략 지시를 완벽히 반영하여 최종 합의(Term Sheet)에 도달하는 협상 수치와 대화를 작성하세요.",
            use_light_model=False,
            temperature=0.3,
        )
        logs.append({"node": "Node 4B: Sparring Simulator (Round 2 HITL)", "model": model_used})

        agreed_base = int(parsed.agreed_base_wage_eur or ref_base)
        agreed_bonus = int(parsed.agreed_bonus_wage_eur or ref_bonus)
        release_clause = int(parsed.release_clause_eur or ref_rc)
        agreed_fee_pct = float(parsed.agreed_fee_pct or 6.0)

        # Recalculate final agreed PSR & Net-Gross breakdown
        final_psr = invoke_hermes_mcp_tool(
            tool_trace,
            "calculate_psr_and_tax_breakdown",
            {
                "league": psr.get("league", p["league"]),
                "transfer_fee_eur": p["market_value_eur"] if state.get("track_mode") == "TRACK_A_TRANSFER" else 0,
                "weekly_wage_eur": agreed_base,
                "contract_years": int(p.get("target_contract_years", 4)),
                "agent_fee_pct": agreed_fee_pct,
                "signing_bonus_eur": int(p.get("target_signing_bonus_eur", 0)),
            },
        )

        transcript.extend(
            [
                {
                    "round": "Round 2 (Human-in-the-Loop 반영)",
                    "speaker": "선수 에이전트 AI (사람 전략 반영)",
                    "message": parsed.agent_r2,
                },
                {
                    "round": "Round 2 (최종 타결)",
                    "speaker": f"{target_club_name} 디렉터 AI",
                    "message": parsed.director_r2,
                },
            ]
        )

        metrics.update(
            {
                "human_strategy_label": strategy_label,
                "agreed_base_wage": agreed_base,
                "agreed_bonus_wage": agreed_bonus,
                "release_clause_eur": release_clause,
                "agreed_fee_pct": agreed_fee_pct,
                "agreed_weekly_net_wage_eur": final_psr["weekly_net_wage_eur"],
                "agreed_annual_net_wage_eur": final_psr["annual_net_wage_eur"],
                "agreed_annual_psr_book_cost_eur": final_psr["annual_psr_book_cost_eur"],
                "agreed_total_deal_package_eur": final_psr["total_deal_package_cost_eur"],
            }
        )

        log_work_event(
            "LANGGRAPH_NODE_4B",
            f"Sparring Round 2 resolved with strategy={choice} -> agreed_base=€{agreed_base:,}, bonus=€{agreed_bonus:,}, annual_psr=€{final_psr['annual_psr_book_cost_eur']:,}",
        )
        return {
            "hermes_tool_trace": tool_trace,
            "psr_and_tax_breakdown": final_psr,
            "negotiation_metrics": metrics,
            "sparring_transcript": transcript,
            "model_usage_log": logs,
        }
