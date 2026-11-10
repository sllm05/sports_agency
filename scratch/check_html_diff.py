import subprocess

res = subprocess.run(['git', 'diff', 'src/sports_agency/api/static/index.html'], capture_output=True, text=True, encoding='utf-8')
lines = res.stdout.splitlines()

for i, line in enumerate(lines):
    if line.startswith('-') and not line.startswith('---'):
        if '영입' in line or 'scout' in line or 'recruitment' in line:
            print(f"DEL: {line.strip()[:100]}")
    elif line.startswith('+') and not line.startswith('+++'):
        if '영입' in line or 'scout' in line or 'recruitment' in line:
            print(f"ADD: {line.strip()[:100]}")
