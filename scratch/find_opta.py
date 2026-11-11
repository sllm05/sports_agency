import os

for root, dirs, files in os.walk('.'):
    if '.venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.py')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    c = f.read()
                if 'Opta / FBref' in c:
                    print(f'Found "Opta / FBref" in {path}')
            except Exception:
                pass
