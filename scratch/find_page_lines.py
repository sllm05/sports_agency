with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="page-' in l:
        print(f"{i+1}: {l.strip()[:80]}")
