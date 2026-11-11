with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[3265:3285]
for i, l in enumerate(lines):
    print(f"{i+3266}: {l}", end='')
