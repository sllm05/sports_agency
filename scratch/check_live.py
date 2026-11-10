import urllib.request
import json

req = urllib.request.urlopen('http://127.0.0.1:8000/api/agency/recruitment-targets')
data = json.loads(req.read().decode('utf-8'))
print('Server response count:', len(data['targets']))
for t in data['targets']:
    print(f"- [{t['target_type']}] {t['name_ko']} ({t['name']}) | {t['category']} | {t['current_club']}")
