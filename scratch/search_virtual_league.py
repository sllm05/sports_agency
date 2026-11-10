with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'VIRTUAL_LEAGUE' in line or 'VIRTUAL_LEAGUES' in line or '가상 리그' in line or '가상리그' in line:
        print(f"Line {i+1}: {line.strip()}")
