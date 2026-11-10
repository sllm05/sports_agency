p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect page-recruitment HTML
rec_match = text[text.find('<!-- PAGE: RECRUITMENT TARGETS'):text.find('<!-- PAGE: ADMIN CONSOLE')]
print("Recruitment HTML length:", len(rec_match))
print("\n--- FIRST 60 LINES OF RECRUITMENT HTML ---")
for line in rec_match.splitlines()[:60]:
    print(line)
