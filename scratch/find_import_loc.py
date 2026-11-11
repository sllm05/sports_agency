with open('src/sports_agency/api/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:60]
for i, l in enumerate(lines):
    if 'simulate_client_club_renewal_pipeline' in l:
        print(f"{i+1}: {l}")
        for k in range(max(0, i-5), min(len(lines), i+5)):
            print(f"  {k+1}: {lines[k]}", end='')
