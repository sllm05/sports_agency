import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx >= 1700 and "index.html" in l and "edit_file" in l:
            try:
                d = json.loads(l)
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "edit_file" and "index.html" in str(args.get("Path", "")):
                        tgt = args.get("Target", "")
                        rep = args.get("Replacement", "")
                        step = d.get("step_index")
                        print(f"=== Line {idx} Step {step} ===")
                        print("TARGET PREVIEW:\n", tgt[:120])
                        print("REPLACEMENT PREVIEW:\n", rep[:200])
                        print("-" * 50)
            except Exception as e:
                pass
