import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if "index.html" in l and ("write_file" in l or "edit_file" in l or "python" in l):
            try:
                d = json.loads(l)
                step = d.get("step_index")
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name in ("write_file", "edit_file") and "index.html" in str(args.get("Path", "")):
                        print(f"Line {idx} Step {step} tool={name}")
                    elif name == "run_command" and "index.html" in str(args.get("CommandLine", "")):
                        cmd = args.get("CommandLine", "")[:100]
                        print(f"Line {idx} Step {step} cmd: {cmd}")
            except Exception as e:
                pass
