import json
import os

transcript_path = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total transcript lines: {len(lines)}")

# We will read each line, find tool_calls with edit_file on index.html, and apply them sequentially!
with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    current_html = f.read()

initial_len = len(current_html)
print(f"Initial index.html len: {initial_len}")

success_count = 0
fail_count = 0

for idx, line in enumerate(lines):
    if "index.html" not in line or "edit_file" not in line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue

    for tc in d.get("tool_calls", []):
        fn = tc.get("function", {})
        if fn.get("name") == "edit_file":
            args = fn.get("arguments", {})
            if "index.html" in args.get("Path", ""):
                target = args.get("Target", "")
                replacement = args.get("Replacement", "")
                step = d.get("step_index")
                if target in current_html:
                    current_html = current_html.replace(target, replacement)
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"Failed at step {step}, target preview: {repr(target[:40])}")

print(f"Replay complete: {success_count} applied, {fail_count} failed. Final len: {len(current_html)}, lines: {len(current_html.splitlines())}")

with open("src/sports_agency/api/static/index.html", "w", encoding="utf-8") as f:
    f.write(current_html)
