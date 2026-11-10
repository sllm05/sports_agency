import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx in (1707, 1709):
            d = json.loads(l)
            print(f"=== Line {idx} Step {d.get('step_index')} ===")
            for tc in d.get("tool_calls", []):
                print(tc.get("name") or tc.get("function", {}).get("name"))
                args = tc.get("args") or tc.get("function", {}).get("arguments")
                print("Target:\n", repr(args.get("Target")))
                print("Replacement:\n", repr(args.get("Replacement")[:100]))
