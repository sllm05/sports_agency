with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'renderPortfolio' in line or 'portfolio-players-grid' in line or 'loadAgencyPortfolio' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
