import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function calculate22Positions(')
print(text[idx+4000:idx+5500])
