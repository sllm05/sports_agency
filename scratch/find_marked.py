with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'marked' in line or 'contract-markdown' in line or 'doc-writer' in line or 'renderMarkdown' in line:
            print(f'{i+1}: {line.strip()[:100]}')
