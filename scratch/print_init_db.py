with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(1509, 1535):
    print(f"{j+1}: {lines[j]}", end="")
