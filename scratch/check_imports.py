with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines[:120], 1):
    if "portfolio" in line.lower() or "enroll" in line.lower() or "agency" in line.lower():
        print(f"L{idx}: {line.strip()}")
