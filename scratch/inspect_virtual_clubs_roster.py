import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
c = conn.cursor()

virtual_clubs = [
    '네오 뮌헨 FC',
    '메트로폴리스 FC',
    '솔라리스 시티 FC',
    '루미나르 SC',
    '아발론 유나이티드',
    '아틀라스 FC',
    '한양 시티 FC',
    '호라이즌 로버스'
]

print("--- CURRENT ROSTER OF VIRTUAL CLUBS ---")
for club in virtual_clubs:
    c.execute("SELECT player_id, name, position, market_value_eur FROM players WHERE current_club = ?", (club,))
    players = c.fetchall()
    c.execute("SELECT manager_id, name, preferred_formation FROM managers WHERE current_club = ?", (club,))
    managers = c.fetchall()
    print(f"\n[CLUB: {club}]")
    print(f"  Players ({len(players)}): {players}")
    print(f"  Managers ({len(managers)}): {managers}")
