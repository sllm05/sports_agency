import os

p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"
print("Exists:", os.path.exists(p))
if os.path.exists(p):
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()
    print("Length:", len(text))
    print("Lines:", len(text.splitlines()))
