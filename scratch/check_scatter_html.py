with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[740:770]
for i, l in enumerate(lines):
    print(f"{i+741}: {l}", end='')
