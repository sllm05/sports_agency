with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async function loadAgencyRecruitmentTargets(')
print(text[idx+1400:idx+2500])
