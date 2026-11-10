with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if "page-recruitment" in line or "recruitment-cards-grid" in line:
        print(f"L{idx}: {line.strip()[:80]}")
