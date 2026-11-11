"""
One-click Contract Compliance Audit (계약 컴플라이언스 원클릭 감사).

Deterministic (no LLM) audit of a player/deal against:
  1. FIFA FFAR Art. 12  - representation contract term (max 24 months)
  2. FIFA FFAR Art. 13/15 - agent service-fee cap (by annual remuneration & who engages the agent)
  3. FIFA FFAR dual representation (conflict of interest)
  4. FIFA RSTP Art. 18(3) / Bosman - pre-contract negotiation window (<= 6 months)
  5. UK FA GBE work-permit points (only when the destination league is the Premier League)
  6. PSR / FSR - amortisation cap & annual book-cost headroom

Every check returns status in {PASS, WARN, FAIL, INFO} plus a human readable detail and an optional
regulation citation retrieved from the SQLite vector store (best-effort).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from mcp_server.football_mcp_server import (
    _get_conn,
    calculate_gbe_points_from_db,
    calculate_psr_and_tax_breakdown,
)

USD_EUR_APPROX = 0.92  # FFAR thresholds are in USD; DB wages are EUR
FFAR_REMUNERATION_THRESHOLD_USD = 200_000
GBP_EUR_APPROX = 1.17
PSR_THREE_YEAR_LOSS_LIMIT_EUR = int(105_000_000 * GBP_EUR_APPROX)  # EPL PSR GBP 105M / 3 seasons


def _citation(category: str, query: str) -> str | None:
    """Best-effort regulation citation from the vector store (never raises)."""
    try:
        from sports_agency.rag.sqlite_vector_store import VECTOR_STORE

        hits = VECTOR_STORE.search_regulations(query=query, top_k=1, category_filter=category)
        if hits:
            ch = hits[0]
            return f"{ch['source_citation']} (기준일: {ch['effective_date']})"
    except Exception:
        return None
    return None


def _check(key: str, title: str, status: str, detail: str, citation: str | None = None, data: dict | None = None) -> dict:
    return {
        "key": key,
        "title": title,
        "status": status,
        "detail": detail,
        "citation": citation,
        "data": data or {},
    }


def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def run_compliance_audit(
    player_id: int,
    weekly_wage_eur: int | None = None,
    transfer_fee_eur: int = 0,
    contract_years: int = 4,
    agent_fee_pct: float = 5.0,
    representation_months: int = 24,
    engaged_by: str = "PLAYER",
    destination_league: str | None = None,
    also_represents_club: bool = False,
    signing_bonus_eur: int = 0,
) -> dict[str, Any]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {"error": f"Player ID {player_id} not found"}
    p = dict(row)

    engaged_by = (engaged_by or "PLAYER").upper()
    dest_league = destination_league or p.get("league") or "Premier League"
    wage = int(weekly_wage_eur if weekly_wage_eur is not None else (p.get("weekly_wage_eur") or 0))
    annual_remuneration_eur = wage * 52
    checks: list[dict] = []

    # 1. Representation contract term (FFAR Art. 12)
    if representation_months > 24:
        checks.append(_check(
            "rep_term", "대리 계약 기간 (FFAR 제12조)", "FAIL",
            f"{representation_months}개월 설정 — 최대 24개월 초과, 자동 연장 조항은 무효입니다.",
            _citation("FIFA_FFAR_FEE", "FIFA FFAR representation contract maximum 24 months Article 12"),
            {"months": representation_months, "limit": 24},
        ))
    else:
        checks.append(_check(
            "rep_term", "대리 계약 기간 (FFAR 제12조)", "PASS",
            f"{representation_months}개월 — 최대 24개월 이내입니다.",
            _citation("FIFA_FFAR_FEE", "FIFA FFAR representation contract maximum 24 months Article 12"),
            {"months": representation_months, "limit": 24},
        ))

    # 2. Service fee cap (FFAR Art. 13/15)
    over_threshold = annual_remuneration_eur * (1 / USD_EUR_APPROX) > FFAR_REMUNERATION_THRESHOLD_USD
    if engaged_by == "CLUB":
        cap = 6.0 if over_threshold else 10.0
    else:
        cap = 3.0 if over_threshold else 5.0
    cap_note = (
        f"{'선수' if engaged_by != 'CLUB' else '구단'} 측 고용, 연 보수 약 €{annual_remuneration_eur:,} "
        f"({'20만 달러 초과' if over_threshold else '20만 달러 이하'}) → 상한 {cap:.1f}%"
    )
    fee_note = " ※ Circular No. 1873 에 따라 FFAR 수수료 상한은 법원 판결로 잠정 유예 중이므로 로컬 규정을 병행 확인하세요."
    if agent_fee_pct > cap:
        checks.append(_check(
            "fee_cap", "에이전트 수수료 상한 (FFAR 제13·15조)", "FAIL",
            f"요율 {agent_fee_pct:.1f}% > 상한 {cap:.1f}%. {cap_note}.{fee_note}",
            _citation("FIFA_FFAR_FEE", "FIFA FFAR Article 15 service fee cap Circular 1873"),
            {"requested_pct": agent_fee_pct, "cap_pct": cap},
        ))
    else:
        checks.append(_check(
            "fee_cap", "에이전트 수수료 상한 (FFAR 제13·15조)", "PASS",
            f"요율 {agent_fee_pct:.1f}% ≤ 상한 {cap:.1f}%. {cap_note}.{fee_note}",
            _citation("FIFA_FFAR_FEE", "FIFA FFAR Article 15 service fee cap Circular 1873"),
            {"requested_pct": agent_fee_pct, "cap_pct": cap},
        ))

    # 3. Dual representation / conflict of interest
    if also_represents_club:
        checks.append(_check(
            "dual_rep", "이중 대리 금지 (이해충돌)", "FAIL",
            "구단과 선수를 동시에 대리할 수 없습니다. 한쪽 대리를 포기하거나 서면 동의 절차가 필요합니다.",
            _citation("FIFA_FFAR_FEE", "FIFA FFAR dual representation conflict of interest"),
        ))
    elif p.get("is_agency_client"):
        checks.append(_check(
            "dual_rep", "이중 대리 금지 (이해충돌)", "INFO",
            "이미 당사 전속 고객입니다. 상대 구단 대리 여부만 확인하세요.",
        ))
    else:
        checks.append(_check(
            "dual_rep", "이중 대리 금지 (이해충돌)", "PASS",
            "단독 대리인으로 진행됩니다. (기존 에이전시 해지 여부는 별도 확인 필요)",
        ))

    # 4. Bosman / RSTP Art. 18(3)
    expiry = _parse_date(p.get("contract_expires"))
    if expiry:
        days = (expiry - date.today()).days
        if days < 0:
            checks.append(_check(
                "bosman", "계약 만료 / 보스만 룰 (RSTP 제18조 3항)", "PASS",
                f"계약이 {-days}일 전에 만료되어 FA 신분입니다. 자유롭게 협상 가능합니다.",
                _citation("PSR_CONTRACT_LAW", "FIFA RSTP Article 18 Bosman 6 months pre-contract"),
                {"days_to_expiry": days},
            ))
        elif days <= 183:
            checks.append(_check(
                "bosman", "계약 만료 / 보스만 룰 (RSTP 제18조 3항)", "PASS",
                f"만료 D-{days}. 6개월 이내이므로 타 구단과 사전 계약(Pre-contract) 협상이 가능합니다.",
                _citation("PSR_CONTRACT_LAW", "FIFA RSTP Article 18 Bosman 6 months pre-contract"),
                {"days_to_expiry": days},
            ))
        else:
            checks.append(_check(
                "bosman", "계약 만료 / 보스만 룰 (RSTP 제18조 3항)", "WARN",
                f"만료 D-{days} ({expiry}). 6개월 초과 — 현 소속 구단 동의 없이 타 구단과 협상하면 규정 위반입니다.",
                _citation("PSR_CONTRACT_LAW", "FIFA RSTP Article 18 Bosman 6 months pre-contract"),
                {"days_to_expiry": days},
            ))
    else:
        checks.append(_check("bosman", "계약 만료 / 보스만 룰 (RSTP 제18조 3항)", "INFO", "계약 만료일 정보가 없습니다."))

    # 5. UK FA GBE (Premier League only)
    gbe = None
    if dest_league == "Premier League":
        try:
            gbe = calculate_gbe_points_from_db(
                intl_match_pct=float(p.get("intl_match_pct") or 0),
                continental_minutes_pct=float(p.get("continental_minutes_pct") or 0),
                league_band=int(p.get("current_league_band") or 0),
            )
            checks.append(_check(
                "gbe", "UK FA GBE 워크퍼밋 (15점)", "PASS" if gbe["passed"] else "WARN",
                gbe["status_summary"],
                _citation("GBE_WORK_PERMIT", "영국 FA GBE 워크퍼밋 점수 산정 Auto-Pass ESC"),
                {"points": gbe["total_points"], "threshold": gbe["pass_threshold"], "auto_pass": gbe["is_auto_pass"]},
            ))
        except Exception as exc:  # noqa: BLE001
            checks.append(_check("gbe", "UK FA GBE 워크퍼밋 (15점)", "INFO", f"GBE 산정 불가: {exc}"))
    else:
        checks.append(_check(
            "gbe", "UK FA GBE 워크퍼밋 (15점)", "INFO",
            f"목적지 리그({dest_league})는 영국 GBE 적용 대상이 아닙니다.",
        ))

    # 6. PSR / FSR
    psr = None
    if transfer_fee_eur > 0 or wage > 0:
        psr = calculate_psr_and_tax_breakdown(
            league=dest_league,
            transfer_fee_eur=int(transfer_fee_eur),
            weekly_wage_eur=wage,
            contract_years=int(contract_years),
            agent_fee_pct=float(agent_fee_pct),
            signing_bonus_eur=int(signing_bonus_eur),
        )
        annual_cost = psr["annual_psr_book_cost_eur"]
        share = annual_cost / (PSR_THREE_YEAR_LOSS_LIMIT_EUR / 3) * 100
        amort_capped = int(contract_years) > psr["amortization_years_applied"]
        status = "PASS"
        notes = [f"연간 PSR 장부비용 €{annual_cost:,} (연 손실 허용 한도 약 €{PSR_THREE_YEAR_LOSS_LIMIT_EUR // 3:,} 대비 {share:.0f}%)"]
        if share > 100:
            status = "FAIL"
            notes.append("이 선수 한 명만으로 연간 손실 허용 한도를 초과합니다.")
        elif share > 50:
            status = "WARN"
            notes.append("한도의 절반 이상을 소진합니다. 구단 재무 여력 확인이 필요합니다.")
        if amort_capped:
            status = "WARN" if status == "PASS" else status
            notes.append(f"계약 {contract_years}년 중 감가상각은 최대 {psr['amortization_years_applied']}년까지만 인정됩니다.")
        checks.append(_check(
            "psr", "PSR / FSR 재무 건전성", status, " · ".join(notes),
            _citation("PSR_CONTRACT_LAW", "EPL PSR UEFA FSR 이적료 감가상각 5년 RSTP Article 18"),
            {"annual_psr_book_cost_eur": annual_cost, "share_of_annual_limit_pct": round(share, 1)},
        ))
    else:
        checks.append(_check("psr", "PSR / FSR 재무 건전성", "INFO", "이적료·주급 입력이 없어 재무 감사를 건너뛰었습니다."))

    counts = {s: sum(1 for c in checks if c["status"] == s) for s in ("PASS", "WARN", "FAIL", "INFO")}
    if counts["FAIL"]:
        verdict, verdict_label = "BLOCKED", "❌ 계약 발행 불가 — 위반 항목을 먼저 해소하세요"
    elif counts["WARN"]:
        verdict, verdict_label = "REVIEW", "⚠️ 조건부 승인 — 경고 항목 확인 후 진행"
    else:
        verdict, verdict_label = "CLEARED", "✅ 컴플라이언스 통과 — 계약 발행 가능"

    return {
        "status": "success",
        "player": {
            "player_id": p["player_id"],
            "name": p["name"],
            "name_ko": p.get("name_ko"),
            "club": p.get("current_club"),
            "league": p.get("league"),
            "nationality": p.get("nationality"),
            "contract_expires": p.get("contract_expires"),
        },
        "inputs": {
            "weekly_wage_eur": wage,
            "transfer_fee_eur": int(transfer_fee_eur),
            "contract_years": int(contract_years),
            "agent_fee_pct": float(agent_fee_pct),
            "representation_months": int(representation_months),
            "engaged_by": engaged_by,
            "destination_league": dest_league,
            "also_represents_club": bool(also_represents_club),
        },
        "checks": checks,
        "summary": counts,
        "verdict": verdict,
        "verdict_label": verdict_label,
        "audited_at": datetime.now().isoformat(timespec="seconds"),
    }
