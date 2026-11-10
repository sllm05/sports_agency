import json

with open('data/datasets/managers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total managers in JSON: {len(data)}")
for m in data[:3]:
    print(json.dumps(m, indent=2, ensure_ascii=False)[:400])
