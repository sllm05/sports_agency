with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
routes = re.findall(r'@app\.(?:get|post|delete|put)\([^\)]+\)', text)
for r in routes:
    if 'agency' in r or 'recruitment' in r or 'watchlist' in r or 'portfolio' in r:
        print(r)
