with open('mcp_server/football_mcp_server.py', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['네오 뮌헨', '메트로폴리스', '한양 시티']):
        print(f"football_mcp_server.py:{i+1} {line.strip()}")

with open('src/sports_agency/api/main.py', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line for k in ['네오 뮌헨', '메트로폴리스', '한양 시티']):
        print(f"main.py:{i+1} {line.strip()}")
