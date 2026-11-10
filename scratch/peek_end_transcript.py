import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx >= 2440:
            try:
                d = json.loads(l)
                step = d.get("step_index")
                src = d.get("source")
                typ = d.get("type")
                tcs = d.get("tool_calls", [])
                tc_names = [tc.get("name") or tc.get("function", {}).get("name") for tc in tcs]
                content = (d.get("content") or "")[:100]
                print(f"Line {idx} Step {step} src={src} typ={typ} tools={tc_names} content={repr(content)}")
            except Exception as e:
                pass
