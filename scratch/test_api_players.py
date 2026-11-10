import urllib.request
import json

req = urllib.request.urlopen('http://127.0.0.1:8000/api/players')
data = json.loads(req.read().decode('utf-8'))

players = data.get('all_players', [])
print("Total all_players count:", len(players))

pl_clubs = set()
for p in players:
    if p.get('league') == 'Premier League':
        pl_clubs.add(p.get('current_club'))

print(f"Premier League clubs count: {len(pl_clubs)}")
for c in sorted(pl_clubs):
    print(" -", c)

haaland_list = [p for p in players if 'haaland' in p.get('name', '').lower() or '홀란드' in (p.get('name_ko') or '')]
print("Haaland in players:", len(haaland_list))
for h in haaland_list:
    print("   ", h['player_id'], h['name'], h.get('name_ko'), h.get('current_club'), h.get('league'), h.get('is_agency_client'))

son_list = [p for p in players if 'heung-min' in p.get('name', '').lower() or '손흥민' in (p.get('name_ko') or '')]
print("Son in players:", len(son_list))
for s in son_list:
    print("   ", s['player_id'], s['name'], s.get('name_ko'), s.get('current_club'), s.get('league'), s.get('is_agency_client'))
