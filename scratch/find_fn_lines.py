with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for fn in ['startTransferPipelineEvaluation', 'finalizeTransferPipeline', 'evaluateClientRenewalPipeline', 'finalizeRenewalPipeline', 'switchScatterView', 'updateScoutingScatterChart', 'loadBosmanRadar', 'updateCareerAgingChart']:
    for i, line in enumerate(lines):
        if f'function {fn}' in line:
            print(f'{fn} is at line {i+1}')
