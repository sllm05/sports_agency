with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function filterManagersOnly' in l or 'function applyRosterFilters' in l:
        print(f"--- Line {i+1} ---")
        for j in range(i, min(len(lines), i+30)):
            print(lines[j], end='')
