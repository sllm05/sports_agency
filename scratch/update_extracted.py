import sqlite3
import json
import re

# 1. Load players from data/agency_desk.db
conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

query = '''
SELECT p.player_id, p.name, p.position, p.current_club, p.league, p.market_value_eur,
       COALESCE(s.goals_per90, 0.0) as goals_per90,
       COALESCE(s.assists_per90, 0.0) as assists_per90,
       COALESCE(s.xg_per90, 0.0) as xg_per90,
       COALESCE(s.xa_per90, 0.0) as xa_per90,
       COALESCE(s.key_passes_per90, 0.0) as key_passes_per90,
       COALESCE(s.progressive_actions_per90, 0.0) as progressive_actions_per90,
       COALESCE(s.defensive_duels_won_pct, 50.0) as defensive_duels_won_pct,
       COALESCE(s.pos_percentile, 50) as pos_percentile,
       COALESCE(t.tactical_archetype, '') as tactical_archetype,
       COALESCE(t.strengths_tags, '') as strengths_tags,
       COALESCE(t.weaknesses_tags, '') as weaknesses_tags,
       COALESCE(t.progression_tendency, '') as progression_tendency,
       COALESCE(t.finishing_clinicality, '') as finishing_clinicality
FROM players p
LEFT JOIN player_stats s ON p.player_id = s.player_id
LEFT JOIN player_playstyle_and_tendencies t ON p.player_id = t.player_id
WHERE p.market_value_eur >= 65000000 OR p.player_id IN (2999, 508, 315, 625, 1072, 104)
ORDER BY p.market_value_eur DESC;
'''

cursor.execute(query)
rows = [dict(r) for r in cursor.fetchall()]

NAME_KO_MAP = {
    'Erling Haaland': '엘링 홀란드',
    'Heung-min Son': '손흥민',
    'Min-Jae Kim': '김민재',
    'Kang-in Lee': '이강인',
    'Kylian Mbappé': '킬리안 음바페',
    'Kevin De Bruyne': '케빈 데 브라위너',
    'Rodri': '로드리',
    'Virgil van Dijk': '버질 반 다이크',
    'Jude Bellingham': '주드 벨링엄',
    'Lamine Yamal': '라민 야말',
    'Vinicius Junior': '비니시우스 주니오르',
    'Bukayo Saka': '부카요 사카',
    'William Saliba': '윌리엄 살리바',
    'Pedri': '페드리',
    'Florian Wirtz': '플로리안 비르츠',
    'Jamal Musiala': '자말 무시알라',
    'Cole Palmer': '콜 파머',
    'Michael Olise': '마이클 올리세',
    'Declan Rice': '데클란 라이스',
    'Moisés Caicedo': '모이세스 카이세도',
    'Lautaro Martínez': '라우타로 마르티네스',
    'Alexander Isak': '알렉산더 이삭',
    'Ousmane Dembélé': '우스만 뎀벨레',
    'Federico Valverde': '페데리코 발베르데',
    'Arda Guler': '아르다 귈레르',
    'Jeremy Doku': '제레미 도쿠',
    'Pau Cubarsí': '파우 쿠바르시',
    'Achraf Hakimi': '아슈라프 하키미',
    'Nuno Mendes': '누누 멘데스',
    'Warren Zaïre-Emery': '워렌 자이르-에메리',
    'Khvicha Kvaratskhelia': '흐비차 크바라츠헬리아',
    'Joao Neves': '주앙 네베스',
    'Vitinha': '비티냐',
    'Julián Álvarez': '훌리안 알바레스',
    'Enzo Fernández': '엔소 페르난데스',
    'Bryan Mbeumo': '브라이언 음뵈모',
    'Matheus Cunha': '마테우스 쿠냐',
    'Benjamin Šeško': '벤야민 세슈코',
    'Kenan Yıldız': '케난 일디즈',
    'Elliot Anderson': '엘리엇 앤더슨',
    'Martín Zubimendi': '마르틴 수비멘디',
    'Ryan Gravenberch': '라이언 흐라번베르흐',
    'Hugo Ekitike': '위고 에키티케',
    'Antoine Semenyo': '앙투안 세메뇨',
    'Sandro Tonali': '산드로 토날리',
    'Nico Paz': '니코 파스',
    'Desire Doue': '데지레 두에',
    'Fermín López': '페르민 로페스',
    'Dominik Szoboszlai': '도미니크 소보슬라이',
    'Rayan Cherki': '라얀 셰르키',
    'Morgan Rogers': '모건 로저스',
    'Yan Diomandé': '얀 디오망데',
    'Aleksandar Pavlović': '알렉산다르 파블로비치',
    'João Pedro': '주앙 페드로',
    'Estevao': '에스테방'
}

for r in rows:
    r['name_ko'] = NAME_KO_MAP.get(r['name'], r['name'])

# Priority sorting: 손흥민 (2999), 홀란드 (1), 김민재 (508), 이강인 (315), 그 외
special_ids = [2999, 1, 508, 315]
special_players = [r for r in rows if r['player_id'] in special_ids]
other_players = [r for r in rows if r['player_id'] not in special_ids]
special_players.sort(key=lambda x: special_ids.index(x['player_id']))
all_players = special_players + other_players

with open('rea/extracted_players.json', 'w', encoding='utf-8') as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

print(f"Updated rea/extracted_players.json with {len(all_players)} players.")
