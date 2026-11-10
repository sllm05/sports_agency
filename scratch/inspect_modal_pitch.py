import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'modal-pitch-viewer', text):
    idx = m.start()
    print('--- MODAL PITCH VIEWER OCCURRENCE ---')
    print(text[max(0, idx-100):min(len(text), idx+400)])
