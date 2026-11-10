with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '@app.get("/")' in l or '@app.get("")' in l or 'FileResponse(STATIC_DIR' in l:
        print(f'{i+1}: {l.strip()}')
        for j in range(i+1, min(i+10, len(lines))):
            print(f'  {j+1}: {lines[j].strip()}')
