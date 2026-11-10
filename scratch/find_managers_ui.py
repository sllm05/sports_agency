with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'MGR' in line or '감독' in line:
        if any(term in line for term in ['filter', 'populate', 'select', 'manager', 'api']):
            print(f"Line {i+1}: {line.strip()[:100]}")
