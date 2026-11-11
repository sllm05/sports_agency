with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_around(pattern, count=30):
    for i, line in enumerate(lines):
        if pattern in line:
            print(f"=== Found '{pattern}' at line {i+1} ===")
            for j in range(max(0, i-5), min(len(lines), i+count)):
                print(f"{j+1}: {lines[j]}", end='')
            break

print_around('scoutingScatterChart', 40)
print_around('external-prospect-input', 30)
print_around('updateCareerAgingChart', 50)
