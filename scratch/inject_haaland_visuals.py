import sys, os
sys.path.insert(0, os.path.abspath("."))
from sports_agency.agents.document_writer import (
    _build_valuation_hexagon_svg,
    _build_datamb_percentile_bars_html,
    _build_psr_financial_gauge_svg,
    _build_deal_term_sheet_card_html,
)

# Haaland data
p = {
    "name": "Erling Haaland",
    "name_ko": "엘링 홀란",
    "position": "ST",
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
}
vp = {"highest_market_value_eur": 200000000, "international_caps": 39}
psr = {
    "annual_psr_book_cost_eur": 53860380,
    "weekly_net_wage_eur": 470250,
}
metrics = {
    "agreed_base_wage": 855000,
    "agreed_bonus_wage": 148500,
    "release_clause_eur": 290000000,
    "agreed_fee_pct": 6.5,
    "target_club_name": "Manchester City FC",
}

radar_svg = _build_valuation_hexagon_svg(p, vp)
bars_html = _build_datamb_percentile_bars_html(p)
psr_svg = _build_psr_financial_gauge_svg(psr, "Manchester City FC", 855000)
card_html = _build_deal_term_sheet_card_html(metrics, psr)

pitch_path = "outputs/Erling_Haaland/3_club_pitch_deck.md"
with open(pitch_path, "r", encoding="utf-8") as f:
    content = f.read()

# Inject top visuals if not present
if "<svg" not in content:
    top_block = f"\n\n{radar_svg}\n\n{bars_html}\n\n"
    if "## 1." in content:
        parts = content.split("## 1.", 1)
        content = f"{parts[0]}{top_block}## 1.{parts[1]}"
    
    if "## 2." in content:
        parts = content.split("## 2.", 1)
        sub = parts[1].split("\n---", 1)
        if len(sub) == 2:
            content = f"{parts[0]}## 2.{sub[0]}\n\n{psr_svg}\n\n---{sub[1]}"
        else:
            content = f"{parts[0]}## 2.{parts[1]}\n\n{psr_svg}\n"
            
    if "## 4." in content:
        parts = content.split("## 4.", 1)
        content = f"{parts[0]}## 4.{parts[1]}\n\n{card_html}\n"

    with open(pitch_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated 3_club_pitch_deck.md with visual elements successfully!")
else:
    print("Visual elements already present in 3_club_pitch_deck.md")
