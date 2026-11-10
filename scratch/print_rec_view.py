with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="scouting-view-recruitment"')
print(text[idx:idx+2500])
