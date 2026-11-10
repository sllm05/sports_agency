import os
from pathlib import Path

def get_dir_size(p):
    total = 0
    for f in p.rglob('*'):
        try:
            if f.is_file():
                total += f.stat().st_size
        except (PermissionError, FileNotFoundError):
            pass
    return total

print("=== 1. DATA DIRECTORY BREAKDOWN ===")
data_path = Path("data")
if data_path.exists():
    data_items = []
    for entry in data_path.iterdir():
        if entry.is_dir():
            s = get_dir_size(entry)
            data_items.append((entry.name, s, "dir"))
        else:
            s = entry.stat().st_size
            data_items.append((entry.name, s, "file"))
    data_items.sort(key=lambda x: x[1], reverse=True)
    for name, s, itype in data_items:
        mb = s / (1024 * 1024)
        if mb > 0.01:
            print(f"  {name:<40} | {itype:<5} | {mb:>8.2f} MB")

print("\n=== 2. .VENV TOP PACKAGES BREAKDOWN ===")
site_packages = Path(".venv/Lib/site-packages")
if site_packages.exists():
    pkg_sizes = []
    for entry in site_packages.iterdir():
        if entry.is_dir():
            s = get_dir_size(entry)
            pkg_sizes.append((entry.name, s))
        else:
            pkg_sizes.append((entry.name, entry.stat().st_size))
    pkg_sizes.sort(key=lambda x: x[1], reverse=True)
    for name, s in pkg_sizes[:15]:
        mb = s / (1024 * 1024)
        print(f"  {name:<40} | {mb:>8.2f} MB")

print("\n=== 3. .GIT DIRECTORY BREAKDOWN ===")
git_path = Path(".git")
if git_path.exists():
    git_items = []
    for entry in git_path.iterdir():
        if entry.is_dir():
            s = get_dir_size(entry)
            git_items.append((entry.name, s, "dir"))
        else:
            git_items.append((entry.name, entry.stat().st_size, "file"))
    git_items.sort(key=lambda x: x[1], reverse=True)
    for name, s, itype in git_items[:10]:
        mb = s / (1024 * 1024)
        print(f"  {name:<40} | {itype:<5} | {mb:>8.2f} MB")
