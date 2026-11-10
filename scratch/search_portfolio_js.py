with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "portfolio" in line.lower() and ("function" in line or "const " in line or "let " in line or "async " in line):
        print(f"L{idx}: {line.strip()[:80]}")
    elif "page-portfolio" in line:
        print(f"L{idx}: {line.strip()[:80]}")
