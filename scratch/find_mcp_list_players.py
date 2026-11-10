with open('mcp_server/football_mcp_server.py', encoding='utf-8') as f:
    code = f.read()

import re
pattern = r'def list_agency_players\(.*?\n(?=def |\Z)'
m = re.search(pattern, code, re.DOTALL)
if m:
    print(m.group(0)[:1500])
