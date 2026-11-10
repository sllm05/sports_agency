with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '신규 영입' in line or '신규 고객' in line or 'Recruitment' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
