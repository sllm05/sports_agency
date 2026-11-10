with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("if (pageId === 'page-scouting')")
print(text[idx:idx+400])
