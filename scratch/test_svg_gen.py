import math

def build_valuation_hexagon_svg(p: dict, vp: dict = None) -> str:
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

    # Grid rings
    grid_polys = []
    for step in [0.25, 0.5, 0.75, 1.0]:
        pts = [f"{cx + r * step * math.cos(a):.1f},{cy + r * step * math.sin(a):.1f}" for a in angles]
        grid_polys.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="#27272a" stroke-width="1" />')

    # Spoke lines & labels
    spokes = []
    for i, a in enumerate(angles):
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        lx = cx + (r + 26) * math.cos(a)
        ly = cy + (r + 26) * math.sin(a)
        spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#27272a" stroke-width="1" />')
        anchor = "middle"
        if math.cos(a) > 0.3: anchor = "start"
        elif math.cos(a) < -0.3: anchor = "end"
        spokes.append(
            f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" fill="#a1a1aa" font-size="11" font-weight="600" font-family="system-ui, sans-serif">{labels[i]} <tspan fill="#34d399" font-weight="bold">{scores[i]}</tspan></text>'
        )

    # Data polygon
    data_pts = [f"{cx + r * (scores[i] / 100.0) * math.cos(a):.1f},{cy + r * (scores[i] / 100.0) * math.sin(a):.1f}" for i, a in enumerate(angles)]
    poly_str = " ".join(data_pts)

    # Vertex dots
    dots = [f'<circle cx="{pt.split(",")[0]}" cy="{pt.split(",")[1]}" r="4" fill="#10b981" stroke="#ffffff" stroke-width="1.5" />' for pt in data_pts]

    svg = f'''
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
'''
    return svg.strip()

p = {"name": "Erling Haaland", "market_value_eur": 200000000, "weekly_wage_eur": 450000, "age": 24, "minutes_played": 3131, "contract_expires": "2034-06", "intl_match_pct": 88.0}
print(build_valuation_hexagon_svg(p)[:300])
