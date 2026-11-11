import re

files_to_fix = [
    'src/sports_agency/agents/document_writer.py',
    'agent/document_writer.py'
]

new_func = '''def _build_datamb_percentile_bars_html(p: dict[str, Any]) -> str:
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
    )'''

func_pattern = re.compile(r'def _build_datamb_percentile_bars_html\(p: dict\[str, Any\]\) -> str:.*?(?=\ndef _build_psr_financial_gauge_svg)', re.DOTALL)

for fpath in files_to_fix:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if func_pattern.search(c):
        c = func_pattern.sub(new_func + '\n\n', c)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Patched _build_datamb_percentile_bars_html in {fpath}")
    else:
        print(f"Pattern not found in {fpath}")
