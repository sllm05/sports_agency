import re

with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

print("page-recruitment:", "id=\"page-recruitment\"" in text)
print("page-scouting:", "id=\"page-scouting\"" in text)
print("nav-btn-recruitment:", "id=\"nav-btn-recruitment\"" in text)
print("nav-btn-scouting:", "id=\"nav-btn-scouting\"" in text)

# find line numbers of nav-btn and pages
lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "nav-btn-scouting" in line or "nav-btn-recruitment" in line or "id=\"page-scouting\"" in line or "id=\"page-recruitment\"" in line:
        print(f"L{idx}: {line.strip()[:80]}")
