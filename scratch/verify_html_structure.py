import re

with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('--- NAV BUTTONS ---')
nav_matches = re.findall(r'<button id="nav-btn-[^"]+"[^>]*>.*?</button>', html)
for m in nav_matches:
    print(m)

print('\n--- SCOUTING VIEWS & ELEMENTS ---')
print('scouting-view-recruitment in html:', 'id="scouting-view-recruitment"' in html)
print('scouting-view-watchlist in html:', 'id="scouting-view-watchlist"' in html)
print('scouting-view-all in html:', 'id="scouting-view-all"' in html)
print('page-recruitment in html:', 'id="page-recruitment"' in html)
print('switchScoutingView in html:', 'switchScoutingView' in html)
