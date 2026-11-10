with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'agency/recruitment-targets' in line or 'recruitmentTargets' in line or 'target.name' in line:
        print(f"Line {i+1}: {line.strip()}")
