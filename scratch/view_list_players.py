with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def list_agency_players' in l:
        print(f"--- Line {i+1} ---")
        for j in range(i, min(len(lines), i+30)):
            print(lines[j], end='')
        break
