import sys
sys.path.insert(0, '.')
from collections import defaultdict
from mcp_server.football_mcp_server import list_agency_players

def run_tests():
    print("Fetching players via list_agency_players()...")
    players = list_agency_players()
    print(f"Total players & managers returned: {len(players)}")

    BIG_5_LEAGUES = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']
    VIRTUAL_LEAGUES = ['TEST_LEAGUE', 'VIRTUAL_LEAGUE', '테스트/가상 리그 (Virtual League)', 'TEST', 'VIRTUAL', '테스트/가상 리그']
    VIRTUAL_CLUBS = [
        '네오 뮌헨 FC',
        '메트로폴리스 FC',
        '솔라리스 시티 FC',
        '루미나르 SC',
        '아발론 유나이티드',
        '아틀라스 FC',
        '한양 시티 FC',
        '호라이즌 로버스'
    ]

    def is_virtual_player(p):
        if not p:
            return False
        if p.get('player_id', 0) >= 90000 and p.get('player_id', 0) <= 90200:
            return True
        if p.get('current_club') in VIRTUAL_CLUBS:
            return True
        lg = p.get('league') or ''
        if '테스트' in lg or '가상' in lg or 'Virtual' in lg:
            return True
        return False

    # 1. Test Premier League clubs
    pl_players = [p for p in players if p.get('league') == 'Premier League' and not is_virtual_player(p)]
    pl_clubs = set(p['current_club'] for p in pl_players)
    print(f"\n[TEST 1] Premier League Clubs: {len(pl_clubs)} (Expected: 20)")
    assert len(pl_clubs) == 20, f"Expected 20 PL clubs, got {len(pl_clubs)}: {pl_clubs}"
    assert 'Manchester City' not in pl_clubs, "'Manchester City' dummy club still exists!"
    assert 'Manchester City FC' in pl_clubs, "'Manchester City FC' missing!"
    assert 'Tottenham Hotspur' not in pl_clubs, "'Tottenham Hotspur' dummy club still exists!"
    assert 'Tottenham Hotspur FC' in pl_clubs, "'Tottenham Hotspur FC' missing!"

    mcfc_players = [p for p in pl_players if p['current_club'] == 'Manchester City FC']
    print(f"  Manchester City FC player count: {len(mcfc_players)} (Expected: 25)")
    assert len(mcfc_players) == 25, f"Expected 25, got {len(mcfc_players)}"
    haaland = next((p for p in mcfc_players if 'Haaland' in p['name']), None)
    assert haaland is not None, "Erling Haaland missing from Manchester City FC!"
    print(f"  -> Verified Haaland in Manchester City FC: ID={haaland['player_id']}, Name={haaland['name']}")

    spurs_players = [p for p in pl_players if p['current_club'] == 'Tottenham Hotspur FC']
    print(f"  Tottenham Hotspur FC player count: {len(spurs_players)} (Expected: 30)")
    assert len(spurs_players) == 30, f"Expected 30, got {len(spurs_players)}"
    son = next((p for p in spurs_players if 'Son' in p['name']), None)
    assert son is not None, "Heung-min Son missing from Tottenham Hotspur FC!"
    print(f"  -> Verified Son in Tottenham Hotspur FC: ID={son['player_id']}, Name={son['name']}")

    # 2. Test Bundesliga clubs
    bl_players = [p for p in players if p.get('league') == 'Bundesliga' and not is_virtual_player(p)]
    bl_clubs = set(p['current_club'] for p in bl_players)
    print(f"\n[TEST 2] Bundesliga Clubs: {len(bl_clubs)} (Expected: 18)")
    assert len(bl_clubs) == 18, f"Expected 18 BL clubs, got {len(bl_clubs)}: {bl_clubs}"
    assert 'FC 바이에른 뮌헨' not in bl_clubs, "'FC 바이에른 뮌헨' dummy club still exists!"
    assert 'FC Bayern München' in bl_clubs, "'FC Bayern München' missing!"
    bayern_players = [p for p in bl_players if p['current_club'] == 'FC Bayern München']
    musiala = next((p for p in bayern_players if 'Musiala' in p['name']), None)
    assert musiala is not None, "Jamal Musiala missing from FC Bayern München!"
    print(f"  -> Verified Musiala in FC Bayern München: ID={musiala['player_id']}, Name={musiala['name']}")

    # 3. Test All Big 5 Clubs total
    big5_players = [p for p in players if p.get('league') in BIG_5_LEAGUES and not is_virtual_player(p)]
    big5_clubs = set(p['current_club'] for p in big5_players)
    print(f"\n[TEST 3] Total Big 5 Clubs: {len(big5_clubs)} (Expected: exactly 96)")
    assert len(big5_clubs) == 96, f"Expected exactly 96 Big 5 clubs, got {len(big5_clubs)}"

    # 4. Test Virtual League
    virt_players = [p for p in players if is_virtual_player(p)]
    virt_clubs = set(p['current_club'] for p in virt_players)
    print(f"\n[TEST 4] Virtual League Clubs: {len(virt_clubs)} (Expected: 8)")
    print(f"  Virtual Clubs found: {sorted(list(virt_clubs))}")
    assert len(virt_clubs) == 8, f"Expected 8 virtual clubs, got {len(virt_clubs)}"
    for vc in VIRTUAL_CLUBS:
        assert vc in virt_clubs, f"Virtual club '{vc}' missing from virtual league!"
        c_members = [p for p in virt_players if p['current_club'] == vc]
        print(f"   [{vc}] {len(c_members)} members: {[m['name'] for m in c_members]}")

    print("\nALL TESTS PASSED 100%! DATA INTEGRITY VERIFIED.")

if __name__ == "__main__":
    run_tests()
