with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[25:55]
for i, l in enumerate(lines):
    print(f"{i+26}: {l}", end='')
