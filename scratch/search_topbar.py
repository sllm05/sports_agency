with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '선택:' in line or 'selected-client' in line or 'top-nav-client' in line:
        print(f"Line {i+1}: {line.strip()}")
