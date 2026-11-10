with open(r'src\sports_agency\api\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/players' in line or 'def get_players' in line or 'list_agency_players' in line:
        print(f"Line {i+1}: {line.strip()}")
