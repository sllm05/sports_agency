with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
def show_func(name):
    m = re.search(r'function\s+' + name + r'\s*\([^)]*\)\s*\{', text)
    if m:
        start = m.start()
        print(f"=== {name} ===")
        print(text[start:start+1200])
        print("="*60)
    else:
        print(f"Function {name} not found")

show_func('switchScatterView')
show_func('updateScoutingScatterChart')
show_func('openClientTransferModal')
show_func('startTransferPipelineEvaluation')
show_func('finalizeTransferPipeline')
