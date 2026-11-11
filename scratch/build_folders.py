import os
import shutil
from pathlib import Path

ROOT = Path("c:/AI-Native-Agent/sports_agency")

# Folders to create
folders = ["html", "css", "javascript", "py", "agent"]
for f in folders:
    (ROOT / f).mkdir(parents=True, exist_ok=True)

print("Created directories: html, css, javascript, py, agent")
