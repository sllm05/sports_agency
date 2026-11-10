p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(10, 95):
    print(f"{i+1}: {lines[i]}", end="")
