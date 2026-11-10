import sys
sys.path.append(".")
from mcp_server.football_mcp_server import list_agency_recruitment_targets

res = list_agency_recruitment_targets()
print("Total targets count:", res.get("total_targets"))
print("Summary:", res.get("summary"))
targets = res.get("targets", [])
print(f"Loaded {len(targets)} targets. First 3:")
for t in targets[:3]:
    print(f"  ID={t.get('target_id')}, Name={t.get('name_ko')}({t.get('name')}), Club={t.get('current_club')}, Category={t.get('category')}, is_virtual={t.get('is_virtual')}, status={t.get('scouting_status')}")
