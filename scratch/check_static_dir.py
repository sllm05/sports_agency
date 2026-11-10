with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(min(50, len(lines))):
    if "STATIC_DIR" in lines[i]:
        print(f"{i+1}: {lines[i]}", end="")
