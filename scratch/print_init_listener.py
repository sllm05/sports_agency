with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "window.addEventListener('DOMContentLoaded'" in line:
        for j in range(max(0, i-5), min(i+10, len(lines))):
            print(f"{j+1}: {lines[j]}", end="")
