with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="page-home"')
print(text[start+1200:start+3500])
