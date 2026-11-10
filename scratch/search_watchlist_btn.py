with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

print("Has toggleCurrentPlayerWatchlist?", "toggleCurrentPlayerWatchlist" in text)
for i, line in enumerate(text.splitlines()):
    if "toggleCurrentPlayerWatchlist" in line or "scouting-watchlist" in line:
        print(f"{i+1}: {line.strip()[:100]}")
