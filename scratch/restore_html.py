import json

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"

# Read backwards from line 2300 to find the last write_file or full edit of index.html
with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx in range(len(lines)-1, -1, -1):
    line = lines[idx]
    if "index.html" in line and "write_file" in line:
        d = json.loads(line)
        for tc in d.get("tool_calls", []):
            if tc.get("function", {}).get("name") == "write_file" and "index.html" in tc.get("function", {}).get("arguments", {}).get("Path", ""):
                print(f"Found write_file on index.html at line {idx}, step {d.get('step_index')}")
                content = tc["function"]["arguments"]["Content"]
                print(f"Content length: {len(content)}")
                with open("src/sports_agency/api/static/index.html", "w", encoding="utf-8") as out:
                    out.write(content)
                print("Restored index.html from step", d.get('step_index'))
                exit(0)
