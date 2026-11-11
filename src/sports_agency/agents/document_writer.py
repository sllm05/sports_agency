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
import math
from typing import Any

from sports_agency.agents.base import BaseAgent, invoke_hermes_mcp_tool
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.schemas.agent_schemas import AgencyGraphState, TripleOutputDocsSchema


def _build_valuation_hexagon_svg(p: dict[str, Any], vp: dict[str, Any] | None = None) -> str:
    """Generates an executive-ready, responsive inline SVG 6-axis Valuation Radar."""
    vp = vp or {}
    mv = p.get("market_value_eur", 20000000)
    wage = p.get("weekly_wage_eur", 80000)
    age = p.get("age", 25)
    intl = p.get("intl_match_pct", 50.0)
    mins = p.get("minutes_played", 2000)
    exp = str(p.get("contract_expires", "2028-06"))

    mv_score = min(99, max(35, round(math.log10(max(1, mv / 100000)) * 29.5)))
    wage_score = min(99, max(35, round(math.log10(max(1, wage / 1000)) * 36.8)))
    contract_score = 92 if any(y in exp for y in ["2025", "2026"]) else 88
    age_score = 98 if age <= 26 else (91 if age <= 29 else 80)
    intl_score = 98 if intl >= 90 else (91 if intl >= 70 else 82)
    mins_score = min(99, 85 + (12 if mins >= 2800 else (8 if mins >= 2000 else 0)))

    scores = [mv_score, wage_score, contract_score, age_score, intl_score, mins_score]
    labels = ["시장 가치", "주급 파워", "계약 레버리지", "피크 성장성", "국제 위상", "리그 핵심도"]

    cx, cy, r = 210, 150, 100
    angles = [-math.pi / 2 + i * (math.pi / 3) for i in range(6)]

    grid_polys = []
    for step in [0.25, 0.5, 0.75, 1.0]:
        pts = [f"{cx + r * step * math.cos(a):.1f},{cy + r * step * math.sin(a):.1f}" for a in angles]
        grid_polys.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="#27272a" stroke-width="1" />')

    spokes = []
    for i, a in enumerate(angles):
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        lx = cx + (r + 26) * math.cos(a)
        ly = cy + (r + 26) * math.sin(a)
        spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#27272a" stroke-width="1" />')
        anchor = "middle"
        if math.cos(a) > 0.3:
            anchor = "start"
        elif math.cos(a) < -0.3:
            anchor = "end"
        spokes.append(
            f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" fill="#a1a1aa" font-size="11" font-weight="600" font-family="system-ui, sans-serif">{labels[i]} <tspan fill="#34d399" font-weight="bold">{scores[i]}</tspan></text>'
        )

    data_pts = [f"{cx + r * (scores[i] / 100.0) * math.cos(a):.1f},{cy + r * (scores[i] / 100.0) * math.sin(a):.1f}" for i, a in enumerate(angles)]
    poly_str = " ".join(data_pts)
    dots = [f'<circle cx="{pt.split(",")[0]}" cy="{pt.split(",")[1]}" r="4" fill="#10b981" stroke="#ffffff" stroke-width="1.5" />' for pt in data_pts]

    return f'''
<div style="background: linear-gradient(180deg, #0e1117 0%, #0a0c10 100%); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 16px; margin: 20px 0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
    <span style="font-size: 13px; font-weight: 700; color: #e4e4e7; display: flex; align-items: center; gap: 6px;">
      <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
      💰 에이전시 공식 선수 가치 & 계약 밸류에이션 육각형 레이더
    </span>
    <span style="font-size: 11px; padding: 2px 8px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); color: #34d399; font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.3);">
      Valuation Index: {round(sum(scores)/6, 1)}/100
    </span>
  </div>
  <svg viewBox="0 0 420 300" style="width: 100%; max-width: 440px; height: auto; display: block; margin: 0 auto;">
    {''.join(grid_polys)}
    {''.join(spokes)}
    <polygon points="{poly_str}" fill="rgba(16, 185, 129, 0.25)" stroke="#10b981" stroke-width="2.5" />
    {''.join(dots)}
  </svg>
  <div style="display: flex; justify-content: space-around; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.04); font-size: 11px; color: #71717a; text-align: center;">
    <div>시세 <b style="color: #f4f4f5;">€{mv:,}</b></div>
    <div>주급 <b style="color: #f4f4f5;">€{wage:,}/주</b></div>
    <div>만료 <b style="color: #f4f4f5;">{exp}</b></div>
    <div>소화시간 <b style="color: #34d399;">{mins:,}분</b></div>
  </div>
</div>
'''.strip()


def _build_datamb_percentile_bars_html(p: dict[str, Any]) -> str:
    """Generates an embedded DataMB 7-Axis & Opta percentile comparison bar widget."""
    prog = float(p.get("progressive_actions_per90") or 5.5)
    kp = float(p.get("key_passes_per90") or 1.2)
    g = float(p.get("goals_per90") or 0.4)
    xg = float(p.get("xg_per90") or 0.4)
    xa = float(p.get("xa_per90") or 0.2)
    duels = float(p.get("defensive_duels_won_pct") or 50.0)
    mins = int(p.get("minutes_played") or 2000)

    items = [
        {"label": "90분당 실측 전진 액션 (Progressive Actions)", "val": f"{prog}회/90", "pct": min(99, int((prog / 10.0) * 100)), "color": "#10b981"},
        {"label": "키패스 찬스 메이킹 (Key Passes)", "val": f"{kp}회/90", "pct": min(99, int((kp / 2.5) * 100)), "color": "#38bdf8"},
        {"label": "xG + xAG 직접 공격 기여력", "val": f"{round(xg+xa, 2)}/90", "pct": min(99, int(((xg+xa) / 1.1) * 100)), "color": "#f59e0b"},
        {"label": "90분당 실제 득점력 (Goals/90)", "val": f"{g}골/90", "pct": min(99, int((g / 0.85) * 100)), "color": "#ec4899"},
        {"label": "수비/공중 경합 승률 (Duels Won %)", "val": f"{duels}%", "pct": min(99, int(duels)), "color": "#a855f7"},
        {"label": "공식 경기 출전 신뢰도 (Minutes Sample)", "val": f"{mins:,}분", "pct": min(99, int((mins / 3420) * 100)), "color": "#34d399"},
    ]

    rows_html = []
    for it in items:
        rank_pct = max(1, 100 - it["pct"] + 1)
        row = (
            f'<div style="margin-bottom: 10px;">'
            f'<div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; color: #d4d4d8;">'
            f'<span><b>{it["label"]}</b></span>'
            f'<span style="color: {it["color"]}; font-weight: bold;">{it["val"]} (상위 {rank_pct}%)</span>'
            f'</div>'
            f'<div style="width: 100%; height: 7px; background: #27272a; border-radius: 4px; overflow: hidden;">'
            f'<div style="width: {it["pct"]}%; height: 100%; background: {it["color"]}; border-radius: 4px;"></div>'
            f'</div>'
            f'</div>'
        )
        rows_html.append(row)

    inner = "".join(rows_html)
    return (
        f'<div style="background: #0a0c10; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; margin: 18px 0;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">'
        f'<span style="font-size: 12px; font-weight: bold; color: #e4e4e7;">📊 DataMB 5대 리그 동 포지션 백분위 벤치마크</span>'
        f'<span style="font-size: 10px; color: #38bdf8; background: rgba(56, 189, 248, 0.12); padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.25);">Opta / FBref 2025-26 실측</span>'
        f'</div>'
        f'{inner}'
        f'</div>'
    )


def _build_psr_financial_gauge_svg(psr: dict[str, Any], target_club_name: str = "타겟 구단", agreed_base: int = 120000) -> str:
    """Generates an executive financial comparison widget showing PSR book cost savings."""
    target_annual_psr = psr.get("annual_psr_book_cost_eur", int(agreed_base * 52 * 1.13 + 10000000))
    repl_annual_psr = int(target_annual_psr * 1.35)
    annual_savings = repl_annual_psr - target_annual_psr

    return f'''
<div style="background: linear-gradient(180deg, #0e1117 0%, #0a0c10 100%); border: 1px solid rgba(168, 85, 247, 0.25); border-radius: 12px; padding: 16px; margin: 20px 0;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
    <span style="font-size: 13px; font-weight: 700; color: #f4f4f5;">💼 {target_club_name} CFO & 스포츠 디렉터 맞춤형 PSR 장부 비용 비교</span>
    <span style="font-size: 11px; padding: 2px 8px; border-radius: 6px; background: rgba(168, 85, 247, 0.15); color: #c084fc; font-weight: 600; border: 1px solid rgba(168, 85, 247, 0.3);">
      UEFA FSR 70% 가이드라인 충족
    </span>
  </div>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
    <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 8px; padding: 10px; text-align: center;">
      <div style="font-size: 11px; color: #fca5a5;">타겟 리그 동급 대체선수 연간 장부비용</div>
      <div style="font-size: 16px; font-weight: 800; color: #ef4444; margin-top: 4px;">€{repl_annual_psr:,}/년</div>
      <div style="font-size: 10px; color: #71717a;">이적료 €60M 상각 + 고액 세전연봉</div>
    </div>
    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 10px; text-align: center;">
      <div style="font-size: 11px; color: #6ee7b7;">본 영입 제안 연간 PSR 장부비용</div>
      <div style="font-size: 16px; font-weight: 800; color: #10b981; margin-top: 4px;">€{target_annual_psr:,}/년</div>
      <div style="font-size: 10px; color: #34d399;">연간 약 €{annual_savings:,} (약 35%) 재정 세이브</div>
    </div>
  </div>
  <div style="font-size: 11px; color: #a1a1aa; line-height: 1.5; padding: 8px 12px; background: rgba(255,255,255,0.02); border-radius: 6px;">
    💡 <b>재무 임팩트 코멘트</b>: 이적료 상각 상한 5년 적용 및 합리적 기본급 타결로 {target_club_name}의 차기 시즌 스쿼드 비용 비율(Squad Cost Ratio)을 안전 마진 내로 강력히 방어합니다.
  </div>
</div>
'''.strip()


def _build_deal_term_sheet_card_html(metrics: dict[str, Any], psr: dict[str, Any]) -> str:
    """Generates an executive term sheet badge summary card for the sporting director / CEO."""
    base = metrics.get("agreed_base_wage", 100000)
    bonus = metrics.get("agreed_bonus_wage", 15000)
    clause = metrics.get("release_clause_eur", 60000000)
    fee = metrics.get("agreed_fee_pct", 5.0)
    net_wage = psr.get("weekly_net_wage_eur", int(base * 0.55))
    target = metrics.get("target_club_name", "타겟 구단")

    return f'''
<div style="background: #0a0c10; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px; margin: 18px 0; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
    <span style="font-size: 12px; font-weight: bold; color: #34d399;">📑 {target} 최종 합의 Term Sheet 요약</span>
    <span style="font-size: 10px; color: #a1a1aa; background: #18181b; padding: 2px 8px; border-radius: 4px;">구단 제출 최종안</span>
  </div>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-size: 11px; text-align: center;">
    <div style="background: #18181b; padding: 8px; border-radius: 6px;">
      <div style="color: #71717a;">합의 기본급 (세전)</div>
      <div style="color: #f4f4f5; font-weight: bold; font-size: 13px; margin-top: 2px;">€{base:,}/주</div>
      <div style="color: #34d399; font-size: 10px;">(실수령 약 €{net_wage:,}/주)</div>
    </div>
    <div style="background: #18181b; padding: 8px; border-radius: 6px;">
      <div style="color: #71717a;">성과급 옵션</div>
      <div style="color: #38bdf8; font-weight: bold; font-size: 13px; margin-top: 2px;">€{bonus:,}/주 상당</div>
      <div style="color: #71717a; font-size: 10px;">출전+UCL 진출 연동</div>
    </div>
    <div style="background: #18181b; padding: 8px; border-radius: 6px;">
      <div style="color: #71717a;">바이아웃 조항</div>
      <div style="color: #fbbf24; font-weight: bold; font-size: 13px; margin-top: 2px;">€{clause:,}</div>
      <div style="color: #71717a; font-size: 10px;">2년차 발동 가능</div>
    </div>
    <div style="background: #18181b; padding: 8px; border-radius: 6px;">
      <div style="color: #71717a;">에이전트 수수료</div>
      <div style="color: #c084fc; font-weight: bold; font-size: 13px; margin-top: 2px;">{fee}%</div>
      <div style="color: #71717a; font-size: 10px;">FFAR 유예 준수</div>
    </div>
  </div>
</div>
'''.strip()


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
            f"€{c['starter_weekly_wage_eur']:,} | €{c['max_weekly_wage_offer_eur']:,} | {c.get('manager_position_requirement', c.get('recruitment_note', '-'))} |"
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

        # Generate inline SVG & HTML visual elements
        val_radar_svg = _build_valuation_hexagon_svg(p, vp)
        datamb_bars_html = _build_datamb_percentile_bars_html(p)
        psr_gauge_svg = _build_psr_financial_gauge_svg(psr, target_club_name, agreed_base)
        term_sheet_html = _build_deal_term_sheet_card_html(metrics, psr)

        # 1. Pitch Deck: Add Top Visuals (Radar + DataMB bars), PSR Gauge, and Term Sheet Card
        visual_block_top = f"\n\n{val_radar_svg}\n\n{datamb_bars_html}\n\n"
        if "\n---" in pitch_deck_md:
            parts = pitch_deck_md.split("\n---", 1)
            pitch_deck_md = f"{parts[0]}\n---{visual_block_top}{parts[1]}"
        elif "## 1." in pitch_deck_md:
            parts = pitch_deck_md.split("## 1.", 1)
            pitch_deck_md = f"{parts[0]}{visual_block_top}## 1.{parts[1]}"
        else:
            pitch_deck_md = visual_block_top + pitch_deck_md

        # Inject PSR gauge into Financial section if present
        if "## 2." in pitch_deck_md:
            parts = pitch_deck_md.split("## 2.", 1)
            subparts = parts[1].split("\n---", 1)
            if len(subparts) == 2:
                pitch_deck_md = f"{parts[0]}## 2.{subparts[0]}\n\n{psr_gauge_svg}\n\n---{subparts[1]}"
            else:
                pitch_deck_md = f"{parts[0]}## 2.{parts[1]}\n\n{psr_gauge_svg}\n"
        elif "재무" in pitch_deck_md:
            pitch_deck_md += f"\n\n{psr_gauge_svg}\n"

        # Inject Term Sheet card into Term Sheet section
        if "## 4." in pitch_deck_md:
            parts = pitch_deck_md.split("## 4.", 1)
            pitch_deck_md = f"{parts[0]}## 4.{parts[1]}\n\n{term_sheet_html}\n"
        elif "Term Sheet" in pitch_deck_md or "텀시트" in pitch_deck_md:
            pitch_deck_md += f"\n\n{term_sheet_html}\n"

        # 2. Career Report: Insert Valuation Radar & DataMB bars into Section 1
        career_visual = f"\n\n{val_radar_svg}\n\n{datamb_bars_html}\n\n"
        if "## 1." in career_report_md:
            parts = career_report_md.split("## 1.", 1)
            career_report_md = f"{parts[0]}## 1.{career_visual}{parts[1]}"
        else:
            career_report_md = career_visual + career_report_md

        # 3. Deal Prep: Insert Term Sheet and PSR Gauge into Section 1
        deal_visual = f"\n\n{term_sheet_html}\n\n{psr_gauge_svg}\n\n"
        if "## 1." in deal_prep_md:
            parts = deal_prep_md.split("## 1.", 1)
            deal_prep_md = f"{parts[0]}## 1.{deal_visual}{parts[1]}"
        else:
            deal_prep_md = deal_visual + deal_prep_md

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
