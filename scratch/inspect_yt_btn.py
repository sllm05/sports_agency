import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="ytSyncBtn"')
print(text[max(0, idx-200):min(len(text), idx+300)])
