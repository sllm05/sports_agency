import os
from pathlib import Path

root = Path('.')
total_size = 0
items = []

for entry in sorted(root.iterdir()):
    try:
        if entry.is_dir():
            dir_size = 0
            for f in entry.rglob('*'):
                try:
                    if f.is_file():
                        dir_size += f.stat().st_size
                except (PermissionError, FileNotFoundError):
                    pass
            items.append((entry.name, dir_size, 'dir'))
        elif entry.is_file():
            items.append((entry.name, entry.stat().st_size, 'file'))
    except (PermissionError, FileNotFoundError):
        pass

items.sort(key=lambda x: x[1], reverse=True)
total_bytes = sum(x[1] for x in items)

print(f"Total project size: {total_bytes / (1024*1024):.2f} MB\n")
print(f"{'Name':<35} | {'Type':<6} | {'Size (MB)':<10} | {'Percentage':<8}")
print("-" * 70)
for name, size, itype in items:
    mb = size / (1024*1024)
    pct = (size / total_bytes) * 100 if total_bytes > 0 else 0
    if mb > 0.05:
        print(f"{name:<35} | {itype:<6} | {mb:>9.2f} MB | {pct:>7.1f}%")
