p = r"C:\Users\KIM DONGJUN\.gemini\antigravity\brain\a4f5f1b7-a2ab-4158-8106-0065502786bf\scratch\inject_agency_features.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

checks = ['id="page-portfolio"', 'id="page-recruitment"', 'id="page-admin"', 'modal-pitch-viewer', 'loadAgencyPortfolio', 'loadAgencyRecruitmentTargets']
for c in checks:
    print(c, c in text)
