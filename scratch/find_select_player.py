with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "function selectPlayer" in line:
        print(f"Line {i+1}: {line.strip()}")
        for j in range(i, min(i+25, len(lines))):
            print(f"  {lines[j].strip()}")
