import urllib.request
import json

res = urllib.request.urlopen("http://127.0.0.1:8000/api/agency/portfolio")
data = json.loads(res.read())
print("Portfolio summary:", data["summary"])
print("Players count:", len(data["players"]))
print("Managers count:", len(data["managers"]))
