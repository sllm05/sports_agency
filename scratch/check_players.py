import json, re, sys

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'const PLAYERS_DATABASE = (\[.*?\]);', text)
if match:
    data = json.loads(match.group(1))
    print(f"Total players in PLAYERS_DATABASE: {len(data)}")
    names = [p.get('name', '') for p in data]
    print(f"Names (sample 10): {names[:10]}")
    son = [p for p in data if 'Son' in p.get('name', '') or '손' in p.get('name_ko', '')]
    print(f"Son in DB: {son}")
    haaland = [p for p in data if 'Haaland' in p.get('name', '')]
    print(f"Haaland in DB: {haaland}")
    minjae = [p for p in data if 'Min' in p.get('name', '') or '김민재' in p.get('name_ko', '')]
    print(f"Minjae in DB: {minjae}")
    kangin = [p for p in data if 'Kang' in p.get('name', '') or '이강인' in p.get('name_ko', '')]
    print(f"Kangin in DB: {kangin}")
