with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "/api/players" in line and "def " in lines[i+1]:
        for j in range(i, min(i+20, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
