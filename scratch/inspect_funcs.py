with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_range(start, count):
    print(f"=== Lines {start} to {start+count} ===")
    for i in range(start-1, min(len(lines), start-1+count)):
        print(f"{i+1}: {lines[i]}", end='')

print("=== evaluateClientRenewalPipeline ===")
for i, line in enumerate(lines):
    if 'evaluateClientRenewalPipeline' in line:
        print_range(max(1, i-2), 40)
        break

print("\n=== finalizeTransferPipeline ===")
for i, line in enumerate(lines):
    if 'finalizeTransferPipeline' in line:
        print_range(max(1, i-2), 40)
        break
