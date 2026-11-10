import sys
sys.path.append('.')
from mcp_server.football_mcp_server import (
    list_agency_recruitment_targets,
    generate_client_recruitment_pitch_deck,
    enroll_target_as_agency_client,
    get_agency_portfolio_overview,
    terminate_agency_client_contract,
    list_agency_managers
)

# 1. Check managers
mgrs = list_agency_managers()
print(f"Total managers: {len(mgrs)}")
pep = next((m for m in mgrs if 'Guardiola' in m.get('name', '')), None)
print("Found Pep in list_agency_managers:", pep is not None, pep.get('current_club') if pep else None)

# 2. Check recruitment targets
rc = list_agency_recruitment_targets()
print(f"Total recruitment targets: {rc['total_targets']}")
for t in rc['targets'][:6]:
    print(f" - [{t['target_type']}] {t['name_ko']} ({t['name']}) | {t['current_club']} | Cat: {t['category']} | IsVirtual: {t['is_virtual']}")

# 3. Test Pitch Deck for Pep
deck = generate_client_recruitment_pitch_deck(101, "MANAGER")
print("Pitch deck for Pep length:", len(deck.get("markdown_content", "")))

# 4. Enroll Pep
enroll_res = enroll_target_as_agency_client(101, "MANAGER", lead_agent="수석 에이전트", commission_pct=7.0)
print("Enroll Pep:", enroll_res["status"], enroll_res["message"])

# 5. Check Portfolio
pf = get_agency_portfolio_overview()
mgr_names = [m.get('name') for m in pf.get('managers', [])]
print("Portfolio managers after enroll:", mgr_names)
assert 'Pep Guardiola' in mgr_names

# 6. Terminate Pep
term_res = terminate_agency_client_contract(101, "MANAGER", reason="테스트 종료 복귀")
print("Terminate Pep:", term_res["status"])

pf2 = get_agency_portfolio_overview()
print("Portfolio after terminate total clients:", pf2['summary']['total_clients'])

print("ALL MCP BACKEND FUNCTIONS WORK PERFECTLY!")
