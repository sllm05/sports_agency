import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if 2350 <= idx <= 2445:
            try:
                d = json.loads(l)
                step = d.get("step_index")
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "run_command":
                        cmd = args.get("CommandLine", "")
                        if "git" in cmd or "index.html" in cmd:
                            print(f"Line {idx} Step {step} run_command: {cmd}")
            except Exception as e:
                pass
