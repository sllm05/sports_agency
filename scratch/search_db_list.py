with open(r'src\sports_agency\database.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def list_agency_players' in line:
        for j in range(i, min(i + 60, len(lines))):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
