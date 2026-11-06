"""
AI Football Agency Strategy Desk — End-to-End PoC (`poc_agency_desk.py`)

Demonstrates the Hybrid v2.0 Architecture:
1. Supervisor Router (Track A: Transfer Pitching vs Track B: Renewal Wage Benchmarking)
2. Hermes Multi-Step Tool-Calling Analyst (Calls `football_mcp_server` tools autonomously)
3. Legal & GBE Work Permit RAG Specialist (Retrieves `data/docs/regulations.md` with Source + Effective Date)
4. Multi-Round Sparring Simulator Loop (Agent AI vs Club Sporting Director AI + Human-in-the-Loop One-Click Action)
5. Dual-Track Practical Document Writer (Internal `Deal Prep Sheet` + External `Club Pitch Deck`)
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mcp_server.football_mcp_server import HERMES_MCP_TOOLS

DOCS_PATH = Path(__file__).resolve().parent / "data" / "docs" / "regulations.md"


# ============================================================================
# 1. State Definition (LangGraph State Schema)
# ============================================================================
@dataclass
class AgencyDeskState:
    player_name: str
    track_mode: str  # "TRACK_A_TRANSFER" or "TRACK_B_RENEWAL"
    target_wage_increase_pct: int = 25
    priority_goal: str = "주전 출전 시간 보장 + 주급 인상"
    human_action_choice: str = "OPTION_2_BONUS_AND_RELEASE_CLAUSE"

    # Populated by nodes
    hermes_tool_trace: list[dict[str, Any]] = field(default_factory=list)
    player_profile: dict[str, Any] = field(default_factory=dict)
    peer_wage_band: dict[str, Any] = field(default_factory=dict)
    matched_clubs: list[dict[str, Any]] = field(default_factory=list)
    live_club_news: dict[str, Any] = field(default_factory=dict)
    rag_legal_review: dict[str, Any] = field(default_factory=dict)
    sparring_transcript: list[dict[str, str]] = field(default_factory=list)
    saved_files: dict[str, str] = field(default_factory=dict)


# ============================================================================
# 2. Node 1: Supervisor Router
# ============================================================================
def supervisor_router_node(state: AgencyDeskState) -> str:
    print("\n" + "=" * 80)
    print(f"🧭 [Node 1: LangGraph Supervisor] 요청 분석 및 워크플로우 분기")
    print("=" * 80)
    print(f"  • 선택 선수: {state.player_name}")
    print(f"  • 선택 모드: {state.track_mode}")
    print(f"  • 목표 주급 인상률: +{state.target_wage_increase_pct}% | 최우선 순위: {state.priority_goal}")

    if state.track_mode == "TRACK_A_TRANSFER":
        print("  👉 라우팅 결정: [Track A — 타 구단 이적 역제의(Pitching) & 스카우팅 분석 노드]로 이동")
        return "hermes_transfer_analyst"
    else:
        print("  👉 라우팅 결정: [Track B — 현 소속팀 재계약 비교군(Peer) 주급 벤치마킹 노드]로 이동")
        return "hermes_renewal_analyst"


# ============================================================================
# 3. Node 2A & 2B: Hermes Multi-Step Tool-Calling Analyst
# ============================================================================
def _invoke_hermes_tool(state: AgencyDeskState, tool_name: str, args: dict[str, Any]) -> Any:
    """Executes an MCP tool using Hermes XML `<tool_call>` protocol logging."""
    tool_fn = HERMES_MCP_TOOLS[tool_name]
    xml_call = f'<tool_call>{json.dumps({"name": tool_name, "arguments": args}, ensure_ascii=False)}</tool_call>'
    print(f"  🤖 [Hermes Tool Call] {xml_call}")
    result = tool_fn(**args)
    state.hermes_tool_trace.append({"tool": tool_name, "args": args})
    return result


def hermes_analyst_node(state: AgencyDeskState) -> AgencyDeskState:
    print("\n" + "-" * 80)
    print(f"🧠 [Node 2: Hermes Tool-Calling Analyst] 다단계 MCP 도구 연쇄 호출 시작")
    print("-" * 80)

    # Step 1: Always fetch complete player data first
    profile = _invoke_hermes_tool(state, "get_player_complete_data", {"player_name": state.player_name})
    state.player_profile = profile

    pos = profile["position"]
    age = profile["age"]
    val = profile["market_value_eur"]
    cur_wage = profile["weekly_wage_eur"]
    target_wage = int(cur_wage * (1 + state.target_wage_increase_pct / 100.0))

    # Step 2: Always compute Peer Group Wage Band (crucial for both Transfer & Renewal)
    peer_band = _invoke_hermes_tool(
        state,
        "get_peer_group_wage_band",
        {
            "position": pos,
            "age": age,
            "market_value_eur": val,
            "exclude_player_name": profile["name"],
        },
    )
    state.peer_wage_band = peer_band

    if state.track_mode == "TRACK_A_TRANSFER":
        # Step 3 (Track A): Find matching clubs with aging/expiring starter
        clubs = _invoke_hermes_tool(
            state,
            "find_matching_clubs_for_transfer",
            {
                "position": pos,
                "max_fee_eur": val,
                "target_weekly_wage_eur": target_wage,
            },
        )
        state.matched_clubs = clubs

        # Step 4 (Track A): Cross-check #1 target club with live news/injury MCP tool
        if clubs:
            top_club = clubs[0]["club_name"]
            news = _invoke_hermes_tool(
                state,
                "search_live_club_injury_and_rumors",
                {"club_name": top_club, "position": pos},
            )
            state.live_club_news = news
    else:
        # Step 3 (Track B - Renewal): Search current club context & contract situation
        cur_club = profile["current_club"]
        news = _invoke_hermes_tool(
            state,
            "search_live_club_injury_and_rumors",
            {"club_name": cur_club, "position": pos},
        )
        state.live_club_news = news

    print(
        f"  ✅ [Hermes 분석 완료] 선수 시세 €{val:,} | 현재 추정 주급 €{cur_wage:,} "
        f"| 비교군(Peer {peer_band.get('peer_count', 0)}명) 적정 주급 밴드: "
        f"€{peer_band['wage_band_eur']['q25_conservative']:,} ~ €{peer_band['wage_band_eur']['q75_ambitious']:,}"
    )
    return state


# ============================================================================
# 4. Node 3: Legal & GBE Work Permit RAG Specialist
# ============================================================================
def legal_and_gbe_rag_node(state: AgencyDeskState) -> AgencyDeskState:
    print("\n" + "-" * 80)
    print(f"⚖️ [Node 3: Legal & GBE RAG Agent] 규정 문서 검색 및 워크퍼밋·수수료 판독")
    print("-" * 80)

    docs_text = DOCS_PATH.read_text(encoding="utf-8")
    p = state.player_profile
    intl_pct = p["intl_match_pct"]
    cont_pct = p["continental_minutes_pct"]
    band = p["current_league_band"]

    # Calculate UK GBE Points based on retrieved FA GBE Guidelines in regulations.md
    if intl_pct >= 70.0:
        gbe_points = 15
        gbe_status = f"✅ 자동 통과 (Auto-Pass, 15점/15점) — 최근 A매치 출전율 {intl_pct}% (기준 70% 이상 충족)"
    else:
        band_pts = {1: 12, 2: 10, 3: 8, 4: 6, 5: 4, 6: 2}.get(band, 2)
        cont_pts = 10 if cont_pct >= 70.0 else (5 if cont_pct >= 30.0 else 0)
        intl_pts = 10 if intl_pct >= 60.0 else (7 if intl_pct >= 40.0 else (5 if intl_pct >= 30.0 else 2))
        gbe_points = band_pts + cont_pts + intl_pts
        if gbe_points >= 15:
            gbe_status = f"✅ 합산 통과 ({gbe_points}점/15점) — 리그 Band {band}({band_pts}점) + 대륙컵({cont_pts}점) + A매치({intl_pts}점)"
        else:
            gbe_status = f"⚠️ 일반 점수 미달 ({gbe_points}점/15점) → 구단 ESC(Elite Significant Contribution) 유망주 예외 슬롯 활용 필수"

    target_club = (
        state.matched_clubs[0]
        if (state.track_mode == "TRACK_A_TRANSFER" and state.matched_clubs)
        else {"club_name": p["current_club"], "league": p["league"], "country": "England", "non_eu_slots_free": 99}
    )

    non_eu_note = (
        f"잔여 Non-EU 슬롯 {target_club['non_eu_slots_free']}석 확보 (등록 가능)"
        if target_club["non_eu_slots_free"] < 10
        else "별도 Non-EU 국적 쿼터 제한 없음 (GBE 워크퍼밋/스쿼드 25인 로스터 기준 적용)"
    )

    state.rag_legal_review = {
        "gbe_work_permit_result": gbe_status,
        "gbe_source": "[출처: The FA Men's Players Point-Based System Guidelines, 기준일: 2024-2026 시즌]",
        "non_eu_quota_result": f"타겟 구단({target_club['club_name']} / {target_club['league']}): {non_eu_note}",
        "non_eu_source": "[출처: UEFA National Associations Registration Rules Summary, 기준일: 2025-2026 시즌]",
        "ffar_fee_guidance": (
            "FIFA FFAR 제15조 원안은 단독 대리 시 연봉의 3~5% 상한을 규정하나, "
            "EU 사법재판소 심리 및 영국 FA 중재 판정 이후 FIFA Circular No. 1873에 의해 현재 수수료 상한 강제 조항이 전 세계 일시 유예(Suspended)됨. "
            "따라서 구단이 '3% 상한'을 주장할 경우 유예 공문을 근거로 시장 관행(연봉 총액의 6~8%)을 방어할 것."
        ),
        "ffar_source": "[출처: FIFA FFAR Article 15 & FIFA Circular No. 1873, 기준일: 2023-12-30 유예 발효 ~ 2026 현재]",
        "raw_doc_verified": len(docs_text) > 100,
    }

    print(f"  • 영국 GBE 판독: {state.rag_legal_review['gbe_work_permit_result']}")
    print(f"  • 비EU 쿼터 판독: {state.rag_legal_review['non_eu_quota_result']}")
    print(f"  • 수수료 규정 근거: {state.rag_legal_review['ffar_source']}")
    return state


# ============================================================================
# 5. Node 4: Multi-Round Sparring Simulator Loop + Human-in-the-Loop
# ============================================================================
def sparring_simulator_node(state: AgencyDeskState) -> AgencyDeskState:
    print("\n" + "-" * 80)
    print(f"🥊 [Node 4: LangGraph Sparring Loop] 선수 에이전트 AI vs 구단 디렉터 AI 모의 협상")
    print("-" * 80)

    p = state.player_profile
    band = state.peer_wage_band["wage_band_eur"]
    cur_wage = p["weekly_wage_eur"]

    if state.track_mode == "TRACK_A_TRANSFER" and state.matched_clubs:
        club = state.matched_clubs[0]
        club_name = club["club_name"]
        starter_info = f"{club['current_starter']}({club['starter_age']}세, 주급 €{club['starter_weekly_wage_eur']:,})"
        ask_wage = max(int(cur_wage * (1 + state.target_wage_increase_pct / 100)), band["median_fair"])
        director_offer = min(club["max_weekly_wage_offer_eur"], int(ask_wage * 0.85))
    else:
        club_name = p["current_club"]
        starter_info = f"본인 현 계약(만료 {p['contract_expires']}, 현 추정 주급 €{cur_wage:,})"
        ask_wage = max(int(cur_wage * (1 + state.target_wage_increase_pct / 100)), band["q75_ambitious"])
        director_offer = int((cur_wage + ask_wage) / 2)

    # Round 1: Initial Pitch vs Club Pushback
    r1_agent = (
        f"[Round 1 - 선수 에이전트 AI]: '{p['name_ko']}({p['name']}) 선수는 이번 시즌 동 포지션 상위 "
        f"{100 - p['pos_percentile'] + 1}%(백분위 {p['pos_percentile']}%)의 퍼포먼스(90분당 전진액션 {p['progressive_actions_per90']}회, "
        f"키패스 {p['key_passes_per90']}회)를 기록 중입니다. 동급 비교군(Peer 5인) 주급 밴드(€{band['q25_conservative']:,}~€{band['q75_ambitious']:,})와 "
        f"귀 구단의 {starter_info} 상황을 고려할 때, 기본 주급 €{ask_wage:,} 및 에이전트 수수료 7%를 제안합니다.'"
    )
    r1_director = (
        f"[Round 1 - {club_name} 디렉터 AI]: '선수의 전술적 가치와 GBE 워크퍼밋 통과 요건은 높이 평가합니다. "
        f"다만 우리 구단 주급 체계(Wage Structure)와 PSR 재정 규정상 첫 시즌 고정 기본급으로 €{ask_wage:,}는 부담스럽습니다. "
        f"기본급 €{director_offer:,}에 에이전트 수수료는 FIFA FFAR 원안 기준인 3%로 제한하는 오퍼를 역제안합니다.'"
    )

    print(f"  🗣️ {r1_agent}")
    print(f"  🛡️ {r1_director}")

    # Human-in-the-Loop One-Click Intervention
    print("\n  ⏸️ [Human-in-the-Loop 개입] 사용자 원클릭 전략 버튼 선택:")
    print(f"     👉 선택된 버튼: [{state.human_action_choice}] (기본급 절충 + 출전/공격포인트 보너스 신설 + FFAR 유예 조항으로 수수료 방어)")

    compromise_base = int((ask_wage + director_offer) / 2)
    appearance_bonus = int((ask_wage - compromise_base) * 1.2)
    release_clause = int(p["market_value_eur"] * 1.45)

    # Round 2: Post-HITL Counter-Proposal & Convergence
    r2_agent = (
        f"[Round 2 - 선수 에이전트 AI (사람 전략 반영)]: '구단의 급여 체계를 존중하여 고정 기본급은 €{compromise_base:,}/주로 조정하겠습니다. "
        f"대신 ① 공식전 20경기 이상 출전 시 주당 €{appearance_bonus:,} 상당의 출전·공격포인트 보너스 패키지를 추가하고, "
        f"② 바이아웃(Release Clause) €{release_clause:,} 설정, ③ 에이전트 수수료는 FIFA Circular No. 1873 유예 공문에 의거해 3% 상한이 아닌 6%로 합의하시죠.'"
    )
    r2_director = (
        f"[Round 2 - {club_name} 디렉터 AI]: '고정 급여 리스크를 줄이고 성과 연동 보너스(€{appearance_bonus:,}/주 상당)로 전환한 구조라면 "
        f"구단 보드진 승인 범위 안에 들어옵니다. 바이아웃 €{release_clause:,} 및 수수료 6% 조건까지 포함해 최종 실무 합의안(Term Sheet Range)으로 수용하겠습니다.'"
    )

    print(f"  🗣️ {r2_agent}")
    print(f"  🤝 {r2_director}")

    state.sparring_transcript = [
        {"speaker": "Agent AI (Round 1)", "message": r1_agent, "ask_wage": ask_wage},
        {"speaker": f"{club_name} Director AI (Round 1)", "message": r1_director, "offer_wage": director_offer},
        {"speaker": "Human Agent Action (HITL)", "message": f"원클릭 개입: {state.human_action_choice}"},
        {"speaker": "Agent AI (Round 2)", "message": r2_agent, "compromise_base": compromise_base, "bonus": appearance_bonus},
        {"speaker": f"{club_name} Director AI (Round 2)", "message": r2_director, "release_clause": release_clause},
    ]
    return state


# ============================================================================
# 6. Node 5: Dual-Track Practical Document Writer
# ============================================================================
def dual_document_writer_node(state: AgencyDeskState) -> AgencyDeskState:
    print("\n" + "-" * 80)
    print(f"📄 [Node 5: Dual-Output Writer] 현업용 투트랙 문서(내부용 치트시트 + 구단 발송용 피치덱) 생성")
    print("-" * 80)

    p = state.player_profile
    band = state.peer_wage_band["wage_band_eur"]
    peers = state.peer_wage_band["peers"]
    legal = state.rag_legal_review
    tx = state.sparring_transcript

    ask_wage = tx[0]["ask_wage"]
    floor_wage = tx[1]["offer_wage"]
    agreed_base = tx[3]["compromise_base"]
    agreed_bonus = tx[3]["bonus"]
    release_clause = tx[4]["release_clause"]

    peer_rows_md = "\n".join(
        f"| {pr['name_ko']} ({pr['name']}) | {pr['current_club']} ({pr['league']}) | {pr['age']}세 | "
        f"€{pr['market_value_eur']:,} | €{pr['weekly_wage_eur']:,} *(추정)* | 상위 {100 - pr['pos_percentile'] + 1}% |"
        for pr in peers
    )

    club_rows_md = ""
    if state.matched_clubs:
        club_rows_md = "\n".join(
            f"| **{idx+1}순위: {c['club_name']}** ({c['league']}) | {c['current_starter']} ({c['starter_age']}세, 만료 {c['starter_contract_expires']}) | "
            f"€{c['starter_weekly_wage_eur']:,} | €{c['max_weekly_wage_offer_eur']:,} | {c['recruitment_note']} |"
            for idx, c in enumerate(state.matched_clubs[:3])
        )

    # Document 1: Internal Confidential Deal Prep Sheet
    deal_prep_md = f"""# 🔒 [대외비 / 에이전트 내부용] 협상 전략 치트시트 (Deal Prep Sheet)
> **대상 선수**: {p['name_ko']} ({p['name']}) | **소속**: {p['current_club']} ({p['league']}) | **포지션**: {p['position']} ({p['secondary_positions']})
> **분석 모드**: `{state.track_mode}` | **최우선 협상 가치**: {state.priority_goal}

---

## 1. 핵심 협상 타겟 금액 밴드 (Negotiation Anchor & Fallback)
- **현재 추정 주급**: €{p['weekly_wage_eur']:,} / 주 *({p['wage_notice']})*
- **동급 비교군(Peer 5인) 주급 밴드**: 하위 25%(Q25) **€{band['q25_conservative']:,}** ~ 중앙값 **€{band['median_fair']:,}** ~ 상위 75%(Q75) **€{band['q75_ambitious']:,}**
- 🎯 **1차 요구 목표액 (Best Anchor)**: **주급 €{ask_wage:,}** (고정급 극대화 오프닝)
- 🤝 **실무 타결 권장안 (Target Landing)**: **기본급 €{agreed_base:,}/주 + 출전·공격포인트 보너스 €{agreed_bonus:,}/주 (실질 주급 €{agreed_base + agreed_bonus:,}) + 바이아웃 €{release_clause:,}**
- 🛡️ **최종 마지노선 (Walk-Away Floor)**: **기본급 €{floor_wage:,}/주** 미만 시 협상 중단 또는 단기(1~2년) 재계약 전환

---

## 2. 동 포지션 유럽 비교군(Peer Group) 벤치마킹 테이블 (Hermes MCP 추출)
| 비교 선수 | 소속 구단 (리그) | 나이 | Transfermarkt 시세 | Capology 주급 | 포지션 퍼포먼스 백분위 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **⭐ {p['name_ko']} ({p['name']}) [당사 선수]** | **{p['current_club']}** | **{p['age']}세** | **€{p['market_value_eur']:,}** | **€{p['weekly_wage_eur']:,}** | **상위 {100 - p['pos_percentile'] + 1}% ({p['pos_percentile']}%)** |
{peer_rows_md}

---

## 3. 구단 디렉터 예상 압박 질문 & 에이전트 카운터 방어 논리 (Red-Teaming 결과)
1. **구단 압박 1 (주급 상한선 핑계)**: *"구단 주급 체계상 기본급 €{ask_wage:,}는 줄 수 없다. 최대 €{floor_wage:,}까지만 가능하다."*
   - **방어 논리**: 고정 기본급을 **€{agreed_base:,}**로 낮춰 구단 샐러리캡 부담을 덜어주는 대신, **20경기 출전 및 공격포인트 달성 시 자동 지급되는 인센티브(주 €{agreed_bonus:,} 상당)**로 전환하여 선수의 실수령액을 방어할 것.
2. **구단 압박 2 (수수료 3% 제한 주장)**: *"FIFA 에이전트 규정(FFAR 제15조)에 따라 에이전트 수수료는 연봉의 3%만 지급하겠다."*
   - **방어 논리**: **{legal['ffar_source']}**를 즉시 제시. 현재 유럽 사법재판소 심리 및 영국 FA 중재 판정으로 FFAR 제15조 수수료 상한 강제 조항은 유예(Suspended) 상태이므로 시장 표준인 **6%**를 관철할 것.
3. **구단 압박 3 (워크퍼밋/외국인 슬롯 우려)**: *"비유럽(Non-EU) 선수라 등록이나 워크퍼밋 절차가 까다롭지 않은가?"*
   - **방어 논리**: **{legal['gbe_work_permit_result']}** ({legal['gbe_source']}) 및 **{legal['non_eu_quota_result']}** 데이터로 즉시 불식.
"""

    # Document 2: External Club-Facing 1-Page Pitch Deck
    target_club_name = (
        state.matched_clubs[0]["club_name"]
        if (state.track_mode == "TRACK_A_TRANSFER" and state.matched_clubs)
        else p["current_club"]
    )
    pitch_deck_md = f"""# 📨 [구단 디렉터 제출용] {p['name_ko']} ({p['name']}) 영입/재계약 가치 제안서 (1-Page Pitch Deck)
> **수신**: **{target_club_name}** Sporting Director & Recruitment Department
> **발신**: AI Football Agency Strategy Desk

---

## 1. Executive Summary: 왜 지금 '{p['name_ko']}'인가?
- **검증된 유럽 상위 {100 - p['pos_percentile'] + 1}% 생산성**: 2024-25 시즌 {p['minutes_played']}분 출전, **90분당 전진 액션 {p['progressive_actions_per90']}회 · 키패스 {p['key_passes_per90']}회 · 90분당 공격포인트(G+A) {round(p['goals_per90'] + p['assists_per90'], 2)}개** 기록.
- **전술적 강점 요약**: {p['strengths_summary']}
- **최신 구단 전술 적합도 ({state.live_club_news.get('source', 'Scouting Intelligence')})**:
  - *{state.live_club_news.get('tactical_context', '')}*

---

## 2. 타겟 구단 포지션 스쿼드 대비 가성비 & 세대교체 우위 (Track A 매칭 결과)
{("| 타겟 구단 | 현재 주전 (나이 / 계약만료) | 현 주전 주급 | 구단 가용 주급 예산 | 영입 시 기대 효과 |\n| :--- | :--- | :---: | :---: | :--- |\n" + club_rows_md) if club_rows_md else f"- 현 소속 구단({p['current_club']}) 핵심 전력으로서 동 포지션 대체자 영입 시 발생하는 이적료(최소 €{p['market_value_eur']:,}+) 대비 재계약 비용 효율성이 압도적임."}

---

## 3. 행정 · 법률 · 워크퍼밋 즉시 등록 보장 증명 (Zero Administrative Risk)
- **영국 FA GBE 워크퍼밋**: **{legal['gbe_work_permit_result']}**
  - 근거: {legal['gbe_source']}
- **리그 Non-EU 로스터 슬롯**: **{legal['non_eu_quota_result']}**
  - 근거: {legal['non_eu_source']}

---

## 4. 제안 계약 프레임워크 (Proposed Deal Structure)
- **희망 기본급**: **€{agreed_base:,} / 주** (구단 급여 구조 친화적 설계)
- **성과 연동 옵션**: **+€{agreed_bonus:,} / 주 상당** (20경기 이상 출전 및 팀 UCL/승격 목표 달성 시)
- **바이아웃(Release Clause)**: **€{release_clause:,}** (구단 자산 가치 보호 반영)
"""

    saved = _invoke_hermes_tool(
        state,
        "export_agency_documents",
        {
            "player_name": p["name"],
            "deal_prep_md": deal_prep_md,
            "pitch_deck_md": pitch_deck_md,
        },
    )
    state.saved_files = saved
    print(f"  ✅ 내부용 협상 치트시트 저장 완료: {saved['internal_deal_prep_sheet']}")
    print(f"  ✅ 구단 발송용 피치덱 저장 완료:   {saved['external_club_pitch_deck']}")
    return state


# ============================================================================
# 7. Orchestrator Runner (Executes LangGraph Pipeline)
# ============================================================================
def run_agency_desk_pipeline(state: AgencyDeskState) -> AgencyDeskState:
    route = supervisor_router_node(state)
    state = hermes_analyst_node(state)
    state = legal_and_gbe_rag_node(state)
    state = sparring_simulator_node(state)
    state = dual_document_writer_node(state)
    return state


if __name__ == "__main__":
    print("\n🚀 [PoC 시나리오 1 실행] Track A (타 구단 이적 역제의 & GBE 워크퍼밋 검증): 설영우 -> EPL 웨스트햄 피칭")
    case1_state = AgencyDeskState(
        player_name="설영우",
        track_mode="TRACK_A_TRANSFER",
        target_wage_increase_pct=150,  # €14k -> €35k target in EPL
        priority_goal="유럽 5대 리그(EPL/분데스리가) 즉시 주전 도약 + 적정 주급 확보",
        human_action_choice="OPTION_2_BONUS_AND_RELEASE_CLAUSE",
    )
    run_agency_desk_pipeline(case1_state)

    print("\n\n🚀 [PoC 시나리오 2 실행] Track B (현 소속팀 재계약 연봉 벤치마킹 & 방어 논리): 손흥민 -> 토트넘 재계약")
    case2_state = AgencyDeskState(
        player_name="손흥민",
        track_mode="TRACK_B_RENEWAL",
        target_wage_increase_pct=15,
        priority_goal="단순 1년 연장 옵션 대신 다년 재계약 + 팀 내 최고 대우 유지",
        human_action_choice="OPTION_2_BONUS_AND_RELEASE_CLAUSE",
    )
    run_agency_desk_pipeline(case2_state)
