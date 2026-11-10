import json

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for idx, l in enumerate(f):
        if idx == 1697:
            d = json.loads(l)
            for tc in d.get("tool_calls", []):
                print(tc.get("args", {}).get("CommandLine"))
