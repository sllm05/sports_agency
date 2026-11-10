with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def generate_client_recruitment_pitch_deck' in l:
        for j in range(i, min(len(lines), i+80)):
            print(lines[j], end='')
        break
