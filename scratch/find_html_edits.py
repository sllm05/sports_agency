import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if "index.html" in l and "edit_file" in l:
            try:
                d = json.loads(l)
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "edit_file" and "index.html" in str(args.get("Path", "")):
                        tgt = args.get("Target", "")[:50]
                        rep_len = len(args.get("Replacement", ""))
                        step = d.get("step_index")
                        print(f"Line {idx} Step {step}: tgt={repr(tgt)} rep_len={rep_len}")
            except Exception as e:
                pass
