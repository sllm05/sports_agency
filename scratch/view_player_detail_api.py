with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/api/players/{' in l or 'def api_get_player_detail' in l:
        print(f"--- Line {i+1} ---")
        for j in range(i, min(len(lines), i+30)):
            print(lines[j], end='')
        break
