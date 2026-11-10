with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function updateNavState(')
print(text[idx:idx+1200])
