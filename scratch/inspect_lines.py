with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for target_line in [905, 1591, 1779, 2063]:
    start = max(0, target_line - 4)
    end = min(len(lines), target_line + 4)
    print(f"=== Around line {target_line} ===")
    for i in range(start, end):
        print(f"L{i+1}: {lines[i].strip()[:70]}")
