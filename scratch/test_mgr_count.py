import sys
sys.path.append('.')
from mcp_server.football_mcp_server import list_agency_players, list_agency_managers

players = list_agency_players()
managers = list_agency_managers()
print(f"Players count: {len(players)}")
print(f"Managers count: {len(managers)}")
mgr_positions = set(p.get("position") for p in players)
print(f"Positions in players: {mgr_positions}")
