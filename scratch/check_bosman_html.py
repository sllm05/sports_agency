with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[780:850]
for i, l in enumerate(lines):
    print(f"{i+781}: {l}", end='')
