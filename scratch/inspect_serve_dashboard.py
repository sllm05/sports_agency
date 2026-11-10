with open('src/sports_agency/api/main.py', encoding='utf-8') as f:
    text = f.read()

idx = text.find('def serve_dashboard')
if idx != -1:
    print(text[idx-50:idx+800])
