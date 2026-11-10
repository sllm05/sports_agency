import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

for var in ['isPlaying', 'lastTime', 'TOTAL_DURATION', 'playbackSpeed', 'currentTime', 'initUI', 'renderPitch']:
    m = re.search(rf'(?:let|const|var|function)\s+{var}\b.*?(?=\n)', text)
    if m:
        print(m.group(0))
