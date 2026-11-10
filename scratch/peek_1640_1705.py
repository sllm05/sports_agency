import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if 1640 <= idx <= 1705:
            d = json.loads(l)
            step = d.get("step_index")
            tcs = d.get("tool_calls", [])
            for tc in tcs:
                name = tc.get("name") or tc.get("function", {}).get("name")
                args = tc.get("args") or tc.get("function", {}).get("arguments")
                print(f"Line {idx} Step {step} tool={name}:")
                if name == "write_file":
                    print("  Path:", args.get("Path"))
                elif name == "edit_file":
                    print("  Path:", args.get("Path"))
                    print("  Target preview:", repr(args.get("Target", "")[:60]))
                elif name == "run_command":
                    print("  Cmd:", args.get("CommandLine", "")[:80])
