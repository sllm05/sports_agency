import re

with open('src/sports_agency/api/main.py', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'@app\.get\([^\)]+\)\s+def\s+(\w+)', text):
    print(m.group(0))

for m in re.finditer(r'app\.mount\([^\)]+\)', text):
    print(m.group(0))
