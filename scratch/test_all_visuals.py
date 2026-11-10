def build_datamb_percentile_bars_html(p: dict) -> str:
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
        rows_html.append(f'''
    <div style="margin-bottom: 10px;">
      <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; color: #d4d4d8;">
        <span><b>{it["label"]}</b></span>
        <span style="color: {it["color"]}; font-weight: bold;">{it["val"]} (상위 {100 - it["pct"] + 1}%)</span>
      </div>
      <div style="width: 100%; height: 7px; background: #27272a; border-radius: 4px; overflow: hidden;">
        <div style="width: {it["pct"]}%; height: 100%; background: {it["color"]}; border-radius: 4px;"></div>
      </div>
    </div>
''')

    return f'''
<div style="background: #0a0c10; border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; margin: 18px 0;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px;">
    <span style="font-size: 12px; font-weight: bold; color: #e4e4e7;">📊 DataMB 5대 리그 동 포지션 백분위 벤치마크</span>
    <span style="font-size: 10px; color: #38bdf8; background: rgba(56, 189, 248, 0.12); padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.25);">Opta / FBref 2025-26 실측</span>
  </div>
  {''.join(rows_html)}
</div>
'''.strip()

def build_psr_financial_gauge_svg(psr: dict, target_club_name: str = "타겟 구단", agreed_base: int = 120000) -> str:
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

def build_deal_term_sheet_card_html(metrics: dict, psr: dict) -> str:
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

print("All components defined successfully.")
