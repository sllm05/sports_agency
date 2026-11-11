funcs = [
    'updateTransferClubsDropdown',
    'startTransferPipelineEvaluation',
    'finalizeTransferPipeline',
    'evaluateClientRenewalPipeline',
    'finalizeRenewalPipeline',
    'switchScatterView',
    'updateScoutingScatterChart',
    'setBosmanTargetType',
    'loadBosmanRadar',
    'updateCareerAgingChart'
]

with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

for fn in funcs:
    if f'function {fn}' in content:
        print(f'FOUND function {fn}')
    elif f'{fn} =' in content or f'{fn}(' in content:
        print(f'REFERENCED {fn}')
    else:
        print(f'MISSING {fn}')
