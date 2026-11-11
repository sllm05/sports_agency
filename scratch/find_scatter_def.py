with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function updateScoutingScatterChart' in line:
        for j in range(i, min(len(lines), i+120)):
            print(f"{j+1}: {lines[j]}", end='')
        break
