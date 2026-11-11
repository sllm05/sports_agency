with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'def simulate_client_club_renewal_pipeline' in line:
        for j in range(i, min(len(lines), i+80)):
            print(f"{j+1}: {lines[j]}", end='')
        break
