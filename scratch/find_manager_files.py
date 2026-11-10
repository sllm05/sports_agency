import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if 'manager' in f.lower() or 'seed' in f.lower():
            print(os.path.join(root, f))
