with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '@app.get("/")' in line or "index.html" in line:
        for j in range(max(0, i-2), min(i+15, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
