import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

script_idx = text.find('<script>')
html_part = text[:script_idx]
script_part = text[script_idx:]

get_ids = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", script_part)
print("Unique IDs queried in JS:", set(get_ids))

html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html_part))
print("\nHTML IDs defined:", html_ids)

missing = set(get_ids) - html_ids
print("\nMISSING IDs (Queried in JS but NOT in HTML):", missing)
