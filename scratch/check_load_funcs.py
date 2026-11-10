with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'function load\w+\([^\)]*\)', text)
print("Load functions:", matches)
