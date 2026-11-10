with open(r'mcp_server\football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def list_agency_players' in line:
        for j in range(i, min(i + 50, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
