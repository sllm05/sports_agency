import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="pitchCanvasTactics"')
if idx != -1:
    print(text[max(0, idx-3500):max(0, idx-1000)])
