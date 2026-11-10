with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(340, 440):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
