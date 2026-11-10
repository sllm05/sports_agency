with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
routes = re.findall(r'@app\.(post|get)\(["\'](/api/[^"\']+)["\']', text)
for m, r in routes:
    print(f"{m.upper():4} {r}")
