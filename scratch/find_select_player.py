with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for selectPlayer or similar player dossier functions
import re
matches = [m.start() for m in re.finditer(r'function selectPlayer\(', text)]
for idx in matches:
    print(text[idx:idx+1500])
