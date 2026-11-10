p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    text = f.read()

rec_js = text[text.find('// PILLAR 2: TALENT & MANAGER RECRUITMENT CONTROLLER'):text.find('// MODAL CLOSE & SUBMIT HANDLERS')]
for line in rec_js.splitlines()[200:260]:
    print(line)
