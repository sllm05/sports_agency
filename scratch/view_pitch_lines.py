with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1930, 2030):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
