with open("src/sports_agency/api/agency_routes.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "@agency_bp" in line:
        print(f"L{idx}: {line.strip()[:80]}")
