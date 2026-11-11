with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[4000:4040]
for i, l in enumerate(lines):
    print(f"{i+4001}: {l}", end='')
