with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[8480:8580]
for i, l in enumerate(lines):
    print(f"{i+8481}: {l}", end='')
