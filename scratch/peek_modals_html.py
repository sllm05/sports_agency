p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"

with open(p, "r", encoding="utf-8") as f:
    text = f.read()

modals_start = text.find("MODALS_HTML = '''")
modals_end = text.find("JAVASCRIPT_LOGIC = '''")
modals_str = text[modals_start:modals_end]

for line in modals_str.splitlines():
    if 'id="modal-' in line:
        print(line.strip())
