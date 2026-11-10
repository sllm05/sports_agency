with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '5대 리그' in line or 'Premier League' in line or '전체 구단' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
