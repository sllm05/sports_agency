import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

c.execute("SELECT contract_expires, count(*) FROM players GROUP BY contract_expires ORDER BY count(*) DESC LIMIT 20")
print("Player contract expiry distribution:")
for r in c.fetchall():
    print(r)

# Check players with earliest contract expiration
c.execute("SELECT player_id, name, name_ko, current_club, league, contract_expires, market_value_eur FROM players WHERE contract_expires IS NOT NULL AND contract_expires != '' ORDER BY contract_expires ASC LIMIT 15")
print("\nEarliest expiring contracts:")
for r in c.fetchall():
    print(r)

# Check young high market value players (< 23)
c.execute("SELECT player_id, name, name_ko, current_club, league, age, market_value_eur FROM players WHERE age <= 22 ORDER BY market_value_eur DESC LIMIT 15")
print("\nTop U-22 Wonderkids:")
for r in c.fetchall():
    print(r)

# Check managers
c.execute("SELECT manager_id, name, current_club, league, contract_expires, points_per_game, win_rate_pct FROM managers ORDER BY win_rate_pct DESC LIMIT 15")
print("\nTop Managers by win rate:")
for r in c.fetchall():
    print(r)
