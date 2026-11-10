with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

scout_view = text[text.find('id="page-scouting"'):text.find('id="page-strategy"')]
for line in scout_view.splitlines():
    if "manager" in line.lower() or "감독" in line:
        print(line.strip()[:100])
