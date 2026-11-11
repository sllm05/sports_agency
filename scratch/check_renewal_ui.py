with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[8365:8465]
for i, l in enumerate(lines):
    print(f"{i+8366}: {l}", end='')
