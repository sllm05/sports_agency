with open('src/sports_agency/api/static/index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '네오 뮌헨' in line or '한양 시티' in line or '메트로폴리스' in line:
        print(f"index.html Line {i+1}: {line.strip()[:100]}")
