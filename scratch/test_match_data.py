from mcp_server.football_mcp_server import find_matching_clubs_for_transfer

matches = find_matching_clubs_for_transfer(
    position="ST",
    max_fee_eur=85000000,
    target_weekly_wage_eur=250000,
    preferred_league="ALL"
)
for m in matches:
    print(f"Club: {m['club_name']}, Starter: {m['current_starter']} ({m['starter_age']}yo), Urgency: {m['recruitment_urgency']}")
