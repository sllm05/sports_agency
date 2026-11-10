with open('mcp_server/football_mcp_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 1750-1850:")
for i in range(1750, 1850):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
