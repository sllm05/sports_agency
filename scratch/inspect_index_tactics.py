import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

start_marker = "2D Tactical Grid Match Engine"
idx = text.find(start_marker)
if idx != -1:
    print(text[idx:idx+4000])
