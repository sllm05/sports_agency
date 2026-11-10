with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    if 'index.html' in l or 'get(' in l or 'static' in l or 'FileResponse' in l or 'mount' in l:
        print(f'{i+1}: {l.strip()}')
