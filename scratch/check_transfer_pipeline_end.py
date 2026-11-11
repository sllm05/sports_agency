with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[3254:3310]
for i, l in enumerate(lines):
    print(f"{i+3255}: {l}", end='')
