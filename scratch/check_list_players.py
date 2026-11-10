from pathlib import Path
import re

text = Path('mcp_server/football_mcp_server.py').read_text(encoding='utf-8')
m = re.search(r'def list_agency_players\([^)]*\):.*?(?=\ndef |\Z)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
