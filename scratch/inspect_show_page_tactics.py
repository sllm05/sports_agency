import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function showPage(')
if idx != -1:
    print(text[idx+800:idx+2000])
