import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
korean_map = {
    1: '엘링 홀란드',
    2: '라민 야말',
    3: '킬리안 음바페',
    27: '아르다 귈러',
    38: '파우 쿠바르시',
    58: '코비 마이누',
    60: '아담 워튼',
    683: '팻슨 다카',
    708: '안수 파티',
    1153: '해리 윙크스',
    1770: '베르논 아도'
}
for pid, ko in korean_map.items():
    conn.execute('UPDATE players SET name_ko = ? WHERE player_id = ?', (ko, pid))
    conn.execute('UPDATE agency_recruitment_targets SET name_ko = ? WHERE target_id = ? AND target_type = "PLAYER"', (ko, pid))
conn.commit()
print('Updated Korean names successfully!')
for row in conn.execute('SELECT target_type, target_id, name, name_ko FROM agency_recruitment_targets'):
    print(row)
conn.close()
