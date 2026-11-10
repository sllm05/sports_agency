import os

for root, dirs, files in os.walk('.'):
    if '.venv' in root or '.git' in root or '__pycache__' in root:
        continue
    for f in files:
        if f.endswith('.py') or f.endswith('.sql') or f.endswith('.json'):
            path = os.path.join(root, f)
            try:
                with open(path, encoding='utf-8') as fl:
                    content = fl.read()
                    if '네오 뮌헨' in content or '메트로폴리스' in content or '한양 시티' in content:
                        print(f"Found in {path}")
            except Exception:
                pass
