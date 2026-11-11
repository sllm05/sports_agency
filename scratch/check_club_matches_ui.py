with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[3450:3520]
for i, l in enumerate(lines):
    print(f"{i+3451}: {l}", end='')
