with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Progressive Actions' in line or 'DataMB 5대 리그 동 포지션 백분위' in line:
            print(f'{i+1}: {line.strip()[:100]}')
