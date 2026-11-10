import os
from pathlib import Path

modules = {}
for p in Path('.').rglob('*.py'):
    if '.venv' in p.parts or 'scratch' in p.parts:
        continue
    rel = str(p)
    lines = len(p.read_text(encoding='utf-8', errors='ignore').splitlines())
    sz = p.stat().st_size / 1024
    modules[rel] = (lines, sz)

for k, (lines, sz) in sorted(modules.items()):
    print(f"{k:<50} | {lines:>5} lines | {sz:>6.1f} KB")
