import sys
sys.path.insert(0, '.')
import sqlite3
from mcp_server.football_mcp_server import get_player_complete_data, find_matching_clubs_for_transfer

def test_matches(player_name):
    p_data = get_player_complete_data(player_name)
    pos = p_data.get('position', 'FW')
    market_val = p_data.get('market_value_eur', 30000000)
    curr_wage = p_data.get('weekly_wage_eur', 100000)
    target_wage = int(curr_wage * 1.3)

    matches = find_matching_clubs_for_transfer(
        position=pos,
        max_fee_eur=market_val,
        target_weekly_wage_eur=target_wage,
        preferred_league="ALL"
    )
    print(f"Results for {player_name} ({pos}): {len(matches)} matches")
    for m in matches:
        print(f" - {m['club_name']} ({m['league']}): urgency={m.get('recruitment_urgency')}, note={m.get('recruitment_note')[:40]}...")

test_matches("Heung-min Son")
test_matches("Erling Haaland")
test_matches("Michael Olise")
