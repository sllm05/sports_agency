import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'showPage\([^\)]+\)', text):
    print(m.group(0))
