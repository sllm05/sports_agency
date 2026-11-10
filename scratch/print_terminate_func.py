with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def terminate_agency_client_contract' in l or 'SELECT c.*, m.current_club' in l:
        print(f"--- Line {i+1} ---")
        for j in range(max(0, i-2), min(len(lines), i+35)):
            print(lines[j], end='')
