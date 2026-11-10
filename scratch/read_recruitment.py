p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, l in enumerate(lines):
    if 'id="page-recruitment"' in l:
        print("".join(lines[idx:idx+60]))
        break
