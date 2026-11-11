with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'preferred-league-select' in line and i < 2000:
            print(f'{i+1}: {line}')
