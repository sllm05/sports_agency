import sys
sys.path.append('.')
import inspect
from mcp_server.football_mcp_server import list_agency_recruitment_targets

print(inspect.getsource(list_agency_recruitment_targets))
