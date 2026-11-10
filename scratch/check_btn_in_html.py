with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

print("In file: 'btn-scouting-watchlist' in text?", 'btn-scouting-watchlist' in text)
import httpx
r = httpx.get("http://127.0.0.1:8000/")
print("In server response: 'btn-scouting-watchlist' in r.text?", 'btn-scouting-watchlist' in r.text)
if 'btn-scouting-watchlist' not in text:
    for line in text.splitlines():
        if "watchlist" in line.lower() or "관심" in line:
            print("Match in text:", line.strip()[:80])
