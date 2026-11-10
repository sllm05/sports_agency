with open('src/sports_agency/api/main.py', encoding='utf-8') as f:
    code = f.read()

import re
pattern = r'@app\.get\("/api/players".*?\n(?=@app|\Z)'
m = re.search(pattern, code, re.DOTALL)
if m:
    print(m.group(0)[:1500])
else:
    print("Not found by regex")
