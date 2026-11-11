with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'incumbentCurve', text)]
for idx in matches:
    print(text[idx-100:idx+200])
    print("="*60)
