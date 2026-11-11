with open('outputs/Michael_Olise_pitch_deck.md', 'r', encoding='utf-8') as f:
    c = f.read()
idx = c.find('DataMB 5대 리그 동 포지션 백분위 벤치마크')
if idx != -1:
    print(c[idx-100:idx+600])
else:
    print('Not found')
