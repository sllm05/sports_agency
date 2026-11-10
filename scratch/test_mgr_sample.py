import sys
sys.path.append('.')
from mcp_server.football_mcp_server import list_agency_players

players = list_agency_players()
mgrs = [p for p in players if p.get("position") == "MGR"]
print(f"Total MGR in players: {len(mgrs)}")
if mgrs:
    print("Sample MGR:", mgrs[0])
