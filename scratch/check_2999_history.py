import json

with open(r'C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        content = data.get('content', '')
        if '2999' in content:
            print(f"Step {data.get('step_index')}, Type: {data.get('type')}")
            print(content[:300].replace('\n', ' '))
