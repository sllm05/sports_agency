with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = [
    'enroll_client', 'terminate_contract', 'client_renew', 'client_transfer', 'client_sign_club',
    'toggle_watchlist', 'check_watchlist'
]

for func in funcs:
    m = re.search(rf'def {func}\([^\)]*\):.*?(?=\n@|\ndef |\Z)', text, re.DOTALL)
    if m:
        print(f"=== {func} ===")
        print(m.group(0)[:500])
        print()
