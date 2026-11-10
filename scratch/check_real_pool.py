import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

# Check players with expiring contracts (e.g. 2025 or 2026)
c.execute("SELECT player_id, name, name_ko, current_club, league, contract_expires, market_value_eur FROM players WHERE contract_expires LIKE '2025%' ORDER BY market_value_eur DESC LIMIT 10")
print("Top expiring players:")
for r in c.fetchall():
    print(r)

# Check highest market value players
c.execute("SELECT player_id, name, name_ko, current_club, league, contract_expires, market_value_eur FROM players ORDER BY market_value_eur DESC LIMIT 10")
print("\nTop market value players:")
for r in c.fetchall():
    print(r)

# Check Korean players
c.execute("SELECT player_id, name, name_ko, current_club, league, market_value_eur FROM players WHERE nationality='Korea, South' OR name_ko IN ('손흥민', '김민재', '이강인', '황희찬')")
print("\nKorean stars:")
for r in c.fetchall():
    print(r)
