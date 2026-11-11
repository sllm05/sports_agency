import sys
sys.path.insert(0, 'src')
from sports_agency.graph.agency_workflow import WORKFLOW_MANAGER
import json

try:
    res = WORKFLOW_MANAGER.start_session(
        thread_id="test_deal_1",
        player_name="Lautaro Martinez",
        track_mode="TRACK_A_TRANSFER",
        target_wage_increase_pct=30,
        priority_goal="5대 리그 즉시 주전 도약 + 적정 주급",
        preferred_league="ALL",
        auto_complete=False,
    )
    print("Workflow success! Keys in result['state']:", list(res['state'].keys()))
    print("matched_clubs:", res['state'].get('matched_clubs'))
except Exception as e:
    import traceback
    print("Workflow error:", e)
    traceback.print_exc()
