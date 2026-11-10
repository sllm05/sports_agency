import json

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "edit_file" in line and "index.html" in line:
            d = json.loads(line)
            print(f"Keys in d: {list(d.keys())}")
            print(f"tool_calls: {d.get('tool_calls')}")
            break
