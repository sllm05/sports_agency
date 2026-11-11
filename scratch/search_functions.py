with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Functions related to transfer:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*transfer[a-zA-Z0-9_]*)\(', text, re.I):
    print(" ", m.group(1))

print("Functions related to renewal:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*renewal[a-zA-Z0-9_]*)\(', text, re.I):
    print(" ", m.group(1))

print("Functions related to scatter:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*scatter[a-zA-Z0-9_]*)\(', text, re.I):
    print(" ", m.group(1))

print("Functions related to curve / aging:")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*(?:curve|aging)[a-zA-Z0-9_]*)\(', text, re.I):
    print(" ", m.group(1))
