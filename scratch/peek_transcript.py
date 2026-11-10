import json

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx in range(5):
        line = f.readline()
        if not line: break
        d = json.loads(line)
        print(f"Line {idx}: step={d.get('step_index')}, type={d.get('type')}, keys={list(d.keys())}")
