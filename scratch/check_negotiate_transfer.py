with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def negotiate_client_club_transfer' in line:
        for j in range(i, min(len(lines), i+50)):
            print(f"{j+1}: {lines[j]}", end='')
        break
