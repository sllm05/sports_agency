with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "이 선수로 협상 전략" in line or "page-strategy" in line:
        print(f"{i+1}: {line.strip()[:100]}")
