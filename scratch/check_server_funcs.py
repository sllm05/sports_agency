import re

with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'def (?:list_agency_clients|enroll_client_to_agency|get_agency_recruitment_targets)', text):
    start = m.start()
    print(text[start:start+1200])
    print('='*50)
