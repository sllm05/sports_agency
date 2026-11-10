import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if "index.html" in l and "write_file" in l:
            try:
                d = json.loads(l)
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "write_file" and "index.html" in str(args.get("Path", "")):
                        step = d.get("step_index")
                        content_len = len(args.get("Content", ""))
                        print(f"Line {idx} Step {step}: write_file index.html len={content_len}")
            except Exception as e:
                pass
