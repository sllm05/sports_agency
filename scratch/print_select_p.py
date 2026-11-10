with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(1814, min(1850, len(lines))):
    print(f"{j+1}: {lines[j]}", end="")
