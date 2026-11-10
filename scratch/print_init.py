with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'addEventListener\(["\']DOMContentLoaded["\'].*?(?=\n\s*\n\s*//|\n\s*function|\Z)', text, re.DOTALL)
for m in matches:
    print(m[:1000])

if not matches:
    idx = text.rfind('DOMContentLoaded')
    if idx != -1:
        print(text[idx-100:idx+800])
