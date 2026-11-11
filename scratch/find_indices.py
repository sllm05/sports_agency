with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if '<!-- Strategy Parameters Setting Panel -->' in line:
        start_idx = i
    if start_idx is not None and '<!-- PAGE 3: TACTICAL DESK & 2D MATCH ENGINE -->' in line:
        end_idx = i
        break

print(f"start_idx: {start_idx}, end_idx: {end_idx}")
if start_idx and end_idx:
    # check line before end_idx
    print("Lines around end_idx:")
    for j in range(end_idx - 6, end_idx + 2):
        print(f"{j}: {lines[j].strip()}")
