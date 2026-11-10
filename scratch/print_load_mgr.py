with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "/api/managers" in line:
        for j in range(max(0, i-5), min(i+25, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
