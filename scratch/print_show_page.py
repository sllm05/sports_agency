with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "function showPage(" in line:
        for j in range(i, min(i+35, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
