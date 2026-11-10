import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"

with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

applied = []
failed = []

with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx == 1707: # skip accidental deletion
            continue
        if "index.html" in l and "edit_file" in l:
            try:
                d = json.loads(l)
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "edit_file" and "index.html" in str(args.get("Path", "")):
                        tgt = args.get("Target", "")
                        rep = args.get("Replacement", "")
                        step = d.get("step_index")
                        if tgt and tgt in html:
                            html = html.replace(tgt, rep, 1)
                            applied.append((idx, step))
                        else:
                            failed.append((idx, step, tgt[:60]))
            except Exception as e:
                pass

print(f"Applied: {len(applied)} edits:")
for idx, step in applied:
    print(f"  Line {idx} Step {step}")
print(f"Failed: {len(failed)} edits:")
for idx, step, tgt in failed:
    print(f"  Line {idx} Step {step}: {repr(tgt)}")

print(f"Resulting html len: {len(html)}, lines: {len(html.splitlines())}")
