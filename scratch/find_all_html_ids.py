import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

# Find all id="..." in the HTML part (before <script>)
script_idx = text.find('<script>')
html_part = text[:script_idx]

ids = re.findall(r'id=["\']([^"\']+)["\']', html_part)
print("All HTML IDs in fm_2d_grid_match.html:")
for i in ids:
    print(f" - {i}")
