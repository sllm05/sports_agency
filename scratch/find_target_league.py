with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '희망 타깃 리그' in line:
            print(f'{i+1}: {line.strip()[:100]}')
