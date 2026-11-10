import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    text = f.read()

print("Title:", re.findall(r'<title>(.*?)</title>', text))

# Look for navigation/tab buttons
for m in re.finditer(r'<button[^>]+id="[^"]*tab[^"]*"[^>]*>(.*?)</button>', text, re.IGNORECASE):
    print("Tab button:", m.group(0)[:150])

# Look for tab panels or sections
for m in re.finditer(r'<section[^>]+id="[^"]*"[^>]*>', text, re.IGNORECASE):
    print("Section:", m.group(0)[:150])

for m in re.finditer(r'<div[^>]+id="[^"]*view[^"]*"[^>]*>', text, re.IGNORECASE):
    print("View div:", m.group(0)[:150])
