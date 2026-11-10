with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(176, 342):
    print(f"{i+1}: {lines[i]}", end="")
