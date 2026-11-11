import os, re

files_to_check = [
    'src/sports_agency/api/static/index.html',
    'src/sports_agency/api/main.py',
    'mcp_server/football_mcp_server.py',
    'src/sports_agency/tactics_engine.py',
]

for fpath in files_to_check:
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    if '30.2' in text:
        print(f"Found '30.2' in {fpath}!")
        for m in re.finditer(r'.{0,50}30\.2.{0,50}', text):
            print("  ->", m.group(0).strip())
