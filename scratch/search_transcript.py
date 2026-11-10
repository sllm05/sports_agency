import json

with open(r'C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        content = data.get('content', '')
        if '손흥민' in content or 'Son' in content:
            print(f"Step {data.get('step_index')}, Type: {data.get('type')}, Source: {data.get('source')}")
            # print up to 200 chars
            print("   ", content[:200].replace('\n', ' '))
