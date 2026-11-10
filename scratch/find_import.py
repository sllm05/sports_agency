import sys

with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r"from ([\w\.]+) import.*get_agency_portfolio_overview", text)
print("Import matches:", matches)
