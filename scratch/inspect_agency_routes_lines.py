with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/agency/' in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(i, min(i+15, len(lines))):
            print(f"  {lines[j].strip()}")
        print("-" * 50)
