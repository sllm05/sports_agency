with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "renderPortfolioClients" in line or "loadPortfolio" in line or "terminateContract" in line:
        print(f"L{idx}: {line.strip()[:80]}")
