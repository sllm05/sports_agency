import json

transcript_path = r'C:\Users\KIM DONGJUN\.gemini\antigravity\brain\8627e6a2-486b-423b-b476-e68ad2335813\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in transcript:', len(lines))
for i in range(max(0, len(lines)-25), len(lines)):
    d = json.loads(lines[i])
    step = d.get("step_index")
    stype = d.get("type")
    status = d.get("status")
    time = d.get("created_at")
    content = str(d.get("content", ""))[:120]
    tool_calls = d.get("tool_calls", [])
    tc_names = [tc.get("name") for tc in tool_calls] if tool_calls else []
    print(f"Step {step} [{stype}] ({status}) at {time} | tools: {tc_names} | content: {content}")
