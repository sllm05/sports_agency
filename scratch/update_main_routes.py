from pathlib import Path

file_path = Path("src/sports_agency/api/main.py")
content = file_path.read_text(encoding="utf-8")

target1 = """if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")"""

replacement1 = """if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

REA_DIR = PROJECT_ROOT / "rea"
if REA_DIR.exists():
    app.mount("/rea", StaticFiles(directory=str(REA_DIR)), name="rea")"""

target2 = """@app.get("/", response_class=HTMLResponse)
def serve_dashboard() -> HTMLResponse:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Dashboard index.html not found</h1>", status_code=404)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))"""

replacement2 = """@app.get("/", response_class=HTMLResponse)
def serve_dashboard() -> HTMLResponse:
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>Dashboard index.html not found</h1>", status_code=404)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.get("/tactics", response_class=HTMLResponse)
@app.get("/fm", response_class=HTMLResponse)
@app.get("/fm-match", response_class=HTMLResponse)
def serve_tactics_engine() -> HTMLResponse:
    tactics_file = PROJECT_ROOT / "rea" / "fm_2d_grid_match.html"
    if not tactics_file.exists():
        return HTMLResponse("<h1>Tactics 2D Grid Engine file not found</h1>", status_code=404)
    return HTMLResponse(tactics_file.read_text(encoding="utf-8"))"""

assert target1 in content, "target1 not found"
assert target2 in content, "target2 not found"

content = content.replace(target1, replacement1, 1)
content = content.replace(target2, replacement2, 1)

file_path.write_text(content, encoding="utf-8")
print("Updated main.py with /tactics routes and /rea mount successfully!")
