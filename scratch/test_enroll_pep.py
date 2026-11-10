import sys
sys.path.append('.')
from mcp_server.football_mcp_server import enroll_target_as_agency_client, get_agency_portfolio_overview, terminate_agency_client_contract

print("=== Enrolling Pep Guardiola ===")
res = enroll_target_as_agency_client(101, "MANAGER", lead_agent="김대표 수석에이전트", commission_pct=7.0)
print("Enroll result:", res)

pf = get_agency_portfolio_overview()
print("Portfolio managers:", [(m['name'], m['name_ko'], m['current_club'], m['points_per_game']) for m in pf['managers']])

print("=== Terminating for cleanup ===")
res_term = terminate_agency_client_contract(101, "MANAGER", reason="테스트 완료 후 복귀")
print("Terminate result:", res_term)
