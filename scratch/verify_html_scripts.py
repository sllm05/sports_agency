import re
import subprocess

with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract script content
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} inline script blocks.")

for i, s in enumerate(scripts):
    with open(f"scratch/extracted_script_{i}.js", "w", encoding="utf-8") as f:
        f.write(s)
    res = subprocess.run(["node", "-c", f"scratch/extracted_script_{i}.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Script {i} ({len(s.splitlines())} lines): SYNTAX OK")
    else:
        print(f"Script {i}: ERROR!\n{res.stderr}")
