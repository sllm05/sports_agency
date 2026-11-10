
with open('scratch/apply_index_updates.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for i in range(0, min(100, len(lines))):
    print(lines[i], end='')
