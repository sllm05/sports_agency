import re
import subprocess
from pathlib import Path

html = Path("rea/fm_2d_grid_match.html").read_text(encoding="utf-8")
matches = re.findall(r"<script>([\s\S]*?)</script>", html)
print(f"Extracted {len(matches)} script tag(s).")

js_code = "\n".join(matches)
temp_js = Path("scratch/temp_check.js")
temp_js.write_text(js_code, encoding="utf-8")

# Run node --check
res = subprocess.run(["node", "--check", str(temp_js)], capture_output=True, text=True)
print("Node --check returncode:", res.returncode)
if res.stdout:
    print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
