import os

target_files = [
    'src/sports_agency/api/static/index.html',
    'html/index.html',
    'javascript/scouting.js',
    'javascript/negotiation.js',
    'javascript/app.js'
]

for tf in target_files:
    if os.path.exists(tf):
        with open(tf, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"=== {tf} ===")
        for i, line in enumerate(lines):
            if '.slice(' in line:
                print(f"Line {i+1}: {line.strip()[:100]}")
