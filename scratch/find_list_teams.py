with open('mcp_server/football_mcp_server.py', encoding='utf-8') as f:
    code = f.read()

import re
m = re.search(r'def list_agency_teams\(.*?\n(?=def |\Z)', code, re.DOTALL)
if m:
    print(m.group(0)[:1500])
