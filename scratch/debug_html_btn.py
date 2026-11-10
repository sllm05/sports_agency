import httpx
r = httpx.get("http://127.0.0.1:8000/")
print("Length:", len(r.text))
print("Has 'btn-scouting-watchlist'?", 'btn-scouting-watchlist' in r.text)
print("Has 'id=\"btn-scouting-watchlist\"'?", 'id="btn-scouting-watchlist"' in r.text)

# Let's see what button id is in r.text
for line in r.text.splitlines():
    if "scouting-watchlist" in line:
        print("Line:", line.strip())
