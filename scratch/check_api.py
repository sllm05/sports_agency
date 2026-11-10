from pathlib import Path
import re

text = Path('src/sports_agency/api/main.py').read_text(encoding='utf-8')
m = re.search(r'@app\.get\("/api/players"\)(.*?)def [^\n]+\n(.*?)(?=\n@app|\Z)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
else:
    print("Not found with exact pattern")
    for line in text.splitlines():
        if "/api/players" in line:
            print(line)
