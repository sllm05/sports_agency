with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<select[^>]*id="([^"]*)"[^>]*>([\s\S]*?)</select>', html)
for sel_id, options in matches:
    if any(k in options for k in ['Premier League', '5대 리그', '전체 구단']):
        print(f"Select ID: '{sel_id}'")
        opts = [o.strip() for o in re.findall(r'<option[^>]*>.*?</option>', options)]
        for o in opts[:10]:
            print(f"  {o}")
        print("---")
