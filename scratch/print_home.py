with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find page-home
start = text.find('id="page-home"')
if start != -1:
    print(text[start:start+2500])
