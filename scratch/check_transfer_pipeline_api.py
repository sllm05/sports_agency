with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'/client/transfer-pipeline', text)]
for idx in matches:
    print(text[idx-50:idx+600])
    print("="*60)
