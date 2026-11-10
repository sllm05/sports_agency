with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'.{0,50}filterManagersOnly.{0,50}', text)
print("filterManagersOnly matches:", matches)
select_mgr = re.findall(r'.{0,50}selectManager.{0,50}', text)
print("selectManager matches:", select_mgr)
