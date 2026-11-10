with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async function initDashboard(')
if idx == -1:
    idx = text.find('function initDashboard(')
if idx != -1:
    print(text[idx:idx+1500])
