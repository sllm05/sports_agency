import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

ids_checked = [
    'hudActionText', 'hudMetricText', 'timeLabel', 'timeSlider',
    'btnPlayPause', 'playerSelect', 'pAvatar', 'pNameKo', 'pClub',
    'pPosBadge', 'pArchetype', 'pMarketVal', 'pStatXg', 'pStatKp',
    'pStatProg', 'pStatDef', 'pStatPctl', 'btnYtHighlight', 'actionList'
]

for el_id in ids_checked:
    exists = f'id="{el_id}"' in text or f"id='{el_id}'" in text
    print(f'id="{el_id}": {exists}')
