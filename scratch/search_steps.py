import json

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_idx, line in enumerate(f):
        if "index.html" in line and ("edit_file" in line or "write_file" in line):
            d = json.loads(line)
            print(f"Step {d.get('step_index')}: line_idx={line_idx}")
