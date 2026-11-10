import sys
sys.path.append('.')
from mcp_server.football_mcp_server import list_agency_recruitment_targets

res = list_agency_recruitment_targets()
print("Total targets:", res["total_targets"])
for t in res["targets"]:
    mv = t.get('market_value_eur') or 0
    ppg = t.get('points_per_game') or 0
    wage = t.get('weekly_wage_eur') or 0
    print(f"[{t['target_type']}] {t['name_ko']} ({t['name']}) | Club: {t['current_club']} | Cat: {t['category']} | MV: €{mv:,} | PPG: {ppg} | Wage: €{wage:,}")
