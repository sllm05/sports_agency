import json

# Load extracted players
with open('rea/extracted_players.json', encoding='utf-8') as f:
    players_data = json.load(f)

print(f"Loaded {len(players_data)} players for embedding.")
