import sys
sys.path.append('.')
import inspect
from mcp_server.football_mcp_server import toggle_target_watchlist, check_target_watchlist

print("=== toggle_target_watchlist ===")
print(inspect.getsource(toggle_target_watchlist))
print("\n=== check_target_watchlist ===")
print(inspect.getsource(check_target_watchlist))
