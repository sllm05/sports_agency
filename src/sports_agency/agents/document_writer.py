"""
Document Writer Agent (`src/sports_agency/agents/document_writer.py`)

Responsible for Node 5: Triple-Output Practical Document Writer.
Synthesizes comprehensive, real-world sports agency deliverables in Markdown:
1. Career Valuation & Growth Report (Family presentation)
2. Negotiation Deal Preparation Cheat Sheet (Internal confidential)
3. Club Pitch Deck & Term Sheet (1-Page Executive Dossier)
"""

from __future__ import annotations

import json
from typing import Any

from sports_agency.agents.base import BaseAgent, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import AgencyGraphState, TripleOutputDocsSchema


class DocumentWriterAgent(BaseAgent):
    """
    Triple-Output Practical Document Writer Agent (powered by gemini-3.8-flash).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Triple-Output Document Writer Agent",
            role_description="실무용 3대 마크다운 문서(커리어 보고서, 협상 치트시트, 구단 제출용 피치덱) 전문 작성 및 파일 디스크 익스포터",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        tool_trace = list(state.get("hermes_tool_trace", []))
        logs = list(state.get("model_usage_log", []))

        p = state["player_profile"]
        band = state["peer_wage_band"]["wage_band_eur"]
        peers = state["peer_wage_band"].get("peers", [])
        legal = state["rag_legal_review"]
        metrics = state["negotiation_metrics"]
        psr = state.get("psr_and_tax_breakdown", {})
        clubs = state.get("matched_clubs", [])
        tactical_matches = state.get("tactical_vector_matches", [])
        live_news = state.get("live_club_news", {})
        transcript = state.get("sparring_transcript", [])

        target_club_name = metrics["target_club_name"]
        ask_wage = metrics["opening_ask_wage"]
        club_offer = metrics["club_counter_wage"]
        agreed_base = metrics["agreed_base_wage"]
        agreed_bonus = metrics["agreed_bonus_wage"]
        release_clause = metrics["release_clause_eur"]
        agreed_fee_pct = metrics["agreed_fee_pct"]
        fallback_wage = metrics["fallback_floor_wage"]

        tend = p.get("playstyle_and_tendencies", {})
        ucl = p.get("career_and_ucl", {})
        vp = p.get("valuation_and_profile", {})
        top_club = clubs[0] if clubs else {}

        peer_rows_md = "\n".join(
            f"| {pr['name_ko']} ({pr['name']}) | {pr['current_club']} ({pr['league']}) | {pr['age']}세 | "
            f"€{pr['market_value_eur']:,} | €{pr['weekly_wage_eur']:,} | 상위 {100 - pr['pos_percentile'] + 1}% |"
            for pr in peers
        )

        club_rows_md = "\n".join(
            f"| **{idx+1}순위: {c['club_name']}** ({c['league']}) | 감독 {c.get('manager_name', '-')} ({c.get('manager_preferred_formation', '-')}) | "
            f"{c['current_starter']} ({c['starter_age']}세, 만료 {c['starter_contract_expires']}) | "
            f"€{c['starter_weekly_wage_eur']:,} | €{c['max_weekly_wage_offer_eur']:,} | {c.get('manager_position_requirement', c['recruitment_note'])} |"
            for idx, c in enumerate(clubs[:3])
        )

        tactical_vec_md = "\n".join(
            f"- **{tm['club_name']}** ({tm['league']}): 전술 벡터 유사도 `{tm['tactical_similarity_score']}` *(임베딩: {tm['embedding_model']})*"
            for tm in tactical_matches
        )

        writer_prompt = (
            f"당신은 유럽 축구 에이전시의 수석 문서 작성 에이전트입니다.\n"
            f"아래 실제 SQLite 심층 데이터(Opta/Understat 백분위, UCL 경력, 감독 전술 요구치, 구단 PSR 감가상각 및 세후/세전 연봉), "
            f"커리어 에이전트의 경로 판정(career_strategy), 벡터 RAG 법률 판독 결과, 그리고 모의 협상 타결 수치를 모두 반영하여 "
            f"현업 실무용 마크다운 문서 3종('career_report_md', 'deal_prep_md', 'pitch_deck_md')을 JSON 객체로 작성하세요.\n\n"
            f"[1. 선수 및 Opta/Understat 실측 심층 데이터]\n"
            f"- 이름: {p['name_ko']} ({p['name']}), 소속: {p['current_club']} ({p['league']}), 포지션: {p['position']} ({p['secondary_positions']}), 나이: {p['age']}세\n"
            f"- 시세: €{p['market_value_eur']:,} (커리어 피크 €{vp.get('highest_market_value_eur', p['market_value_eur']):,}), 현재 주급: €{p['weekly_wage_eur']:,} ({'실제 기밀계약 입력' if not p.get('is_wage_estimated', 1) else '추정치'}), 계약만료: {p['contract_expires']}\n"
            f"- 시즌 스탯: {p['minutes_played']}분 출전, 90분당 득점 {p['goals_per90']}, 도움 {p['assists_per90']}, 전진액션 {p['progressive_actions_per90']}회, 키패스 {p['key_passes_per90']}회, 동 포지션 상위 {100 - p['pos_percentile'] + 1}%\n"
            f"- 전술 아키타입: {tend.get('tactical_archetype', '')}\n"
            f"- 실측 강점(Strengths): {tend.get('strengths_tags', p['strengths_summary'])}\n"
            f"- 실측 보완점(Weaknesses) 및 카운터 방어: {tend.get('weaknesses_tags', '')}\n"
            f"- 내구성/가용률(Availability %) 진단: {tend.get('durability_and_availability_note', '')}\n"
            f"- 통산 & UCL 경력: 통산 {ucl.get('career_matches', 0)}경기 {ucl.get('career_goals', 0)}골 | UCL/유럽대항전 {ucl.get('ucl_matches', 0)}경기 ({ucl.get('ucl_goals', 0)}골 {ucl.get('ucl_assists', 0)}도움) | A매치 {vp.get('international_caps', 0)}경기\n\n"
            f"[2. 커리어 에이전트 경로 판독 및 3개년 로드맵]\n"
            f"- 커리어 경로 판정: {state.get('career_strategy', {}).get('path_label', 'IMMEDIATE_TRANSFER')}\n"
            f"- 계약 레버리지 해설: {state.get('career_strategy', {}).get('contract_leverage', '')}\n"
            f"- 커리어 브리핑: {state.get('career_strategy', {}).get('career_agent_briefing', '')}\n\n"
            f"[3. 비교군(Peer 5인) 주급 밴드 및 마크다운 표]\n"
            f"- Q25: €{band['q25_conservative']:,} / 중앙값: €{band['median_fair']:,} / Q75: €{band['q75_ambitious']:,}\n"
            f"- 비교군 표 행:\n{peer_rows_md}\n\n"
            f"[4. 매칭 구단, 감독 전술 적합도 및 실시간 검색 동향]\n"
            f"- 타겟 구단: {target_club_name} (감독: {top_club.get('manager_name', '현 감독')}, 포메이션: {top_club.get('manager_preferred_formation', '-')}, 포지션 요구사항: {top_club.get('manager_position_requirement', '-')})\n"
            f"- 실시간 동향({live_news.get('source', '')}): {live_news.get('headline', '')} — {live_news.get('tactical_context', '')}\n"
            f"- 구단 비교 행:\n{club_rows_md if club_rows_md else '현 소속팀 재계약 트랙'}\n"
            f"- 전술 벡터 유사도:\n{tactical_vec_md}\n\n"
            f"[5. 구단 재무(PSR/FFP 감가상각) 및 국가별 세전/세후(Net-Gross) 시뮬레이션]\n"
            f"- 협상 기준 세제: {psr.get('league', p['league'])} ({psr.get('negotiation_basis', 'GROSS_WEEKLY')}, 소득세율 {psr.get('top_income_tax_rate_pct', 45)}%, 구단 사회보장세 {psr.get('employer_social_rate_pct', 12)}%)\n"
            f"- 합의 기본급 세전/세후: 세전 주급 €{agreed_base:,}/주 (연 €{psr.get('annual_gross_wage_eur', agreed_base*52):,}) ↔ 선수 실수령 세후 주급 약 €{psr.get('weekly_net_wage_eur', int(agreed_base*0.55)):,}/주 (세후 연봉 €{psr.get('annual_net_wage_eur', 0):,})\n"
            f"- 구단 연간 PSR 장부 총비용(Annualized Squad Cost): 이적료 감가상각(연 €{psr.get('annual_transfer_amortization_eur', 0):,}) + 세전 연봉 + 사회보장세 + 수수료 상각 = **연 €{psr.get('annual_psr_book_cost_eur', 0):,}/년** (총 계약 패키지 €{psr.get('total_deal_package_cost_eur', 0):,})\n"
            f"- 세제/재정 해설: {psr.get('tax_regime_note', '')}\n\n"
            f"[6. SQLite Vector RAG 법률·워크퍼밋 판독 및 출처]\n"
            f"- 영국 GBE: {legal['gbe_work_permit_result']} {legal['gbe_source']}\n"
            f"- Non-EU 쿼터: {legal['non_eu_quota_result']} {legal['non_eu_source']}\n"
            f"- FIFA 수수료: {legal['ffar_fee_guidance']} {legal['ffar_source']}\n"
            f"- 재정 규정: {legal['psr_source']}\n\n"
            f"[7. 모의 협상 타결 조건 ({metrics['human_strategy_label']})]\n"
            f"- 1차 요구액(Anchor): €{ask_wage:,}/주 | 구단 1차 역제안: €{club_offer:,}/주 | 마지노선(Fallback): €{fallback_wage:,}/주\n"
            f"- 최종 합의 기본급: €{agreed_base:,}/주 + 성과 보너스: €{agreed_bonus:,}/주 상당 | 바이아웃: €{release_clause:,} | 에이전트 수수료: {agreed_fee_pct}%\n"
            f"- 협상 대화 요약: {json.dumps(transcript, ensure_ascii=False)}\n\n"
            f"작성 지침:\n"
            f"- 'career_report_md': 선수 및 가족 프레젠테이션용 커리어 성장 및 가치 평가 보고서 (1. 선수 현주소 정밀 진단, 2. 커리어 타이밍 판정 및 계약 만료 주기 레버리지, 3. 3개년 로드맵[Year 1 연착륙, Year 2 대륙대항전, Year 3 엘리트 메가클럽 점프], 4. 추천 리그 및 출전시간 60% 보장 조건)\n"
            f"- 'deal_prep_md': 에이전트 내부 대외비용 협상 치트시트 (1. 타겟 금액 밴드 Anchor/Target/Fallback 및 세전·세후 실수령액 비교, 2. Peer 비교군 마크다운 표, 3. 구단 디렉터 예상 압박 질문 3가지[선수 약점 백분위/가용률, 구단 PSR 감가상각 부담, FFAR 3% 수수료 상한] 및 법률/데이터 카운터 논리)\n"
            f"- 'pitch_deck_md': {target_club_name} 스포츠 디렉터 및 감독 제출용 1-Page Executive Dossier (1. 감독 맞춤형 전술 적합도[포메이션·포지션 요구치 및 Opta 상위 백분위], 2. 단장/CFO 맞춤형 재무·PSR 감가상각 시뮬레이션 표 및 주전 세대교체 가성비 비교표, 3. GBE 워크퍼밋 및 Non-EU 즉시 등록 법률 증명[출처·기준일 명시], 4. 최종 제안 Term Sheet 요약)\n"
            f'반드시 JSON 키 "career_report_md", "deal_prep_md", "pitch_deck_md"만 포함하여 마크다운 원문 문자열로 응답하세요.'
        )

        parsed_docs, model_used = ROUTER.generate_structured(
            writer_prompt,
            TripleOutputDocsSchema,
            system_instruction="실제 데이터와 법률 출처를 정확히 인용하여 현업 에이전시 품질의 마크다운 문서 3종을 작성하세요.",
            use_light_model=False,
            temperature=0.25,
        )
        career_report_md = parsed_docs.career_report_md
        deal_prep_md = parsed_docs.deal_prep_md
        pitch_deck_md = parsed_docs.pitch_deck_md

        logs.append({"node": "Node 5: Triple-Output Document Writer", "model": model_used})

        saved = invoke_hermes_mcp_tool(
            tool_trace,
            "export_triple_agency_documents",
            {
                "player_name": p["name"],
                "career_report_md": career_report_md,
                "deal_prep_md": deal_prep_md,
                "pitch_deck_md": pitch_deck_md,
            },
        )

        log_work_event("LANGGRAPH_NODE_5", f"Generated & saved Triple-Output Markdown documents for {p['name']}")
        return {
            "hermes_tool_trace": tool_trace,
            "career_report_md": career_report_md,
            "deal_prep_md": deal_prep_md,
            "pitch_deck_md": pitch_deck_md,
            "saved_files": saved,
            "model_usage_log": logs,
        }
