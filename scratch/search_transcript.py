import json

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_idx, line in enumerate(f):
        data = json.loads(line)
        calls = data.get("tool_calls", [])
        for c in calls:
            fn = c.get("function", {}).get("name", "")
            args = c.get("function", {}).get("arguments", {})
            if "edit_file" in fn or "write_file" in fn:
                path = args.get("Path", "")
                if "index.html" in path:
                    print(f"Step {data.get('step_index')}: {fn} on {path} (line {line_idx})")
