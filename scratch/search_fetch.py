with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/players' in line or 'fetchPlayers' in line or 'loadAllPlayers' in line or 'allPlayers =' in line:
        print(f"Line {i+1}: {line.strip()}")
