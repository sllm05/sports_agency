with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '전체 구단' in line or 'club-filter-select' in line or 'populateClubFilter' in line or 'updateClubFilter' in line:
        print(f"Line {i+1}: {line.strip()}")
