with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 2080-2170:")
for i in range(2080, 2170):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
