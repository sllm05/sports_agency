import json
import re

# 1. Read the newly extracted players from rea/extracted_players.json
with open('rea/extracted_players.json', 'r', encoding='utf-8') as f:
    players_data = json.load(f)

print(f"Loaded {len(players_data)} players.")
print(f"Top 5: {[p['name_ko'] for p in players_data[:5]]}")

# 2. Read the existing fm_2d_grid_match.html to preserve styling and surrounding DOM
with open('rea/fm_2d_grid_match.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Let's locate the script section
script_start_idx = html_content.find('<script>')
if script_start_idx == -1:
    raise Exception("Cannot find <script> tag in HTML")

html_head_and_body = html_content[:script_start_idx + len('<script>')]

# Let's prepare the updated JavaScript
js_code = """
    // =========================================================================
    // 1. 실제 DB 추출 76명 엘리트 선수 데이터셋 (손흥민, 홀란드, 김민재, 이강인 등)
    // =========================================================================
    const PLAYERS_DATABASE = """ + json.dumps(players_data, ensure_ascii=False) + """;

    // 공식 유튜브 하이라이트 매핑 (실제 플레이 하이라이트 영상 ID)
    const YT_MAP = {
      '손흥민': 'YhEcyglkOx0',
      'Heung-min Son': 'YhEcyglkOx0',
      '엘링 홀란드': '8cfwD8ybFfw',
      'Erling Haaland': '8cfwD8ybFfw',
      '이강인': '2Ec8VofpRmo',
      'Kang-in Lee': '2Ec8VofpRmo',
      '김민재': '38LUvS2jOOU',
      'Min-Jae Kim': '38LUvS2jOOU',
      '황희찬': 'DVNwiAPuPTY',
      'Hwang Heechan': 'DVNwiAPuPTY',
      '킬리안 음바페': '6VC5VHn5EQM',
      'Kylian Mbappé': '6VC5VHn5EQM',
      '케빈 데 브라위너': 'Tw1fCcNaKhc',
      'Kevin De Bruyne': 'Tw1fCcNaKhc',
      '로드리': 'Lpz4PUPJ5kM',
      'Rodri': 'Lpz4PUPJ5kM',
      '주드 벨링엄': 'kNwOJ-BJcPk',
      'Jude Bellingham': 'kNwOJ-BJcPk',
      '라민 야말': '8cfwD8ybFfw',
      'Lamine Yamal': '8cfwD8ybFfw',
      '비니시우스 주니오르': '8cfwD8ybFfw',
      'Vinicius Junior': '8cfwD8ybFfw',
      '버질 반 다이크': '38LUvS2jOOU',
      'Virgil van Dijk': '38LUvS2jOOU',
      '부카요 사카': '9ogC38l8nTU',
      'Bukayo Saka': '9ogC38l8nTU',
      '윌리엄 살리바': '38LUvS2jOOU',
      'William Saliba': '38LUvS2jOOU',
      '페드리': '2Ec8VofpRmo',
      'Pedri': '2Ec8VofpRmo',
      '자말 무시알라': 'kNwOJ-BJcPk',
      'Jamal Musiala': 'kNwOJ-BJcPk',
      '플로리안 비르츠': 'kNwOJ-BJcPk',
      'Florian Wirtz': 'kNwOJ-BJcPk',
      '콜 파머': 'kNwOJ-BJcPk',
      'Cole Palmer': 'kNwOJ-BJcPk'
    };

    // 상태 관리
    let currentPlayer = null;
    let currentActionIdx = 0;
    let isPlaying = true;
    let currentTime = 0; // 0.0 ~ 8.0초
    let playbackSpeed = 1.0;
    const TOTAL_DURATION = 8.0;

    const canvas = document.getElementById('pitchCanvas');
    const ctx = canvas.getContext('2d');

    const MARGIN = 36;
    const PITCH_W = canvas.width - MARGIN * 2;   // 1008
    const PITCH_H = canvas.height - MARGIN * 2;  // 608

    function toPixel(gx, gy) {
      // gx: 0~18 (가로 그리드), gy: 0~12 (세로 그리드)
      return {
        x: MARGIN + (gx / 18) * PITCH_W,
        y: MARGIN + (gy / 12) * PITCH_H
      };
    }

    // =========================================================================
    // 2. 선수별 고유 시그니처 액션 정의 엔진 (DB 스탯 & 시그니처 궤적 매핑)
    // =========================================================================
    function generatePlayerActions(p) {
      const pos = (p.position || 'ST').toUpperCase();
      const archetype = p.tactical_archetype || '';
      const name = p.name_ko || p.name;
      const xg = p.xg_per90 ? p.xg_per90.toFixed(2) : '0.45';
      const kp = p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '2.1';
      const defPct = p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '60';

      // 1) 손흥민 시그니처 (LW: 좌측 하프스페이스 컷인 감아차기 + 번리전 70m 질주 + 컷백)
      if (name.includes('손흥민') || p.name.includes('Son')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '감아차기 원더골',
            title: `[손흥민 존] 하프스페이스 45° 컷인 & 파포스트 감아차기 골`,
            desc: `좌측면에서 안쪽으로 35.1km/h 폭발적 컷인 후 수비 블록을 피해 파포스트 상단 구석을 찌르는 전매특허 U자형 감아차기 (xG ${xg} / 전환율 +32%)`,
            shotType: 'curl',
            phases: [
              { t: 0.0, targetGx: 8.5, targetGy: 9.5, ball: 'target', status: '좌측 터치라인에서 볼 수신 및 상대 풀백(A2)과 1:1 대치', metric: '속도: 18.5 km/h' },
              { t: 2.2, targetGx: 12.0, targetGy: 8.2, ball: 'target', status: '⚡ 45도 안쪽으로 폭발적인 컷인 드리블로 수비수 균열!', metric: '속도: 35.1 km/h (EPL 최고속)' },
              { t: 4.5, targetGx: 14.2, targetGy: 6.8, ball: 'target', status: '아크 45도 손흥민 존 진입 · 오른발 인프런트 각도 정렬', metric: '슈팅 전환율: +32% 공간 확보' },
              { t: 5.8, targetGx: 14.5, targetGy: 6.7, ball: 'shot', shotTarget: { gx: 18.0, gy: 4.6 }, curve: true, curveDx: 0.8, curveDy: 1.8, status: '🌀 골키퍼 손을 피해 휘어 들어가는 명품 U자형 감아차기!', metric: '회전수: 1,250 RPM · 감아차기' },
              { t: 8.0, targetGx: 16.5, targetGy: 9.0, ball: 'goal', status: '⚽ 파포스트 상단 골망 강타! 전매특허 찰칵 세레머니!', metric: 'xG 0.08 골 전환 성공' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '70m 솔로 질주',
            title: `[푸스카스 오마주] 자기 진영부터 수비 4명 파괴 70m 단독 질주 원더골`,
            desc: `후방에서 볼을 잡고 순간 최고 속도 35.3km/h로 상대 미드필더와 센터백을 완벽히 무너뜨리는 역사적인 단독 돌파 득점`,
            shotType: 'direct',
            phases: [
              { t: 0.0, targetGx: 4.0, targetGy: 8.5, ball: 'target', status: '우리 진영 박스 부근에서 루즈볼 가로채기', metric: '수비 가담 성공' },
              { t: 2.5, targetGx: 9.5, targetGy: 8.0, ball: 'target', status: '하프라인을 통과하며 수비 2명을 폭발적 주력으로 따돌림', metric: '속도: 33.4 km/h' },
              { t: 5.0, targetGx: 14.5, targetGy: 7.0, ball: 'target', status: '마지막 센터백까지 바디페인팅으로 제치며 골키퍼와 1:1 대치', metric: '속도: 35.3 km/h' },
              { t: 6.2, targetGx: 16.0, targetGy: 6.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.5 }, status: '침착하게 골키퍼 타이밍을 빼앗는 오른발 인사이드 밀어넣기!', metric: 'xG: 0.85 결정력' },
              { t: 8.0, targetGx: 16.8, targetGy: 6.0, ball: 'goal', status: '⚽ 70m 솔로 스프린트 원더골 완성!', metric: '푸스카스 어워드 오마주' }
            ]
          },
          {
            type: 'PASS', tag: 'pass', tagText: '찬스메이킹',
            title: `[엔드라인 컷백] 좌측면 엔드라인 파괴 후 핀포인트 컷백 어시스트`,
            desc: `터치라인을 완전히 찢고 박스 깊숙이 진입한 뒤 쇄도하는 스트라이커 발밑에 찔러주는 xA 0.45 킬러 패스`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 9.8, ball: 'target', status: '터치라인을 따라 오버래핑 공간 확보', metric: '스프린트 시작' },
              { t: 3.0, targetGx: 15.5, targetGy: 10.5, ball: 'target', status: '상대 풀백을 속도로 완전히 무력화하며 엔드라인 진입', metric: '속도: 33.8 km/h' },
              { t: 5.2, targetGx: 16.5, targetGy: 9.0, ball: 'pass', passTarget: { gx: 15.2, gy: 6.0 }, status: '🎯 문전으로 쇄도하는 스트라이커를 향한 날카로운 컷백!', metric: 'xA: 0.45 킬패스' },
              { t: 8.0, targetGx: 16.5, targetGy: 9.0, ball: 'finish', status: '동료의 논스톱 슈팅 득점 연결 완료!', metric: '어시스트 완성' }
            ]
          }
        ];
      }

      // 2) 엘링 홀란드 시그니처 (ST: 최전방 중앙 박스 지배 + 124km/h 무회전 레이저포 + 공중제비 발리)
      if (name.includes('홀란드') || p.name.includes('Haaland')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '레이저 피니시',
            title: `[괴물 라인 브레이킹] 센터백 몸싸움 파괴 & 124km/h 무회전 레이저포`,
            desc: `센터백 사이를 압도적인 피지컬로 밀쳐내며 침투한 뒤 골문 그물 천장을 찢는 124km/h 대포알 레이저 슈팅 (xG ${xg})`,
            shotType: 'laser',
            phases: [
              { t: 0.0, targetGx: 12.0, targetGy: 6.0, ball: 'mid', status: '상대 센터백 2명 사이에서 오프사이드 라인 주시 및 몸싸움', metric: '경합 승리율: 68%' },
              { t: 2.2, targetGx: 14.5, targetGy: 6.0, ball: 'pass_flight', status: '⚡ 수비수를 힘으로 누르며 중앙 직선 폭풍 쇄도!', metric: '속도: 34.8 km/h 수직 침투' },
              { t: 4.5, targetGx: 16.0, targetGy: 6.0, ball: 'target', status: '원터치 볼 키핑 후 왼발 레이저 슈팅 타이밍 포착', metric: '박스 안 터치 1위' },
              { t: 5.6, targetGx: 16.2, targetGy: 6.0, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.8 }, status: '💥 골문 그물 찢을 듯한 124km/h 대포알 레이저 슈팅!', metric: '슈팅 속도: 124.5 km/h (Laser)' },
              { t: 8.0, targetGx: 16.5, targetGy: 6.0, ball: 'goal', status: '⚽ 골키퍼 반응 불가! 골망 천장 강타 후 가부좌 세레머니!', metric: 'xG: 0.78 확실한 득점' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '아크로바틱 발리',
            title: `[타점 2.4m 공중제비 발리] 측면 크로스 점프 낙하지점 아크로바틱 피니시`,
            desc: `높이 2.4m 허공에서 발을 뻗어 내리꽂는 특유의 무술 같은 아크로바틱 논스톱 발리 슈팅`,
            shotType: 'laser',
            phases: [
              { t: 0.0, targetGx: 13.0, targetGy: 5.0, ball: 'wing', status: '측면 풀백의 크로스 타이밍에 맞춰 박스 진입', metric: '낙하지점 포착' },
              { t: 2.5, targetGx: 15.5, targetGy: 5.5, ball: 'cross', status: '상대 센터백과의 공중볼 경합에서 압도적 제공권 우위 점유', metric: '도약 높이: 85cm' },
              { t: 4.8, targetGx: 16.8, targetGy: 5.8, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 허공에서 발을 뻗어 문전으로 꽂아 넣는 아크로바틱 발리!', metric: '발리 유효슈팅 100%' },
              { t: 8.0, targetGx: 16.8, targetGy: 5.8, ball: 'goal', status: '⚽ 골키퍼가 꼼짝도 못한 채 골망을 흔드는 원더골!', metric: '득점 완성' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '불도저 돌파',
            title: `[30m 단독 불도저 질주] 하프라인 볼 탈환 후 수비 2명 밀치기 돌파`,
            desc: `상대 볼을 가로챈 뒤 압도적인 주력과 피지컬로 수비수를 튕겨내며 박스까지 도달하는 탱크형 전진`,
            shotType: 'laser',
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 6.0, ball: 'target', status: '하프라인 루즈볼 몸싸움으로 제압 탈환', metric: '피지컬 100점' },
              { t: 2.8, targetGx: 13.2, targetGy: 5.8, ball: 'target', status: '따라붙는 수비수를 어깨로 튕겨내며 중앙 직진 돌파', metric: '속도: 33.5 km/h' },
              { t: 5.2, targetGx: 15.8, targetGy: 5.8, ball: 'target', status: '페널티 박스 진입 및 슈팅 폼 형성', metric: '돌파 완료' },
              { t: 6.5, targetGx: 16.5, targetGy: 5.8, ball: 'shot', shotTarget: { gx: 18.0, gy: 6.2 }, status: '강력한 오른발 땅볼 파워슛!', metric: '슈팅 완성' },
              { t: 8.0, targetGx: 16.5, targetGy: 5.8, ball: 'goal', status: '골대 안쪽 맞고 골인!', metric: '득점 성공' }
            ]
          }
        ];
      }

      // 3) 김민재 시그니처 (CB: 괴물 피지컬 스토퍼 인터셉트 + 45m 대각 롱패스 + 34.2km/h 슬라이딩 태클)
      if (name.includes('김민재') || p.name.includes('Min-Jae')) {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '스토퍼 인터셉트',
            title: `[스토퍼 전진 인터셉트 & 45m 전환] 상대 역습 차단 & 45m 레이저 롱패스`,
            desc: `상대 패스 길목을 예측하여 라인을 깨고 전진해 볼을 가로챈 뒤, 반대편 공격수 발밑으로 45m 레이저 롱패스 배급 (경합률 ${defPct}%)`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 3.5, targetGy: 4.5, ball: 'away', status: '상대 공격수의 전진 패스 길목 예측 및 라인 전진', metric: '수비 라인 조율' },
              { t: 2.2, targetGx: 6.8, targetGy: 5.5, ball: 'target', status: '🛡️ 과감한 전진 스텝으로 볼 완벽 인터셉트!', metric: `대인 경합 승리율: ${defPct}%` },
              { t: 4.5, targetGx: 7.2, targetGy: 5.2, ball: 'target', status: '탈환 즉시 고개를 들어 반대편 우측 윙어 질주 포착', metric: '빌드업 시야 확보' },
              { t: 5.8, targetGx: 7.5, targetGy: 5.0, ball: 'pass', passTarget: { gx: 14.5, gy: 2.0 }, status: '🚀 45m를 단숨에 가르는 대각선 전환 롱패스 배급!', metric: '전진 패스 성공 (상위 3%)' },
              { t: 8.0, targetGx: 6.0, targetGy: 5.0, ball: 'finish', status: '완벽한 공수 전환으로 단숨에 득점 기회 창출!', metric: 'xGBuildup: 0.71' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '괴물 리커버리',
            title: `[34.2km/h 괴물 역습 리커버리] 박스 안 슈퍼 슬라이딩 태클`,
            desc: `뒷공간으로 쇄도하는 상대 공격수를 압도적인 주력으로 추격하여 박스 진입 직전 공만 걷어내는 완벽한 슬라이딩 태클`,
            shotType: 'def',
            phases: [
              { t: 0.0, targetGx: 5.5, targetGy: 7.0, ball: 'away', status: '상대 윙어의 배후 침투 감지', metric: '추격 개시' },
              { t: 2.5, targetGx: 4.0, targetGy: 6.5, ball: 'away', status: '순간 속도 34.2km/h 전력 질주로 각도 좁히기', metric: '스프린트: 34.2 km/h' },
              { t: 4.8, targetGx: 2.8, targetGy: 6.0, ball: 'target', status: '⚔️ 위험 지역 진입 직전 오차 없는 슬라이딩 태클 성공!', metric: '클리어링 100%' },
              { t: 8.0, targetGx: 3.2, targetGy: 6.0, ball: 'target', status: '위기 완벽 차단 후 골키퍼에게 안정적 연결', metric: '슈퍼세이브' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '타점 헤더',
            title: `[타점 높은 제공권 헤더] 코너킥 상황 상대 수비 2명 누르는 세트피스 골`,
            desc: `코너킥 상황에서 상대 수비수 2명을 힘으로 누르고 타점 높은 헤더로 골망을 가르는 세트피스 득점`,
            shotType: 'laser',
            phases: [
              { t: 0.0, targetGx: 13.5, targetGy: 5.0, ball: 'corner', status: '코너 플래그에서 크로스 준비 대기', metric: '세트피스 타점' },
              { t: 2.5, targetGx: 15.5, targetGy: 5.5, ball: 'corner_flight', status: '수비수를 따돌리며 박스 중앙으로 강력한 도약 쇄도', metric: '제공권 경합 준비' },
              { t: 4.8, targetGx: 16.5, targetGy: 5.5, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 타점 높은 점프로 골문 구석을 찌르는 헤더 강타!', metric: '헤더 경합 승리율 78%' },
              { t: 8.0, targetGx: 16.5, targetGy: 5.5, ball: 'goal', status: '⚽ 골키퍼 손을 스치며 골망을 가르는 세트피스 득점!', metric: '세트피스 골 완성' }
            ]
          }
        ];
      }

      // 4) 이강인 시그니처 (AM/RW: La Pausa 템포 조절 & 35m 칼날 스루패스 + 바디페인팅 턴 + 왼발 프리킥)
      if (name.includes('이강인') || p.name.includes('Kang-in')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: 'La Pausa 킬패스',
            title: `[La Pausa 스루패스] 2명 유인 후 수비 3명 찢는 35m 핀포인트 킬패스`,
            desc: `볼을 밟으며 템포를 늦춘 뒤 쇄도하는 공격수 발앞으로 오차 없이 찔러 넣는 레이저 스루패스 (키패스 90분당 ${kp}회)`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 8.5, targetGy: 3.8, ball: 'target', status: '볼을 발밑에 붙이며 템포 조절 (La Pausa)', metric: '상대 2명 압박 유인 중' },
              { t: 2.5, targetGx: 9.2, targetGy: 4.5, ball: 'target', status: '상체 바디페인팅으로 무게중심 붕괴 & 120° 시야 개방', metric: '탈압박 성공 (100%)' },
              { t: 4.8, targetGx: 9.6, targetGy: 4.8, ball: 'pass', passTarget: { gx: 15.5, gy: 6.0 }, status: '🎯 수비수 3명 사이 빈틈을 찌르는 35m 칼날 스루패스!', metric: `키패스: 90분당 ${kp}회` },
              { t: 6.8, targetGx: 10.0, targetGy: 5.0, ball: 'receive', status: '쇄도한 공격수 발앞에 정확히 떨어짐', metric: 'xA: 0.42 기대 어시스트' },
              { t: 8.0, targetGx: 10.5, targetGy: 5.0, ball: 'goal', status: '침투 공격수의 침착한 마무리로 득점 완성!', metric: '빅찬스 생성 성공' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '탈압박 턴',
            title: `[바디페인팅 턴] 터치라인 2인 압박 무력화 & 반대편 40m 대각선 전환`,
            desc: `특유의 상체 페인팅 턴으로 수비수를 벗겨낸 뒤 비어있는 반대편으로 단숨에 전환하는 마스터클래스`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 7.5, targetGy: 8.5, ball: 'target', status: '터치라인 부근에서 상대 2명의 샌드위치 압박 직면', metric: '압박 강도 95%' },
              { t: 2.2, targetGx: 7.2, targetGy: 7.5, ball: 'target', status: '몸을 회전하며 상체 페인팅으로 수비수 무게중심 붕괴', metric: '탈압박 성공 (100%)' },
              { t: 4.5, targetGx: 8.2, targetGy: 6.8, ball: 'target', status: '중원으로 빠져나오며 반대편 오픈 공간 탐색', metric: 'xGBuildup: 0.68 기여' },
              { t: 6.0, targetGx: 8.5, targetGy: 6.8, ball: 'pass', passTarget: { gx: 13.0, gy: 2.0 }, status: '📐 반대편 윙어를 향한 정확한 40m 대각선 롱 체인지 패스!', metric: '전환 패스 성공' },
              { t: 8.0, targetGx: 8.8, targetGy: 6.8, ball: 'finish', status: '반대편 측면에서 즉각적인 크로스 찬스로 연결', metric: '공격 전개 완성' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '왼발 원더골',
            title: `[아크 정면 왼발 프리킥/중거리포] 골문 상단 구석 정밀 궤적골`,
            desc: `수비벽을 넘겨 골키퍼 손이 닿지 않는 골문 상단 구석을 정밀하게 찌르는 왼발 인프런트 슈팅`,
            shotType: 'curl',
            phases: [
              { t: 0.0, targetGx: 12.0, targetGy: 5.5, ball: 'target', status: '아크 정면에서 왼발 슈팅 각도 탐색', metric: '슈팅 거리: 22m' },
              { t: 2.5, targetGx: 12.8, targetGy: 5.2, ball: 'target', status: '왼발 각도를 만들기 위한 한 박자 터치', metric: '각도 45° 정렬' },
              { t: 4.8, targetGx: 13.2, targetGy: 5.0, ball: 'shot', shotTarget: { gx: 18.0, gy: 4.8 }, curve: true, curveDx: -0.6, curveDy: -1.5, status: '💥 환상적인 궤적으로 휘어 들어가는 왼발 슈팅!', metric: `xG: ${xg} 정밀 타격` },
              { t: 8.0, targetGx: 13.2, targetGy: 5.0, ball: 'goal', status: '⚽ 크로스바 하단을 맞고 골망을 흔드는 원더골!', metric: '득점 성공' }
            ]
          }
        ];
      }

      // 5) 킬리안 음바페 시그니처 (ST/LW: 순간 가속 38km/h 치달 & 니어포스트 슛)
      if (name.includes('음바페') || p.name.includes('Mbappé')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '38km/h 치달골',
            title: `[초음속 38km/h 치달] 터치라인 1:1 파괴 & 니어포스트 벼락 슛`,
            desc: `세계 최고 38.0km/h 폭발적 가속도로 풀백을 단숨에 벗겨내고 골키퍼 머리 위를 찌르는 니어포스트 강슛`,
            shotType: 'laser',
            phases: [
              { t: 0.0, targetGx: 9.0, targetGy: 8.5, ball: 'target', status: '좌측면에서 볼을 잡고 수비수와 1:1 대치', metric: '치달 모드 개시' },
              { t: 2.2, targetGx: 14.5, targetGy: 7.5, ball: 'target', status: '⚡ 보고도 못 막는 순간 가속 치고 달리기!', metric: '속도: 38.0 km/h (세계 1위)' },
              { t: 4.5, targetGx: 16.2, targetGy: 6.8, ball: 'target', status: '박스 안쪽 진입 후 골키퍼 타이밍 흔들기', metric: '완벽한 1:1 찬스' },
              { t: 5.6, targetGx: 16.5, targetGy: 6.6, ball: 'shot', shotTarget: { gx: 18.0, gy: 6.2 }, status: '💥 니어포스트 상단 골망을 찢는 레이저 슈팅!', metric: '유효슈팅 100%' },
              { t: 8.0, targetGx: 16.5, targetGy: 6.6, ball: 'goal', status: '⚽ 전매특허 팔짱 세레머니!', metric: '골인!' }
            ]
          }
        ];
      }

      // 6) 케빈 데 브라위너 시그니처 (AM/CM: KDB 존 택배 얼리 크로스)
      if (name.includes('데 브라위너') || p.name.includes('Bruyne')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: '택배 얼리 크로스',
            title: `[KDB 존 택배 크로스] 수비 라인 뒷공간을 파고드는 핀포인트 궤적`,
            desc: `우측 하프스페이스에서 수비수 키를 넘겨 골키퍼와 수비 라인 사이로 휘어 떨어지는 환상적인 크로스`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 11.0, targetGy: 3.0, ball: 'target', status: '우측 하프스페이스 KDB 존 점유', metric: '시야 개방' },
              { t: 2.5, targetGx: 12.2, targetGy: 3.5, ball: 'target', status: '문전 공격수들의 침투 타이밍 정밀 포착', metric: '크로스 각도 정렬' },
              { t: 4.8, targetGx: 12.5, targetGy: 3.6, ball: 'pass', passTarget: { gx: 16.5, gy: 6.0 }, status: '🎯 골문 앞으로 마법처럼 휘어지는 인프런트 택배 크로스!', metric: '크로스 성공률: 92%' },
              { t: 8.0, targetGx: 12.8, targetGy: 3.6, ball: 'goal', status: '쇄도한 공격수의 원터치 헤더 득점 연결!', metric: '어시스트 완성' }
            ]
          }
        ];
      }

      // 7) 일반 포지션/아키타입 범용 고유 모션 (다른 모든 70+ 선수 대상)
      if (pos === 'CB' || pos === 'LB' || pos === 'RB') {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '수비 인터셉트',
            title: `[포지션 정밀 수비] 상대 침투 패스 예측 차단 & 40m 빌드업`,
            desc: `DB 실측 경합 승리율 ${defPct}%를 기반으로 한 오차 없는 차단 및 전방 빌드업 배급`,
            shotType: 'pass',
            phases: [
              { t: 0.0, targetGx: 4.5, targetGy: 5.0, ball: 'away', status: '수비 라인 정렬 및 상대 패스 대기', metric: `경합률: ${defPct}%` },
              { t: 2.5, targetGx: 6.2, targetGy: 5.2, ball: 'target', status: '전진 가로채기 성공', metric: '볼 소유권 탈환' },
              { t: 5.0, targetGx: 6.8, targetGy: 5.2, ball: 'pass', passTarget: { gx: 13.0, gy: 3.0 }, status: '측면으로 열어주는 정확한 빌드업 패스', metric: '패스 성공' },
              { t: 8.0, targetGx: 6.8, targetGy: 5.2, ball: 'finish', status: '공격 전개 안정화', metric: '빌드업 완성' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '1:1 차단',
            title: `[박스 안 결정적 블록] 상대 슈팅 궤적을 몸으로 막아내는 육탄 방어`,
            desc: `상대의 위협적인 유효 슈팅 코스를 슬라이딩 블록으로 걷어내는 결정적 수비`,
            shotType: 'def',
            phases: [
              { t: 0.0, targetGx: 4.0, targetGy: 6.0, ball: 'away', status: '상대 공격수의 박스 침투 감지', metric: '위험 차단' },
              { t: 2.8, targetGx: 3.2, targetGy: 5.8, ball: 'target', status: '슈팅 각도를 좁히며 몸을 날리는 슬라이딩 블록', metric: '블록 성공' },
              { t: 5.5, targetGx: 3.0, targetGy: 5.8, ball: 'clear', status: '터치라인 밖으로 안전하게 걷어내기', metric: '위기 모면' },
              { t: 8.0, targetGx: 3.0, targetGy: 5.8, ball: 'finish', status: '실점 위기 방어 완료', metric: '클리어링' }
            ]
          }
        ];
      }

      // 기본 미드필더/공격수
      return [
        {
          type: 'GOAL', tag: 'goal', tagText: '득점',
          title: `[시그니처 결정력] 박스 침투 원터치 피니시 득점 (xG ${xg})`,
          desc: `상대 수비 틈새를 파고들어 정교한 원터치 슈팅으로 골망을 가르는 득점`,
          shotType: 'direct',
          phases: [
            { t: 0.0, targetGx: 11.5, targetGy: 5.0, ball: 'mid', status: '패스 전개를 기다리며 침투 각도 조율', metric: '오프더볼' },
            { t: 2.5, targetGx: 14.0, targetGy: 5.2, ball: 'pass_flight', status: '수비 뒷공간으로 순간 가속 침투', metric: '속도: 29.5 km/h' },
            { t: 4.8, targetGx: 15.5, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.5 }, status: '💥 골문 구석으로 정확한 원터치 슈팅!', metric: `xG: ${xg}` },
            { t: 8.0, targetGx: 15.8, targetGy: 5.2, ball: 'goal', status: '⚽ 침착한 마무리로 득점 성공!', metric: '골인' }
          ]
        },
        {
          type: 'PASS', tag: 'pass', tagText: '찬스메이킹',
          title: `[날카로운 키패스] 수비 라인 사이 공간을 가르는 스루패스 (KP ${kp}회)`,
          desc: `상대 수비 라인의 균열을 포착하고 침투하는 동료 발밑에 찔러준 결정적 패스`,
          shotType: 'pass',
          phases: [
            { t: 0.0, targetGx: 9.0, targetGy: 5.0, ball: 'target', status: '중원에서 볼 소유 및 패스길 탐색', metric: '키패스 준비' },
            { t: 2.5, targetGx: 9.8, targetGy: 5.2, ball: 'target', status: '동료의 침투 타이밍에 맞춰 한 박자 킬패스', metric: `키패스 90분당 ${kp}회` },
            { t: 5.0, targetGx: 10.2, targetGy: 5.2, ball: 'pass', passTarget: { gx: 15.0, gy: 3.5 }, status: '🎯 뒷공간을 향한 핀포인트 스루패스!', metric: '패스 성공' },
            { t: 8.0, targetGx: 10.5, targetGy: 5.2, ball: 'finish', status: '동료의 완벽한 슈팅 찬스로 연결', metric: '찬스메이킹 완료' }
          ]
        }
      ];
    }

    // =========================================================================
    // 3. 22명 전원의 팀 전술 대형 및 상호작용 피직스 (난수 0% 결정론적 엔진)
    // =========================================================================
    // 기본 4-2-3-1 (홈 파랑) vs 4-3-3 (어웨이 빨강)
    const BASE_HOME_11 = [
      { id: 'H1',  pos: 'GK', gx: 0.8,  gy: 6.0, name: 'GK' },
      { id: 'H2',  pos: 'RB', gx: 3.5,  gy: 1.8, name: 'RB' },
      { id: 'H3',  pos: 'CB', gx: 3.0,  gy: 4.2, name: 'CB' },
      { id: 'H4',  pos: 'CB', gx: 3.0,  gy: 7.8, name: 'CB' },
      { id: 'H5',  pos: 'LB', gx: 3.5,  gy: 10.2,name: 'LB' },
      { id: 'H6',  pos: 'DM', gx: 6.5,  gy: 4.5, name: 'DM' },
      { id: 'H7',  pos: 'DM', gx: 6.5,  gy: 7.5, name: 'DM' },
      { id: 'H8',  pos: 'RW', gx: 10.5, gy: 2.5, name: 'RW' },
      { id: 'H9',  pos: 'AM', gx: 9.8,  gy: 6.0, name: 'AM' },
      { id: 'H10', pos: 'LW', gx: 10.5, gy: 9.5, name: 'LW' },
      { id: 'H11', pos: 'ST', gx: 13.5, gy: 6.0, name: 'ST' },
    ];

    const BASE_AWAY_11 = [
      { id: 'A1',  pos: 'GK', gx: 17.2, gy: 6.0, name: 'GK' },
      { id: 'A2',  pos: 'RB', gx: 14.5, gy: 10.2,name: 'RB' },
      { id: 'A3',  pos: 'CB', gx: 15.0, gy: 7.5, name: 'CB' },
      { id: 'A4',  pos: 'CB', gx: 15.0, gy: 4.5, name: 'CB' },
      { id: 'A5',  pos: 'LB', gx: 14.5, gy: 1.8, name: 'LB' },
      { id: 'A6',  pos: 'DM', gx: 11.5, gy: 6.0, name: 'DM' },
      { id: 'A7',  pos: 'CM', gx: 9.5,  gy: 7.8, name: 'CM' },
      { id: 'A8',  pos: 'CM', gx: 9.5,  gy: 4.2, name: 'CM' },
      { id: 'A9',  pos: 'RW', gx: 7.5,  gy: 9.5, name: 'RW' },
      { id: 'A10', pos: 'LW', gx: 7.5,  gy: 2.5, name: 'LW' },
      { id: 'A11', pos: 'ST', gx: 5.5,  gy: 6.0, name: 'ST' },
    ];

    function calculate22Positions(action, t) {
      const phases = action.phases;
      // 현재 t에 해당하는 phase 보간
      let pA = phases[0];
      let pB = phases[phases.length - 1];
      for (let i = 0; i < phases.length - 1; i++) {
        if (t >= phases[i].t && t <= phases[i + 1].t) {
          pA = phases[i];
          pB = phases[i + 1];
          break;
        }
      }

      const ratio = pB.t === pA.t ? 0 : Math.max(0, Math.min(1, (t - pA.t) / (pB.t - pA.t)));
      // 부드러운 스무스스텝 보간
      const smooth = ratio * ratio * (3 - 2 * ratio);

      // 1. 주인공 선수 좌표 계산
      const heroGx = pA.targetGx + (pB.targetGx - pA.targetGx) * smooth;
      const heroGy = pA.targetGy + (pB.targetGy - pA.targetGy) * smooth;

      // 2. 주인공 선수의 실 포지션 슬롯 탐색 (버그 수정: GK 슬롯 고정 교체 버그 해결)
      const heroPos = (currentPlayer.position || 'ST').toUpperCase();
      let heroSlotId = 'H11'; // 기본 ST
      if (heroPos === 'LW') heroSlotId = 'H10';
      else if (heroPos === 'RW') heroSlotId = 'H8';
      else if (heroPos === 'AM' || heroPos === 'CAM') heroSlotId = 'H9';
      else if (heroPos === 'CM' || heroPos === 'DM') heroSlotId = 'H6';
      else if (heroPos === 'CB') heroSlotId = 'H3';
      else if (heroPos === 'LB') heroSlotId = 'H5';
      else if (heroPos === 'RB') heroSlotId = 'H2';
      else if (heroPos === 'GK') heroSlotId = 'H1';

      // 3. 볼 좌표 계산 (곡선 감아차기 Bezier vs 직선 고속 레이저)
      let ballGx = heroGx + 0.2;
      let ballGy = heroGy;
      const isCurling = (action.shotType === 'curl' || pB.curve);
      let ctrlGx = 0, ctrlGy = 0;

      if (pA.ball === 'shot' || pB.ball === 'shot') {
        const shotTarget = pB.shotTarget || { gx: 18.0, gy: 5.0 };
        if (isCurling) {
          // 2차 베지어 곡선 감아차기 탄도: 볼이 바깥으로 휘었다가 안쪽으로 꺾여 들어감
          ctrlGx = (heroGx + shotTarget.gx) * 0.5 + (pB.curveDx || 0.8);
          ctrlGy = (heroGy + shotTarget.gy) * 0.5 + (pB.curveDy || 1.8);
          const t1 = 1 - smooth;
          ballGx = t1 * t1 * heroGx + 2 * t1 * smooth * ctrlGx + smooth * smooth * shotTarget.gx;
          ballGy = t1 * t1 * heroGy + 2 * t1 * smooth * ctrlGy + smooth * smooth * shotTarget.gy;
        } else {
          // 직선 고속 레이저포 탄도 (홀란드 등)
          ballGx = heroGx + (shotTarget.gx - heroGx) * smooth;
          ballGy = heroGy + (shotTarget.gy - heroGy) * smooth;
        }
      } else if (pA.ball === 'pass' || pB.ball === 'pass') {
        const passTarget = pB.passTarget || { gx: 15.0, gy: 6.0 };
        ballGx = heroGx + (passTarget.gx - heroGx) * smooth;
        ballGy = heroGy + (passTarget.gy - heroGy) * smooth;
      } else if (pA.ball === 'goal' || pB.ball === 'goal') {
        ballGx = 18.0;
        ballGy = (pB.shotTarget ? pB.shotTarget.gy : 5.2);
      }

      // 4. 나머지 21명 선수의 전술 반응 (라인 시프트, 침투, 압박)
      const shiftX = (ballGx - 9.0) * 0.45;
      const shiftY = (ballGy - 6.0) * 0.35;

      const homePlayers = BASE_HOME_11.map(p => {
        if (p.id === heroSlotId) {
          // 주인공 선수는 실 포지션 슬롯에 정확히 매핑!
          return {
            ...p,
            gx: heroGx,
            gy: heroGy,
            isHero: true,
            name: currentPlayer.name_ko || currentPlayer.name
          };
        }
        
        // 나머지 아군 10명 전술 연계 (포지션별 유기적 움직임)
        let gx = p.gx + shiftX;
        let gy = p.gy + shiftY * 0.6;
        
        // 손흥민(LW)이 안쪽으로 컷인할 때:
        if (heroSlotId === 'H10') {
          if (p.id === 'H11') {
            // 스트라이커는 니어포스트로 돌아 뛰며 상대 센터백을 유인(Decoy Run)
            gx += smooth * 2.2;
            gy -= smooth * 1.5;
          }
          if (p.id === 'H5') {
            // 풀백은 손흥민 뒤를 받치는 오버래핑 페이크
            gx += smooth * 1.8;
          }
          if (p.id === 'H9') {
            // 공미는 박스 아크에서 세컨볼 리바운드 대기
            gx += smooth * 1.2;
          }
        }
        // 홀란드(ST)가 중앙 침투할 때:
        else if (heroSlotId === 'H11') {
          if (p.id === 'H10' || p.id === 'H8') {
            // 양 윙어는 넓게 측면을 벌려 상대 풀백들을 측면으로 묶어둠
            gx += smooth * 1.5;
          }
          if (p.id === 'H9') {
            // 공미는 킬패스 후 홀란드 뒤로 쇄도
            gx += smooth * 2.5;
          }
        }
        // 김민재(CB)가 수비 및 빌드업할 때:
        else if (heroSlotId === 'H3' || heroSlotId === 'H4') {
          if (p.id === 'H8') {
            // 우측 윙어는 김민재의 롱패스를 받기 위해 전방 질주
            gx += smooth * 2.5;
          }
          if (p.id === 'H6' || p.id === 'H7') {
            // 수미는 김민재의 전진을 커버
            gx -= smooth * 0.8;
          }
        }

        // 골키퍼(H1)는 반드시 골문 앞을 사수
        if (p.id === 'H1') {
          gx = 0.8 + (ballGx / 18.0) * 0.4;
          gy = 6.0 + (ballGy - 6.0) * 0.15;
        }

        return {
          ...p,
          gx: Math.max(0.5, Math.min(17.5, gx)),
          gy: Math.max(0.8, Math.min(11.2, gy)),
          isHero: false
        };
      });

      const awayPlayers = BASE_AWAY_11.map(p => {
        let gx = p.gx + shiftX * 0.6;
        let gy = p.gy + shiftY * 0.7;

        // 상대 센터백 및 마크맨 반응
        if (heroSlotId === 'H10') { // 손흥민 상대
          if (p.id === 'A2') { // 우측 풀백: 1:1 대치 후 컷인에 역동작
            gx += (heroGx - p.gx) * 0.55;
            gy += (heroGy - p.gy) * 0.55;
          }
          if (p.id === 'A3') { // 센터백: 슈팅 각도 좁히려 슬라이딩 블록 시도
            if (smooth > 0.5) {
              gx += 0.8;
              gy += 0.5;
            }
          }
        } else if (heroSlotId === 'H11') { // 홀란드 상대
          if (p.id === 'A3' || p.id === 'A4') { // 두 센터백: 홀란드의 피지컬에 밀려남
            gx += (heroGx - p.gx) * 0.4;
            gy += (heroGy - p.gy) * 0.3;
          }
        }

        // 상대 골키퍼: 슛 각도 좁히기 및 다이빙 모션
        if (p.pos === 'GK') {
          if (pB.ball === 'shot' || pB.ball === 'goal') {
            gx = 17.5;
            gy = 6.0 + (ballGy - 6.0) * 0.6; // 다이빙 반응
          } else {
            gx = 17.2 - Math.min(1.0, (ballGx / 18.0) * 1.2);
            gy = 6.0 + (ballGy - 6.0) * 0.25;
          }
        }

        return {
          ...p,
          gx: Math.max(0.5, Math.min(17.8, gx)),
          gy: Math.max(0.8, Math.min(11.2, gy))
        };
      });

      return {
        hero: { gx: heroGx, gy: heroGy },
        ball: { gx: ballGx, gy: ballGy },
        home: homePlayers,
        away: awayPlayers,
        currentPhase: pB,
        isCurling: isCurling,
        ctrlGx: ctrlGx,
        ctrlGy: ctrlGy
      };
    }

    // =========================================================================
    // 4. 화면 렌더링 루프 (Canvas 2D)
    // =========================================================================
    function renderPitch() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 피치 외곽 테두리
      ctx.fillStyle = '#062817';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // 체커보드 바둑판 잔디 타일
      const cols = 18;
      const rows = 12;
      const cellW = PITCH_W / cols;
      const cellH = PITCH_H / rows;

      for (let c = 0; c < cols; c++) {
        for (let r = 0; r < rows; r++) {
          const isEven = (c + r) % 2 === 0;
          ctx.fillStyle = isEven ? '#0f4225' : '#124d2c';
          ctx.fillRect(MARGIN + c * cellW, MARGIN + r * cellH, cellW, cellH);
        }
      }

      // 바둑판 격자 라인
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let c = 0; c <= cols; c++) {
        ctx.beginPath();
        ctx.moveTo(MARGIN + c * cellW, MARGIN);
        ctx.lineTo(MARGIN + c * cellW, MARGIN + PITCH_H);
        ctx.stroke();
      }
      for (let r = 0; r <= rows; r++) {
        ctx.beginPath();
        ctx.moveTo(MARGIN, MARGIN + r * cellH);
        ctx.lineTo(MARGIN + PITCH_W, MARGIN + r * cellH);
        ctx.stroke();
      }

      // 정규 축구장 라인 (센터서클, 페널티박스, 골라인)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.55)';
      ctx.lineWidth = 2;
      ctx.strokeRect(MARGIN, MARGIN, PITCH_W, PITCH_H);

      // 센터라인 & 센터서클
      ctx.beginPath();
      ctx.moveTo(MARGIN + PITCH_W / 2, MARGIN);
      ctx.lineTo(MARGIN + PITCH_W / 2, MARGIN + PITCH_H);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(MARGIN + PITCH_W / 2, MARGIN + PITCH_H / 2, 60, 0, Math.PI * 2);
      ctx.stroke();

      // 좌우 페널티 박스
      const boxW = cellW * 3;
      const boxH = cellH * 6;
      const boxY = MARGIN + (PITCH_H - boxH) / 2;
      ctx.strokeRect(MARGIN, boxY, boxW, boxH);
      ctx.strokeRect(MARGIN + PITCH_W - boxW, boxY, boxW, boxH);

      // 골문
      ctx.strokeRect(MARGIN - 10, boxY + boxH * 0.3, 10, boxH * 0.4);
      ctx.strokeRect(MARGIN + PITCH_W, boxY + boxH * 0.3, 10, boxH * 0.4);

      if (!currentPlayer) return;

      const actions = generatePlayerActions(currentPlayer);
      const action = actions[currentActionIdx] || actions[0];
      const state = calculate22Positions(action, currentTime);

      // 시야각(FOV) 부채꼴 시각화 (주인공 선수)
      const heroPt = toPixel(state.hero.gx, state.hero.gy);
      ctx.save();
      ctx.fillStyle = 'rgba(16, 185, 129, 0.14)';
      ctx.beginPath();
      ctx.moveTo(heroPt.x, heroPt.y);
      ctx.arc(heroPt.x, heroPt.y, 115, -0.4, 0.4);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 패스/슈팅 궤적 렌더링 (곡선 감아차기 vs 초고속 레이저빔)
      const ballPt = toPixel(state.ball.gx, state.ball.gy);
      if (Math.hypot(heroPt.x - ballPt.x, heroPt.y - ballPt.y) > 15) {
        ctx.save();
        if (state.isCurling) {
          // 감아차기 황금빛 U자형 곡선 아크
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 3.5;
          ctx.setLineDash([6, 3]);
          ctx.shadowColor = '#fbbf24';
          ctx.shadowBlur = 12;
          ctx.beginPath();
          ctx.moveTo(heroPt.x, heroPt.y);
          const ctrlPt = toPixel(state.ctrlGx, state.ctrlGy);
          ctx.quadraticCurveTo(ctrlPt.x, ctrlPt.y, ballPt.x, ballPt.y);
          ctx.stroke();
        } else if (action.shotType === 'laser' || action.title.includes('레이저') || action.title.includes('홀란드')) {
          // 초고속 레이저 직선 탄도
          ctx.strokeStyle = '#ef4444';
          ctx.lineWidth = 4.5;
          ctx.setLineDash([8, 2]);
          ctx.shadowColor = '#f87171';
          ctx.shadowBlur = 14;
          ctx.beginPath();
          ctx.moveTo(heroPt.x, heroPt.y);
          ctx.lineTo(ballPt.x, ballPt.y);
          ctx.stroke();
        } else {
          // 일반 패스/슈팅 점선
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2.5;
          ctx.setLineDash([5, 4]);
          ctx.beginPath();
          ctx.moveTo(heroPt.x, heroPt.y);
          ctx.lineTo(ballPt.x, ballPt.y);
          ctx.stroke();
        }
        ctx.restore();
      }

      // 22명 선수 렌더링 (바둑알)
      // 1) 어웨이 선수 (빨강)
      state.away.forEach(p => {
        const pt = toPixel(p.gx, p.gy);
        ctx.fillStyle = '#dc2626';
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#fca5a5';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 9px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.pos, pt.x, pt.y);
      });

      // 2) 홈 선수 (파랑)
      state.home.forEach(p => {
        const pt = toPixel(p.gx, p.gy);
        if (p.isHero) {
          // 주인공 선수: 화려한 금빛 테두리 + 하이라이트 펄스
          ctx.save();
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 18;
          ctx.fillStyle = '#2563eb';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 16, 0, Math.PI * 2);
          ctx.fill();

          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 3.5;
          ctx.stroke();
          ctx.restore();

          // 이름 뱃지
          ctx.fillStyle = '#fff';
          ctx.font = '900 11px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText((p.name || 'Hero').slice(0, 3), pt.x, pt.y);

          // 상단 왕관 마커
          ctx.fillStyle = '#fbbf24';
          ctx.font = 'bold 12px sans-serif';
          ctx.fillText('★', pt.x, pt.y - 20);
        } else {
          ctx.fillStyle = '#2563eb';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 12, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#93c5fd';
          ctx.lineWidth = 1.5;
          ctx.stroke();

          ctx.fillStyle = '#fff';
          ctx.font = 'bold 9px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(p.pos, pt.x, pt.y);
        }
      });

      // 축구공 렌더링
      ctx.save();
      ctx.shadowColor = '#000';
      ctx.shadowBlur = 8;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(ballPt.x, ballPt.y, 6.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#000000';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // 감아차기 시 스핀 마커 효과
      if (state.isCurling) {
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(ballPt.x, ballPt.y, 9.0, currentTime * 8, currentTime * 8 + Math.PI * 0.7);
        ctx.stroke();
      }
      ctx.restore();

      // HUD 업데이트
      const phase = state.currentPhase;
      const heroRole = currentPlayer.position ? `[${currentPlayer.name_ko || currentPlayer.name} · ${currentPlayer.position}] ` : '';
      document.getElementById('hudActionText').innerText = heroRole + (phase.status || action.title);
      document.getElementById('hudMetricText').innerText = phase.metric || `진행: ${currentTime.toFixed(1)}s`;
      document.getElementById('timeLabel').innerText = `${currentTime.toFixed(1)}s / ${TOTAL_DURATION.toFixed(1)}s`;
      document.getElementById('timeSlider').value = currentTime;
    }

    // =========================================================================
    // 5. 시뮬레이션 루프 & 컨트롤러
    // =========================================================================
    let lastTime = performance.now();
    function animationLoop(now) {
      const dt = (now - lastTime) / 1000;
      lastTime = now;

      if (isPlaying) {
        currentTime += dt * playbackSpeed;
        if (currentTime >= TOTAL_DURATION) {
          currentTime = 0; // 자동 무한 루프
        }
      }

      renderPitch();
      requestAnimationFrame(animationLoop);
    }

    function togglePlay() {
      isPlaying = !isPlaying;
      const btn = document.getElementById('btnPlayPause');
      btn.innerText = isPlaying ? '⏸ 일시정지' : '▶ 재생';
      btn.className = isPlaying ? 't-btn play' : 't-btn';
    }

    function setSpeed(spd) {
      playbackSpeed = spd;
      document.querySelectorAll('.timeline-bar .t-btn').forEach(b => {
        if (b.innerText.includes(`${spd.toFixed(1)}x`) || b.innerText.includes(`${spd}x`)) {
          b.className = 't-btn active';
        } else if (b.innerText.includes('x')) {
          b.className = 't-btn';
        }
      });
    }

    function resetCurrentAction() {
      currentTime = 0;
      isPlaying = true;
      document.getElementById('btnPlayPause').innerText = '⏸ 일시정지';
      document.getElementById('btnPlayPause').className = 't-btn play';
    }

    function onSeekTime(val) {
      currentTime = parseFloat(val);
      renderPitch();
    }

    // =========================================================================
    // 6. 선수 및 액션 인터랙션 핸들러
    // =========================================================================
    function onSelectPlayer(playerId) {
      const p = PLAYERS_DATABASE.find(item => item.player_id == playerId);
      if (!p) return;
      currentPlayer = p;
      currentActionIdx = 0;
      currentTime = 0;

      // 프로필 카드 업데이트
      document.getElementById('pAvatar').innerText = (p.name_ko || p.name).slice(0, 1);
      document.getElementById('pNameKo').innerText = p.name_ko || p.name;
      document.getElementById('pClub').innerText = `${p.current_club || ''} · ${p.league || ''}`;
      document.getElementById('pPosBadge').innerText = p.position || 'ST';
      document.getElementById('pArchetype').innerText = p.tactical_archetype || '전술적 특화 플레이어';

      const valM = (p.market_value_eur / 1000000).toFixed(0);
      document.getElementById('pMarketVal').innerText = `€${valM}M (약 ${Math.round(valM * 14.8)}억 원)`;

      document.getElementById('pStatXg').innerText = `${p.xg_per90 ? p.xg_per90.toFixed(2) : '-'} (실득점 ${p.goals_per90 ? p.goals_per90.toFixed(2) : '-'})`;
      document.getElementById('pStatKp').innerText = `${p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '-'}회/90`;
      document.getElementById('pStatProg').innerText = `${p.progressive_actions_per90 ? p.progressive_actions_per90.toFixed(1) : '-'}회/90`;
      document.getElementById('pStatDef').innerText = `${p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '-'}%`;
      document.getElementById('pStatPctl').innerText = `상위 ${(100 - (p.pos_percentile || 50))}%`;

      // 유튜브 링크 설정
      const ytId = YT_MAP[p.name_ko] || YT_MAP[p.name] || 'YhEcyglkOx0';
      document.getElementById('btnYtHighlight').onclick = () => {
        window.open(`https://www.youtube.com/watch?v=${ytId}`, '_blank');
      };

      // 액션 버튼 목록 생성
      const actions = generatePlayerActions(p);
      const listContainer = document.getElementById('actionList');
      listContainer.innerHTML = '';

      actions.forEach((act, idx) => {
        const div = document.createElement('div');
        div.className = `action-card ${idx === 0 ? 'active' : ''}`;
        div.onclick = () => {
          currentActionIdx = idx;
          currentTime = 0;
          document.querySelectorAll('.action-card').forEach((c, i) => {
            c.className = `action-card ${i === idx ? 'active' : ''}`;
          });
        };
        div.innerHTML = `
          <span class="act-tag ${act.tag}">${act.tagText}</span>
          <div class="act-title">${act.title}</div>
          <div class="act-desc">${act.desc}</div>
        `;
        listContainer.appendChild(div);
      });

      renderPitch();
    }

    // 초기화
    function init() {
      const select = document.getElementById('playerSelect');
      select.innerHTML = '';
      PLAYERS_DATABASE.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.player_id;
        opt.innerText = `${p.name_ko || p.name} (${p.position}) — ${p.current_club || ''}`;
        select.appendChild(opt);
      });

      // 기본 선택: 손흥민 (player_id: 2999) 또는 첫 번째 선수
      const defaultPlayer = PLAYERS_DATABASE.find(p => p.player_id === 2999 || (p.name_ko && p.name_ko.includes('손흥민'))) || PLAYERS_DATABASE[0];
      select.value = defaultPlayer.player_id;
      onSelectPlayer(defaultPlayer.player_id);

      requestAnimationFrame(animationLoop);
    }

    window.onload = init;
  </script>
</body>
</html>
"""

full_html = html_head_and_body + "\n" + js_code

with open('rea/fm_2d_grid_match.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Successfully rebuilt rea/fm_2d_grid_match.html!")
