with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[3110:3170]
for i, l in enumerate(lines):
    print(f"{i+3111}: {l}", end='')
