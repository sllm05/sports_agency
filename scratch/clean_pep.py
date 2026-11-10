import sys
sys.path.append('.')
from mcp_server.football_mcp_server import terminate_agency_client_contract

res = terminate_agency_client_contract(101, "MANAGER", reason="초기 테스트 정리")
print("Terminated Pep:", res)
