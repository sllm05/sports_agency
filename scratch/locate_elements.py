import re

path = r'src/sports_agency/api/static/index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

keywords = [
    'modal-client-transfer',
    'modal-client-renewal',
    'transfer-club-input',
    'transfer-fee-input',
    'startTransferPipelineEvaluation',
    'executeFinalTransferApproval',
    'startRenewalEvaluation',
    'renderPositionScatterPlot',
    '보스만 룰 타겟 구단',
    '5대 리그 외 유망주 등록',
    'incumbentCurve',
    'transfer-summary-club',
    'modal-transfer-final-success'
]

for kw in keywords:
    matches = [i+1 for i, line in enumerate(lines) if kw in line]
    print(f"{kw}: lines {matches[:10]}")
