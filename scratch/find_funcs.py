import re

with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    text = f.read()

funcs = re.findall(r'def ([a-zA-Z0-9_]+)\(', text)
for fn in funcs:
    if any(k in fn for k in ['portfolio', 'client', 'recruitment', 'target', 'manager']):
        print(fn)
