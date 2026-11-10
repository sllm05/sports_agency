import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"

with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    code = f.read()

with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if "main.py" in l and "edit_file" in l and idx < 2670:
            try:
                d = json.loads(l)
                for tc in d.get("tool_calls", []):
                    name = tc.get("name") or tc.get("function", {}).get("name")
                    args = tc.get("args") or tc.get("function", {}).get("arguments")
                    if name == "edit_file" and "main.py" in str(args.get("Path", "")):
                        tgt = args.get("Target", "")
                        rep = args.get("Replacement", "")
                        if tgt in code:
                            code = code.replace(tgt, rep, 1)
                            print(f"Applied edit at line {idx}")
                        else:
                            print(f"Failed edit at line {idx}: {repr(tgt[:40])}")
            except Exception as e:
                pass

with open("src/sports_agency/api/main.py", "w", encoding="utf-8") as f:
    f.write(code)

print("main.py updated. Length:", len(code))
