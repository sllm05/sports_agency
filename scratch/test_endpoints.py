import requests

# 1. RAG Search
rag_res = requests.post('http://127.0.0.1:8000/api/rag/search', json={
    'query': '영국 FA GBE 워크퍼밋 15점 자동 통과 기준',
    'search_type': 'REGULATIONS',
    'top_k': 2
})
print('RAG status:', rag_res.status_code)
rag_data = rag_res.json()
print('RAG results count:', len(rag_data.get('results', [])))
if rag_data.get('results'):
    print('Top result title:', rag_data['results'][0].get('title'))
    print('Top result score:', rag_data['results'][0].get('similarity_score'))

# 2. Finance PSR
psr_res = requests.post('http://127.0.0.1:8000/api/finance/psr-tax', json={
    'league': 'Premier League',
    'transfer_fee_eur': 60000000,
    'weekly_wage_eur': 200000,
    'contract_years': 5,
    'agent_fee_pct': 6.5,
    'signing_bonus_eur': 5000000
})
print('PSR status:', psr_res.status_code)
psr_data = psr_res.json()
print('Annual PSR cost:', f"€{psr_data.get('annual_psr_book_cost_eur'):,}")
print('Net weekly wage:', f"€{psr_data.get('weekly_net_wage_eur'):,}")

# 3. DataMB Peer Matrix
datamb_res = requests.post('http://127.0.0.1:8000/api/scout/datamb-compare', json={
    'player_names': ['Erling Haaland', 'Julián Álvarez', 'Kylian Mbappé'],
    'position_category': 'ST',
    'season': '25/26'
})
print('DataMB status:', datamb_res.status_code)
datamb_data = datamb_res.json()
for p in datamb_data.get('players', []):
    npg = p['metrics'].get('npg', {}).get('raw_value')
    npxg = p['metrics'].get('npxg', {}).get('raw_value')
    conv = p['metrics'].get('conversion_pct', {}).get('raw_value')
    pct = p['metrics'].get('npg', {}).get('percentile')
    print(f"Player: {p['name']}, Mins: {p['minutes']}, NPG: {npg} (Pctl: {pct}%), npxG: {npxg}, Conv: {conv}%")

briefing = datamb_data.get('scouting_agent_briefing', {})
print('\n[Scouting Agent Verdict Headline]:', briefing.get('headline'))
print('[Minutes Verdict]:\n', briefing.get('minutes_sample_verdict'))
