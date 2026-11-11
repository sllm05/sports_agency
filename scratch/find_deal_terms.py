import glob

for p in ['src/sports_agency/api/static/index.html', 'html/index.html', 'javascript/negotiation.js']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if '계약 세부 수치 직접 지정' in c:
        print('Found "계약 세부 수치 직접 지정" in', p)
    if '협상 조건 설정' in c:
        print('Found "협상 조건 설정" in', p)
