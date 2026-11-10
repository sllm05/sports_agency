with open("mcp_server/football_mcp_server.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
for idx, line in enumerate(lines, 1):
    if "def enroll_target_as_agency_client" in line or "def terminate_agency_client_contract" in line:
        print(f"L{idx}: {line.strip()}")
