import os
for root, dirs, files in os.walk('.'):
    if 'api_service.py' in files:
        print(os.path.join(root, 'api_service.py'))
