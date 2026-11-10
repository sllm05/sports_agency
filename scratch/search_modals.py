p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    text = f.read()

for line in text.splitlines():
    if "modal-client" in line or "openClientRenewalModal" in line or "renew" in line.lower() and "def " not in line:
        print(line[:100])
