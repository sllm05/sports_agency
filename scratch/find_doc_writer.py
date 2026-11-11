with open('src/sports_agency/agents/document_writer.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Opta / FBref' in line or 'DataMB' in line or '<div' in line:
            print(f'{i+1}: {line.strip()[:100]}')
