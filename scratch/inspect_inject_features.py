p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if line.startswith("# =") or line.strip().startswith("agency_") or line.strip().startswith("def ") or "PORTFOLIO" in line or "RECRUITMENT" in line:
        print(f"{i+1}: {line.strip()[:100]}")
