with open(r'src\sports_agency\api\static\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '${p.name' in line or '${p.name_ko' in line or '${client.name' in line or '${player.name' in line or '${target.name' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
