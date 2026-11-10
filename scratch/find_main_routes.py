with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "/api/agency" in line:
        print(f"L{idx}: {line.strip()[:80]}")
