import sys, os
sys.path.insert(0, os.path.abspath("."))
import sqlite3
from mcp_server.football_mcp_server import toggle_target_watchlist, check_target_watchlist, list_agency_recruitment_targets

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("SELECT player_id, name FROM players WHERE name LIKE '%Son%' LIMIT 1")
son = c.fetchone()
conn.close()
print("Son:", son)

son_id = son[0]
print("1. Before toggle:", check_target_watchlist(son_id, "PLAYER"))

res_add = toggle_target_watchlist(son_id, "PLAYER")
print("2. Toggle add res:", res_add)
print("3. After toggle add:", check_target_watchlist(son_id, "PLAYER"))

targets = list_agency_recruitment_targets(category="ALL")
print("4. Total targets count:", len(targets["targets"]))
found = [t for t in targets["targets"] if t["target_id"] == son_id]
print("5. Found Son in targets:", len(found) > 0, found[0]["name"] if found else None)

res_rem = toggle_target_watchlist(son_id, "PLAYER")
print("6. Toggle rem res:", res_rem)
print("7. After toggle rem:", check_target_watchlist(son_id, "PLAYER"))
