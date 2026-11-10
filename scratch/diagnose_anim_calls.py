import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'animationLoop', text):
    idx = m.start()
    print('--- animationLoop occurrence ---')
    print(text[max(0, idx-100):min(len(text), idx+150)])
