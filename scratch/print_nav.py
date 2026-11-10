with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:150]):
    if 'nav' in line.lower() or 'btn' in line.lower() or '대시보드' in line or '소속' in line:
        print(f"{i+1}: {line.strip()}")
