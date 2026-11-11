with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    mcp_text = f.read()

# Extract simulate_client_club_renewal_pipeline and simulate_client_club_transfer_pipeline from mcp_server
import re
renew_m = re.search(r'(def simulate_client_club_renewal_pipeline\(.*?\n)(?=\ndef |\n@mcp\.tool|\n# ---)', mcp_text, re.DOTALL)
transfer_m = re.search(r'(def simulate_client_club_transfer_pipeline\(.*?\n)(?=\ndef |\n@mcp\.tool|\n# ---)', mcp_text, re.DOTALL)

with open('py/api_service.py', 'r', encoding='utf-8') as f:
    py_text = f.read()

if renew_m:
    py_text = re.sub(r'def simulate_client_club_renewal_pipeline\(.*?\n(?=\ndef |\n@|\n# ---)', renew_m.group(1), py_text, flags=re.DOTALL)
if transfer_m:
    py_text = re.sub(r'def simulate_client_club_transfer_pipeline\(.*?\n(?=\ndef |\n@|\n# ---)', transfer_m.group(1), py_text, flags=re.DOTALL)

with open('py/api_service.py', 'w', encoding='utf-8') as f:
    f.write(py_text)
print("Updated py/api_service.py to sync with mcp_server")
