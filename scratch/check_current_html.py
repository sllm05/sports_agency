import re

with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pages = re.findall(r'id=["\'](page-[^"\']+)["\']', html)
modals = re.findall(r'id=["\'](modal-[^"\']+)["\']', html)
print('Pages:', pages)
print('Modals:', modals)
print('Total lines:', len(html.splitlines()))
