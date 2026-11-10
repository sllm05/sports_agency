import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx in (1710, 1715, 1720, 1725, 1730, 1735):
            d = json.loads(l)
            for tc in d.get("tool_calls", []):
                name = tc.get("name") or tc.get("function", {}).get("name")
                args = tc.get("args") or tc.get("function", {}).get("arguments")
                print(f"Line {idx} Step {d.get('step_index')} tool={name}:")
                if "Target" in args:
                    print("  Target:", repr(args.get("Target")[:80]))
                if "Path" in args:
                    print("  Path:", args.get("Path"))
