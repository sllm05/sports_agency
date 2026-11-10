import sys
sys.path.append('.')
from mcp_server.football_mcp_server import generate_client_recruitment_pitch_deck

res = generate_client_recruitment_pitch_deck(101, "MANAGER")
print("Pitch deck generated for Pep Guardiola:")
print("Status:", "error" in res)
if "error" in res:
    print("Error:", res["error"])
else:
    print("Keys:", res.keys())
    print("Markdown length:", len(res.get("markdown_content", "")))
    print("Sample:\n", res.get("markdown_content", "")[:500])
