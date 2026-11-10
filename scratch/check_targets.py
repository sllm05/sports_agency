import urllib.request
import json

res = urllib.request.urlopen("http://127.0.0.1:8000/api/agency/recruitment-targets")
data = json.loads(res.read())
print(f"Recruitment targets count: {len(data['targets'])}")
for t in data["targets"]:
    print(f"- [{t['target_type']}] {t['name_ko']} ({t['name']}) | Club: {t.get('current_club')} | Category: {t['category']} | Status: {t['scouting_status']}")
