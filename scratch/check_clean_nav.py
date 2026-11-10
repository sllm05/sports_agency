with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

print("nav-btn-recruitment:", "nav-btn-recruitment" in text)
print("page-recruitment:", "page-recruitment" in text)
print("page-scouting:", "page-scouting" in text)

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "nav-btn-" in line:
        print(f"L{idx}: {line.strip()[:80]}")
