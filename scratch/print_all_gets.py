with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '@app.get(' in l:
        print(f'{i+1}: {l.strip()}')
