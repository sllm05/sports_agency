with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function renderRecruitmentCards(')
if start != -1:
    print(text[start:start+2500])
