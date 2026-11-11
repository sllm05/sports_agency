with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

for line in text.splitlines():
    if 'simulate_client_club_renewal_pipeline' in line:
        print(line)
