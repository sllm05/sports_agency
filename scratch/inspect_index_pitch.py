import re

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'(?:<canvas|id="pitch|2D Tactical|class="[^"]*pitch[^"]*")', text, re.IGNORECASE):
    idx = m.start()
    print('--- MATCH ---')
    print(text[max(0, idx-100):min(len(text), idx+300)])
