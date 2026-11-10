with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find showPage function
start = text.find('function showPage(')
if start != -1:
    print(text[start:start+1200])
