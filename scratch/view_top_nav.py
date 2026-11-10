with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(40, 110):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
