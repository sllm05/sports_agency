import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function animationLoop\(.*?\)\s*\{.*?\n    \}', text, re.DOTALL)
if m:
    print(m.group(0))
else:
    print("animationLoop not found!")
