with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[260:290]
for i, l in enumerate(lines):
    print(f"{i+261}: {l}", end='')
