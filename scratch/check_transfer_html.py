with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[10460:10560]
for i, l in enumerate(lines):
    print(f"{i+10461}: {l}", end='')
