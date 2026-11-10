import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('rea/fm_2d_grid_match.html', encoding='utf-8') as f:
    text = f.read()

# 1. Verify PLAYERS_DATABASE parsed
start_marker = "const PLAYERS_DATABASE = "
end_marker = ";\n\n    // 공식 유튜브 하이라이트 매핑"
start_idx = text.find(start_marker) + len(start_marker)
end_idx = text.find(end_marker, start_idx)
assert start_idx != -1 and end_idx != -1, "PLAYERS_DATABASE markers not found"
players_json_str = text[start_idx:end_idx]
players = json.loads(players_json_str)
print(f"Total players in engine: {len(players)}")

son = [p for p in players if p['player_id'] == 2999][0]
haaland = [p for p in players if p['player_id'] == 1][0]
minjae = [p for p in players if p['player_id'] == 508][0]
kangin = [p for p in players if p['player_id'] == 315][0]

print(f"Son: {son['name_ko']} ({son['position']}) - {son['current_club']}")
print(f"Haaland: {haaland['name_ko']} ({haaland['position']}) - {haaland['current_club']}")
print(f"Minjae: {minjae['name_ko']} ({minjae['position']}) - {minjae['current_club']}")
print(f"Kangin: {kangin['name_ko']} ({kangin['position']}) - {kangin['current_club']}")

# 2. Check slot mapping code in calculate22Positions
assert "heroPos === 'LW') heroSlotId = 'H10'" in text
assert "heroPos === 'ST' || heroPos === 'CF') heroSlotId = 'H11'" in text
assert "heroPos === 'CB') heroSlotId = 'H3'" in text
assert "heroPos === 'AM'" in text
assert "p.id === heroSlotId" in text
assert "p.id === 'H1'" in text # GK safeguard
assert "isCurling" in text # Bezier curling shot

print("All assertion checks passed successfully!")
