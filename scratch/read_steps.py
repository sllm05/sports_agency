import json

with open(r'C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index')
        if idx in range(3705, 3725):
            print(f"--- Step {idx} ({data.get('type')}) ---")
            print(data.get('content', '')[:500])
