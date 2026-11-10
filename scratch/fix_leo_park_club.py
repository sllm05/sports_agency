import sqlite3

conn = sqlite3.connect("data/agency_desk.db")
c = conn.cursor()
c.execute("""
    UPDATE players 
    SET current_club = '네오 뮌헨 FC', league = '가상 유로 챌린지'
    WHERE player_id = 90001
""")
conn.commit()
print("Updated 90001 player to virtual club '네오 뮌헨 FC'")
conn.close()
