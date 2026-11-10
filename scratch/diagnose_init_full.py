import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function init()')
print(text[idx:idx+1500])
