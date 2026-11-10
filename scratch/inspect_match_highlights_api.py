import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/sports_agency/api/main.py', encoding='utf-8') as f:
    text = f.read()

idx = text.find('def get_tactical_match_highlights')
if idx != -1:
    print(text[idx:idx+1500])
