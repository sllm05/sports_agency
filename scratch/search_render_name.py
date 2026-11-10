with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'renderPlayerGrid' in line or 'p.name_ko' in line or 'displayName' in line:
        print(f"Line {i+1}: {line.strip()}")
