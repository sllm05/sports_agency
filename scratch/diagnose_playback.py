import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

# Look for play button in HTML
btn_match = re.search(r'<button[^>]*id="btnPlay"[^>]*>.*?</button>', text, re.DOTALL)
if btn_match:
    print("btnPlay HTML:", btn_match.group(0))

# Look for togglePlay or isPlaying
for m in re.finditer(r'function togglePlay\(.*?\)\s*\{.*?\}', text, re.DOTALL):
    print("togglePlay:", m.group(0))

# Look for animLoop or requestAnimationFrame
for m in re.finditer(r'function animLoop\(.*?\)\s*\{.*?\}', text, re.DOTALL):
    print("animLoop:", m.group(0))

# Look for where animLoop is started initially (window.onload, initUI, etc.)
for m in re.finditer(r'requestAnimationFrame\([^\)]+\)', text):
    print("RAF call:", m.group(0))
