with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['def list_agency_recruitment_targets', 'def get_agency_portfolio_overview', 'def enroll_target_as_agency_client']):
        print(f"--- Line {i+1} ---")
        for j in range(i, min(len(lines), i+60)):
            print(lines[j], end='')
