import json

transcript_path = r'C:\Users\KIM DONGJUN\.gemini\antigravity\brain\8627e6a2-486b-423b-b476-e68ad2335813\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3550, min(3565, len(lines))):
    d = json.loads(lines[i])
    step = d.get("step_index")
    stype = d.get("type")
    status = d.get("status")
    time = d.get("created_at")
    content = str(d.get("content", ""))[:120]
    error = d.get("error")
    tool_calls = d.get("tool_calls", [])
    tc_names = [tc.get("name") for tc in tool_calls] if tool_calls else []
    print(f"Step {step} [{stype}] ({status}) at {time} | tools: {tc_names} | err: {error} | {content}")
