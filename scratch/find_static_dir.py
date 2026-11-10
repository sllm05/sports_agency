with open("src/sports_agency/api/main.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if "STATIC_DIR" in line:
            print(f"{i+1}: {line.strip()}")
