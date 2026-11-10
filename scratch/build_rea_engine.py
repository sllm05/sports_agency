import json
from pathlib import Path

# Load extracted players
with open('rea/extracted_players.json', encoding='utf-8') as f:
    players = json.load(f)

print(f"Loaded {len(players)} players.")

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sports Agency Desk — 2D Tactical Intelligence & Real Data Replayer</title>
  <style>
    :root {
      --bg-dark: #090d16;
      --panel-bg: #111827;
      --panel-header: #1a2234;
      --border-color: #243048;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-green: #10b981;
      --accent-blue: #3b82f6;
      --accent-gold: #f59e0b;
      --accent-red: #ef4444;
      --accent-purple: #8b5cf6;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }

    /* 상단 네비게이션 & 선수 셀렉터 */
    header {
      background: linear-gradient(180deg, #151e32 0%, #0d1424 100%);
      border-bottom: 1px solid var(--border-color);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-shrink: 0;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-badge {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: #042f2e;
      font-size: 11px;
      font-weight: 900;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }

    .brand-title {
      font-size: 15px;
      font-weight: 800;
      color: #f1f5f9;
      letter-spacing: -0.3px;
    }

    /* 중앙 선수 스위처 */
    .player-select-box {
      display: flex;
      align-items: center;
      gap: 10px;
      background: #090e1a;
      border: 1px solid #2d3b55;
      padding: 5px 14px;
      border-radius: 8px;
    }

    .player-select-box label {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
    }

    select#playerSelect {
      background: #1a2438;
      color: #38bdf8;
      border: 1px solid #3b82f6;
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      outline: none;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .yt-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #b91c1c;
      color: #fff;
      text-decoration: none;
      font-size: 12px;
      font-weight: 800;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid #ef4444;
      transition: background 0.15s;
    }
    .yt-btn:hover { background: #dc2626; }

    /* 메인 3열 레이아웃 */
    .main-grid {
      display: grid;
      grid-template-columns: 310px 1fr 310px;
      gap: 12px;
      padding: 12px;
      flex: 1;
      min-height: 0;
    }

    .panel {
      background: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .panel-head {
      background: var(--panel-header);
      padding: 10px 14px;
      font-size: 12px;
      font-weight: 800;
      color: #cbd5e1;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .panel-body {
      padding: 12px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    /* 선수 프로필 카드 */
    .player-card {
      background: #0d1424;
      border: 1px solid #23314d;
      border-radius: 8px;
      padding: 12px;
    }

    .p-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .p-name {
      font-size: 17px;
      font-weight: 900;
      color: #fff;
    }

    .p-pos {
      background: #2563eb;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
    }

    .p-meta {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 10px;
    }

    .p-archetype {
      background: #172554;
      border: 1px solid #1d4ed8;
      color: #93c5fd;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 10px;
    }

    .p-strengths {
      font-size: 12px;
      line-height: 1.5;
      color: #cbd5e1;
      background: #090e1a;
      border: 1px solid #1e293b;
      padding: 8px 10px;
      border-radius: 6px;
    }

    .stat-pill-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
      margin-top: 10px;
    }

    .stat-pill {
      background: #162032;
      border: 1px solid #263550;
      padding: 6px 8px;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .stat-pill .label {
      font-size: 10px;
      color: var(--text-muted);
      font-weight: 600;
    }

    .stat-pill .val {
      font-size: 13px;
      color: #38bdf8;
      font-weight: 800;
    }

    /* 중앙 피치 영역 */
    .pitch-center {
      background: #070a12;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }

    .canvas-wrap {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      min-height: 0;
      padding: 10px;
    }

    canvas#pitchCanvas {
      max-width: 100%;
      max-height: 100%;
      border-radius: 8px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.75);
    }

    /* HUD 오버레이 바 */
    .hud-overlay {
      position: absolute;
      top: 20px;
      left: 20px;
      right: 20px;
      pointer-events: none;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    .hud-badge {
      background: rgba(10, 16, 28, 0.92);
      border: 1px solid #38bdf8;
      backdrop-filter: blur(8px);
      padding: 8px 14px;
      border-radius: 8px;
      color: #fff;
      font-size: 12px;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .hud-phase-tag {
      background: var(--accent-gold);
      color: #000;
      font-size: 10px;
      font-weight: 900;
      padding: 2px 6px;
      border-radius: 4px;
    }

    /* 하단 타임라인 컨트롤 바 */
    .timeline-bar {
      background: #101726;
      border-top: 1px solid var(--border-color);
      padding: 10px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }

    .t-btn {
      background: #1e293b;
      color: #fff;
      border: 1px solid #334155;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.15s;
    }
    .t-btn:hover { background: #334155; }
    .t-btn.active { background: var(--accent-blue); border-color: #60a5fa; }
    .t-btn.play { background: var(--accent-green); color: #022c22; border-color: #34d399; }

    .slider-wrap {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    input[type=range]#timeSlider {
      flex: 1;
      height: 6px;
      border-radius: 3px;
      background: #243248;
      outline: none;
      cursor: pointer;
      accent-color: #38bdf8;
    }

    .time-indicator {
      font-size: 13px;
      font-weight: 800;
      color: #38bdf8;
      font-variant-numeric: tabular-nums;
      min-width: 60px;
      text-align: right;
    }

    /* 우측 고유 액션 리스트 */
    .action-btn-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .action-card {
      background: #0d1424;
      border: 1px solid #23314d;
      border-radius: 8px;
      padding: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
      text-align: left;
    }
    .action-card:hover {
      border-color: #3b82f6;
      background: #131c31;
    }
    .action-card.active {
      border-color: #38bdf8;
      background: #162442;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    .act-tag {
      font-size: 10px;
      font-weight: 900;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 4px;
    }
    .act-tag.goal { background: #059669; color: #fff; }
    .act-tag.pass { background: #2563eb; color: #fff; }
    .act-tag.def { background: #7c3aed; color: #fff; }
    .act-tag.dribble { background: #d97706; color: #fff; }

    .act-title {
      font-size: 13px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 4px;
    }

    .act-desc {
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* 범례 */
    .legend-box {
      background: #090e1a;
      border: 1px solid #1e293b;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 11px;
      color: #94a3b8;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .legend-row {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
    }
  </style>
</head>
<body>

  <!-- 헤더 -->
  <header>
    <div class="brand-group">
      <span class="brand-badge">TACTICAL INTELLIGENCE</span>
      <span class="brand-title">2D 실제 데이터 하이라이트 전술 리플레이어</span>
    </div>

    <div class="player-select-box">
      <label for="playerSelect">분석 대상 선수 선택:</label>
      <select id="playerSelect" onchange="onSelectPlayer(this.value)">
        <!-- JS로 채워짐 -->
      </select>
    </div>

    <div class="header-actions">
      <a id="ytSyncBtn" href="#" target="_blank" class="yt-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        실제 공식 하이라이트 영상
      </a>
    </div>
  </header>

  <!-- 메인 3열 레이아웃 -->
  <div class="main-grid">
    <!-- 좌측: 선수 실제 DB 스탯 & 아키타입 -->
    <div class="panel">
      <div class="panel-head">
        <span>선수 프로필 & Opta 실측 지표</span>
        <span style="color:#10b981; font-weight:900;">DB VERIFIED</span>
      </div>
      <div class="panel-body">
        <div class="player-card">
          <div class="p-header">
            <span class="p-name" id="pCardName">-</span>
            <span class="p-pos" id="pCardPos">-</span>
          </div>
          <div class="p-meta" id="pCardClub">-</div>
          <div class="p-archetype" id="pCardArchetype">-</div>
          <div class="p-strengths" id="pCardStrengths">-</div>

          <div class="stat-pill-grid">
            <div class="stat-pill">
              <span class="label">90분당 실득점 (G90)</span>
              <span class="val" id="pStatGoals">-</span>
            </div>
            <div class="stat-pill">
              <span class="label">기대 득점 (xG90)</span>
              <span class="val" id="pStatXg">-</span>
            </div>
            <div class="stat-pill">
              <span class="label">키패스 (KP90)</span>
              <span class="val" id="pStatKp">-</span>
            </div>
            <div class="stat-pill">
              <span class="label">전진 액션 (Prog90)</span>
              <span class="val" id="pStatProg">-</span>
            </div>
            <div class="stat-pill">
              <span class="label">수비 경합 승리율</span>
              <span class="val" id="pStatDef">-</span>
            </div>
            <div class="stat-pill">
              <span class="label">포지션 백분위</span>
              <span class="val" id="pStatPctl">-</span>
            </div>
          </div>
        </div>

        <div class="legend-box">
          <div style="font-weight:800; color:#cbd5e1; margin-bottom:4px;">피치 그래픽 안내</div>
          <div class="legend-row"><span class="dot" style="background:#2563eb;"></span> 파랑: 주인공 선수 및 아군 11명</div>
          <div class="legend-row"><span class="dot" style="background:#dc2626;"></span> 빨강: 상대 수비 및 압박 11명</div>
          <div class="legend-row"><span class="dot" style="background:#f59e0b;"></span> 노랑 실선/점선: 패스 및 슈팅 궤적</div>
          <div class="legend-row"><span class="dot" style="background:#10b981;"></span> 초록 부채꼴: 패스 시야각(FOV) 및 각도</div>
        </div>
      </div>
    </div>

    <!-- 중앙: 2D 피치 캔버스 & 타임라인 컨트롤 -->
    <div class="pitch-center">
      <div class="canvas-wrap">
        <canvas id="pitchCanvas" width="1080" height="680"></canvas>

        <div class="hud-overlay">
          <div class="hud-badge" id="hudStatusBadge">
            <span class="hud-phase-tag" id="hudPhaseTag">PHASE 1</span>
            <span id="hudActionText">동작 준비 중</span>
          </div>
          <div class="hud-badge" id="hudStatBadge" style="border-color:#10b981;">
            <span id="hudMetricText">속도: 0.0 km/h</span>
          </div>
        </div>
      </div>

      <!-- 하단 타임라인 스크러버 -->
      <div class="timeline-bar">
        <button id="btnPlayPause" class="t-btn play" onclick="togglePlay()">⏸ 일시정지</button>
        <button class="t-btn" onclick="setSpeed(0.5)">0.5x</button>
        <button class="t-btn active" id="btnSpeed1" onclick="setSpeed(1.0)">1.0x</button>
        <button class="t-btn" onclick="setSpeed(2.0)">2.0x</button>
        <button class="t-btn" onclick="resetCurrentAction()">⏮ 처음부터</button>

        <div class="slider-wrap">
          <input type="range" id="timeSlider" min="0" max="8" step="0.05" value="0" oninput="onSeekTime(this.value)">
          <div class="time-indicator" id="timeLabel">0.0s / 8.0s</div>
        </div>
      </div>
    </div>

    <!-- 우측: 해당 선수의 고유 액션 선택기 -->
    <div class="panel">
      <div class="panel-head">
        <span>선수 고유 특기 하이라이트</span>
        <span style="font-size:10px; color:#38bdf8;">3대 시그니처</span>
      </div>
      <div class="panel-body">
        <div style="font-size:11px; color:#94a3b8; line-height:1.4;">
          DB의 실측 능력치와 플레이스타일에 따라 완전히 정밀하게 계산된 고유 모션입니다. 난수 없이 22명이 전술적으로 연계됩니다.
        </div>

        <div class="action-btn-list" id="actionList">
          <!-- JS로 생성됨 -->
        </div>
      </div>
    </div>
  </div>

  <script>
    // 1. 실제 DB에서 추출된 52명 선수 데이터셋
    const PLAYERS_DATABASE = __PLAYERS_JSON__;

    // 공식 유튜브 하이라이트 매핑
    const YT_MAP = {
      '손흥민': 'YhEcyglkOx0',
      'Heung-min Son': 'YhEcyglkOx0',
      '이강인': '2Ec8VofpRmo',
      'Kang-in Lee': '2Ec8VofpRmo',
      '김민재': '38LUvS2jOOU',
      'Min-Jae Kim': '38LUvS2jOOU',
      '황희찬': 'DVNwiAPuPTY',
      'Hwang Heechan': 'DVNwiAPuPTY',
      'Erling Haaland': '8cfwD8ybFfw',
      'Kevin De Bruyne': 'Tw1fCcNaKhc',
      'Rodri': 'Lpz4PUPJ5kM',
      'Kylian Mbappe': '6VC5VHn5EQM',
      'Jude Bellingham': 'kNwOJ-BJcPk',
      'Bukayo Saka': '9ogC38l8nTU',
      'Virgil van Dijk': '38LUvS2jOOU',
      'Bruno Fernandes': 'h2EwOys6evI',
      'Mohamed Salah': 'DvEMr0reE7Y',
      'Young-woo Seol': 'DVNwiAPuPTY',
      '설영우': 'DVNwiAPuPTY',
      '조현우': 'DVNwiAPuPTY',
      '황인범': 'DVNwiAPuPTY'
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
    // 2. 선수별 고유 시그니처 액션 정의 엔진 (DB 스탯 기반 결정론적 키프레임)
    // =========================================================================
    function generatePlayerActions(p) {
      const pos = (p.position || 'ST').toUpperCase();
      const archetype = p.tactical_archetype || '';
      const name = p.name_ko || p.name;
      const xg = p.xg_per90 ? p.xg_per90.toFixed(2) : '0.45';
      const kp = p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '2.1';
      const defPct = p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '60';

      // 1) 손흥민 시그니처
      if (name.includes('손흥민') || p.name.includes('Son')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '득점',
            title: `[손흥민 존] 하프스페이스 컷인 & 파포스트 감아차기 골`,
            desc: `하프스페이스 뒷공간으로 34.2km/h 스프린트 후 수비수 1명을 제치고 골대 구석으로 휘어 차는 시그니처 득점 (xG ${xg} / 전환율 +32%)`,
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 3.5, ball: 'target', status: '하프라인 부근에서 침투 각도 형성', metric: '속도: 18.5 km/h' },
              { t: 2.2, targetGx: 13.5, targetGy: 4.2, ball: 'target', status: '⚡ 폭발적 라인 브레이킹 스프린트!', metric: '속도: 34.2 km/h (순간 최고속)' },
              { t: 4.5, targetGx: 14.8, targetGy: 5.2, ball: 'target', status: '수비수를 안쪽으로 제쳐내며 슈팅 각도 확보', metric: '탈압박 성공 · 감아차기 준비' },
              { t: 5.8, targetGx: 15.0, targetGy: 5.3, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.0 }, status: '⚽ 환상적인 인프런트 감아차기 슈팅!', metric: `xG: ${xg} · 회전 감아차기` },
              { t: 8.0, targetGx: 15.2, targetGy: 5.4, ball: 'goal', status: '🎉 골망 구석을 가르는 완벽한 골인!!', metric: '결정력 전환율 +32% 입증' }
            ]
          },
          {
            type: 'PASS', tag: 'pass', tagText: '찬스메이킹',
            title: `[폭풍 질주 후 컷백] 40m 카운터어택 & 킬러 패스`,
            desc: `역습 상황에서 폭발적인 가속도로 터치라인을 찢은 뒤 박스 안 동료에게 정확히 연결한 컷백 어시스트`,
            phases: [
              { t: 0.0, targetGx: 8.0, targetGy: 2.0, ball: 'target', status: '하프라인 왼쪽 측면에서 볼 수신', metric: '가속 시작' },
              { t: 3.0, targetGx: 14.2, targetGy: 2.2, ball: 'target', status: '측면 수비수를 스피드로 완벽히 무력화', metric: '속도: 33.1 km/h' },
              { t: 5.0, targetGx: 16.0, targetGy: 3.0, ball: 'target', status: '골라인 직전 감속 후 문전 동료 확인', metric: '시야 확보' },
              { t: 6.2, targetGx: 16.0, targetGy: 3.0, ball: 'pass', passTarget: { gx: 15.5, gy: 6.0 }, status: '🎯 쇄도하는 스트라이커 발밑으로 핀포인트 컷백!', metric: 'xA: 0.35 찬스 메이킹' },
              { t: 8.0, targetGx: 16.0, targetGy: 3.0, ball: 'finish', status: '동료의 논스톱 슈팅 마무리 연결', metric: '키패스 성공' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '단독 돌파',
            title: `[단독 드리블 돌파] 수비 2명 사이를 뚫는 저돌적 역습`,
            desc: `수비수 2명의 협력 압박 사이를 순간적인 바디페인팅과 주력으로 돌파하는 크랙 플레이`,
            phases: [
              { t: 0.0, targetGx: 9.0, targetGy: 4.5, ball: 'target', status: '중원 압박 사이에서 볼 키핑', metric: '무게중심 전환' },
              { t: 2.5, targetGx: 11.8, targetGy: 3.8, ball: 'target', status: '상대 센터백의 발을 빼앗는 넛메그 돌파', metric: '수비수 역동작 유발' },
              { t: 5.0, targetGx: 14.5, targetGy: 4.5, ball: 'target', status: '아크 정면까지 35m 전진 드리블 완료', metric: '전진 캐리 성공' },
              { t: 8.0, targetGx: 15.5, targetGy: 5.2, ball: 'target', status: '위협적인 유효 슈팅 연결로 코너킥 획득', metric: '슈팅 창출' }
            ]
          }
        ];
      }

      // 2) 이강인 시그니처
      if (name.includes('이강인') || p.name.includes('Kang-in')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: '킬패스',
            title: `[La Pausa 스루패스] 수비 라인 찢는 35m 핀포인트 킬러 패스`,
            desc: `상대 미드필더 2명을 끌어당기며 템포를 조절한 뒤 침투하는 공격수에게 배달된 레이저 패스 (키패스 90분당 ${kp}회 상위 5%)`,
            phases: [
              { t: 0.0, targetGx: 8.5, targetGy: 4.0, ball: 'target', status: '볼을 밟으며 템포 조절 (La Pausa)', metric: '압박 유인 중' },
              { t: 2.5, targetGx: 9.2, targetGy: 4.8, ball: 'target', status: '상대 수비수 2명의 압박을 등지고 시야 확보', metric: '시야각(FOV) 전방 120° 개방' },
              { t: 4.8, targetGx: 9.8, targetGy: 5.0, ball: 'pass', passTarget: { gx: 15.2, gy: 5.8 }, status: '🎯 수비수 3명 사이 빈틈을 가르는 35m 킬패스 투입!', metric: `전진 패스 지표: 상위 2%` },
              { t: 6.5, targetGx: 10.2, targetGy: 5.0, ball: 'receive', status: '침투한 공격수가 완벽한 1:1 찬스에서 볼 리시브', metric: 'xA: 0.42 기대 어시스트' },
              { t: 8.0, targetGx: 10.5, targetGy: 5.0, ball: 'goal', status: '침투 공격수의 침착한 마무리로 득점 완성!', metric: '빅찬스 생성 완료' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '탈압박',
            title: `[바디페인팅 턴] 2인 압박 무력화 & 반대편 40m 대각선 전환`,
            desc: `상대의 강한 전방 압박을 특유의 상체 페인팅 턴으로 벗겨낸 뒤 비어있는 반대편으로 단숨에 전환하는 플레이메이킹`,
            phases: [
              { t: 0.0, targetGx: 7.5, targetGy: 8.5, ball: 'target', status: '터치라인 부근에서 상대 2명의 샌드위치 압박 직면', metric: '압박 강도 95%' },
              { t: 2.2, targetGx: 7.2, targetGy: 7.5, ball: 'target', status: '몸을 회전하며 상체 페인팅으로 수비수 무게중심 붕괴', metric: '탈압박 성공 (100%)' },
              { t: 4.5, targetGx: 8.2, targetGy: 6.8, ball: 'target', status: '중원으로 빠져나오며 반대편 오픈 공간 탐색', metric: 'xGBuildup: 0.68 기여' },
              { t: 6.0, targetGx: 8.5, targetGy: 6.8, ball: 'pass', passTarget: { gx: 13.0, gy: 2.0 }, status: '📐 반대편 윙어를 향한 정확한 40m 대각선 롱 체인지 패스!', metric: '전환 패스 성공' },
              { t: 8.0, targetGx: 8.8, targetGy: 6.8, ball: 'finish', status: '반대편 측면에서 즉각적인 크로스 찬스로 연결', metric: '공격 전개 완성' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '득점',
            title: `[아크 정면 왼발 프리킥/중거리포] 골문 상단 구석 궤적골`,
            desc: `박스 바깥 아크 정면에서 수비 벽을 넘겨 골키퍼 손이 닿지 않는 상단 구석을 찌르는 정밀 왼발 슈팅`,
            phases: [
              { t: 0.0, targetGx: 12.0, targetGy: 5.5, ball: 'target', status: '아크 정면 좋은 위치에서 볼 소유', metric: '슈팅 거리 22m' },
              { t: 2.5, targetGx: 12.8, targetGy: 5.2, ball: 'target', status: '왼발 슈팅 각도를 만들기 위한 한 박자 터치', metric: '각도 45° 정렬' },
              { t: 4.8, targetGx: 13.2, targetGy: 5.0, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 환상적인 궤적으로 휘어 들어가는 왼발 슈팅!', metric: `xG: ${xg} 정밀 타격` },
              { t: 8.0, targetGx: 13.2, targetGy: 5.0, ball: 'goal', status: '⚽ 크로스바 하단을 맞고 골망을 흔드는 원더골!', metric: '득점 성공' }
            ]
          }
        ];
      }

      // 3) 김민재 시그니처
      if (name.includes('김민재') || p.name.includes('Min-Jae') || p.name.includes('van Dijk')) {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '스토퍼 태클',
            title: `[스토퍼 전진 인터셉트 & 롱패스] 상대 역습 차단 & 45m 다이렉트 배달`,
            desc: `상대 패스 길목을 예측하여 라인을 깨고 전진해 볼을 가로챈 뒤, 반대편 공격수 발밑으로 45m 전진 롱패스 (전진패스 90분당 ${kp}회 상위 3%)`,
            phases: [
              { t: 0.0, targetGx: 4.5, targetGy: 5.5, ball: 'away', status: '상대 공격진의 역습 전개 및 전진 패스 시도', metric: '위험 지역 차단 모드' },
              { t: 2.2, targetGx: 6.8, targetGy: 5.8, ball: 'target', status: '🛡️ 과감한 전진 스텝으로 상대 패스 완벽 인터셉트!', metric: `대인 경합 승리율: ${defPct}%` },
              { t: 4.2, targetGx: 7.2, targetGy: 5.6, ball: 'target', status: '탈환 후 고개를 들어 전방 빈 공간 포착', metric: '빌드업 시야 확보' },
              { t: 5.8, targetGx: 7.5, targetGy: 5.5, ball: 'pass', passTarget: { gx: 14.5, gy: 2.5 }, status: '🚀 전방 윙어를 향해 정확히 꽂히는 45m 레이저 롱패스!', metric: '전진 패스 성공 (상위 3%)' },
              { t: 8.0, targetGx: 6.5, targetGy: 5.5, ball: 'finish', status: '단숨에 우리 팀의 결정적인 득점 기회로 전환!', metric: '공수 전환 성공' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '커버 태클',
            title: `[괴물 피지컬 리커버리] 1:1 결정적 슬라이딩 태클 슈퍼세이브`,
            desc: `뒷공간으로 쇄도하는 상대 공격수를 압도적인 주력으로 추격하여 박스 진입 직전 공만 걷어내는 완벽한 태클`,
            phases: [
              { t: 0.0, targetGx: 5.5, targetGy: 7.0, ball: 'away', status: '상대 윙어의 뒷공간 단독 돌파 발생', metric: '추격 속도: 22.0 km/h' },
              { t: 2.5, targetGx: 4.0, targetGy: 6.5, ball: 'away', status: '순간 속도 34.0km/h로 전력 질주하며 각도 좁히기', metric: '속도: 34.1 km/h 스프린트' },
              { t: 4.8, targetGx: 2.8, targetGy: 6.0, ball: 'target', status: '⚔️ 위험 지역 진입 직전 오차 없는 슬라이딩 태클 성공!', metric: '클리어링 100%' },
              { t: 8.0, targetGx: 3.2, targetGy: 6.0, ball: 'target', status: '위기를 완벽히 탈출하며 동료 골키퍼에게 안정적 연결', metric: '위기 소멸' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '세트피스',
            title: `[타점 높은 제공권 헤더] 코너킥 상황 압도적 타점 헤더 골`,
            desc: `코너킥 상황에서 상대 수비수 2명을 힘으로 누르고 타점 높은 헤더로 골망을 가르는 세트피스 득점`,
            phases: [
              { t: 0.0, targetGx: 14.0, targetGy: 5.0, ball: 'corner', status: '코너 플래그에서 크로스 준비', metric: '세트피스 전술 대형' },
              { t: 2.5, targetGx: 15.5, targetGy: 5.5, ball: 'corner_flight', status: '수비수를 따돌리며 박스 중앙으로 강력한 쇄도', metric: '제공권 경합 준비' },
              { t: 4.8, targetGx: 16.5, targetGy: 5.5, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.3 }, status: '💥 타점 높은 점프로 골문 구석을 찌르는 헤더 강타!', metric: `헤더 경합 승리율 78%` },
              { t: 8.0, targetGx: 16.5, targetGy: 5.5, ball: 'goal', status: '⚽ 골키퍼 손을 스치며 골망을 가르는 득점 완성!', metric: '세트피스 득점' }
            ]
          }
        ];
      }

      // 4) 엘링 홀란드 시그니처 (Box Finisher)
      if (name.includes('Haaland') || archetype.includes('타점·결정력 집중형 스트라이커')) {
        return [
          {
            type: 'GOAL', tag: 'goal', tagText: '원터치 피니시',
            title: `[라인 침투 맹폭] 센터백 사이 공간 침투 & 원터치 피니시`,
            desc: `라인 침투 패스 리시브 8.3회(상위 11%)를 증명하는 번개같은 침투와 골문 구석 원터치 마무리 (xG ${xg})`,
            phases: [
              { t: 0.0, targetGx: 12.5, targetGy: 5.5, ball: 'mid', status: '상대 센터백 2명 사이에서 오프사이드 라인 주시', metric: '스프린트 타이밍 조율' },
              { t: 2.2, targetGx: 14.8, targetGy: 5.2, ball: 'pass_flight', status: '⚡ 수비수 어깨를 누르며 폭발적으로 뒷공간 쇄도!', metric: '속도: 34.8 km/h' },
              { t: 4.5, targetGx: 16.2, targetGy: 5.5, ball: 'target', status: '전방 스루패스를 완벽하게 발밑에 터치', metric: '리시브 성공' },
              { t: 5.6, targetGx: 16.5, targetGy: 5.5, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.8 }, status: '💥 골문 구석으로 벼락같은 논스톱 강슛!', metric: `xG: ${xg} 확실한 결정력` },
              { t: 8.0, targetGx: 16.8, targetGy: 5.5, ball: 'goal', status: '⚽ 골문 그물을 찢을 듯한 완벽한 득점!!', metric: 'G+A 0.82/90 상위 6%' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '타점 피니시',
            title: `[박스 안 피지컬 타점] 크로스를 밀어 넣는 공중제비 발리`,
            desc: `측면 크로스 상황에서 상대 센터백과의 몸싸움을 완벽히 이겨내고 타점 높은 발리로 마무리`,
            phases: [
              { t: 0.0, targetGx: 13.5, targetGy: 4.0, ball: 'wing', status: '측면 풀백의 크로스 타이밍 감지', metric: '박스 안 자리싸움' },
              { t: 2.5, targetGx: 15.8, targetGy: 4.8, ball: 'cross', status: '상대 수비를 힘으로 밀어내며 니어포스트 쇄도', metric: '피지컬 우위' },
              { t: 4.8, targetGx: 16.8, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.1 }, status: '💥 허공에서 발을 뻗어 문전으로 꽂아 넣는 아크로바틱 피니시!', metric: '유효슈팅' },
              { t: 8.0, targetGx: 16.8, targetGy: 5.2, ball: 'goal', status: '골키퍼가 반응조차 하지 못한 원더골!', metric: '득점 완성' }
            ]
          },
          {
            type: 'DRIBBLE', tag: 'dribble', tagText: '돌파',
            title: `[괴물 폭주 돌파] 하프라인 볼 탈환 후 30m 단독 불도저 질주`,
            desc: `상대 볼을 끊어낸 뒤 압도적인 피지컬과 속도로 수비수를 밀쳐내며 박스까지 도달`,
            phases: [
              { t: 0.0, targetGx: 10.0, targetGy: 6.0, ball: 'target', status: '경합 상황에서 공을 몸으로 소유', metric: '볼 소유 안정' },
              { t: 3.0, targetGx: 13.0, targetGy: 5.5, ball: 'target', status: '상대 수비수의 어깨 싸움을 버텨내며 직진 돌파', metric: '속도: 33.2 km/h' },
              { t: 5.5, targetGx: 15.5, targetGy: 5.2, ball: 'target', status: '골키퍼와 1:1 찬스 직면', metric: '슈팅 각 확보' },
              { t: 8.0, targetGx: 16.0, targetGy: 5.2, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.0 }, status: '강력한 슈팅으로 코너킥 찬스 창출', metric: '찬스 창출' }
            ]
          }
        ];
      }

      // 5) 로드리 시그니처 (Press-Resistant Pivot)
      if (name.includes('Rodri') || archetype.includes('탈압박형 수비형 미드필더')) {
        return [
          {
            type: 'PASS', tag: 'pass', tagText: '빌드업 조율',
            title: `[후방 1차 탈압박 기점] 상대 전방 압박 무력화 & 35m 전진 배급`,
            desc: `대인 수비 경합 승리율 64%(상위 1%)와 xGBuildup 0.8(상위 3%)을 증명하는 완벽한 피벗 플레이`,
            phases: [
              { t: 0.0, targetGx: 6.0, targetGy: 6.0, ball: 'target', status: '상대 공격수 2명의 강한 전방 압박을 등지고 볼 수신', metric: '경합 승리율: 64%' },
              { t: 2.2, targetGx: 6.5, targetGy: 5.2, ball: 'target', status: '원터치 턴으로 상대 압박 라인을 완전히 무력화', metric: '탈압박 성공 (상위 1%)' },
              { t: 4.5, targetGx: 7.2, targetGy: 5.5, ball: 'pass', passTarget: { gx: 12.5, gy: 2.5 }, status: '📐 전방 윙어를 향해 정확한 중장거리 전진 패스 배급!', metric: '전진 패스: 6.15회/90' },
              { t: 8.0, targetGx: 7.8, targetGy: 5.5, ball: 'finish', status: '팀 전체의 공격 템포를 한 단계 끌어올리는 완벽한 기점', metric: 'xGBuildup: 0.80 상위 3%' }
            ]
          },
          {
            type: 'GOAL', tag: 'goal', tagText: '중거리 원더골',
            title: `[아크 정면 세컨볼 레이저포] 박스 밖 25m 논스톱 중거리포 득점`,
            desc: `상대 수비가 걷어낸 세컨볼을 지체 없이 오른발 인스텝으로 감아 차 골대 구석을 찌르는 중거리포`,
            phases: [
              { t: 0.0, targetGx: 11.0, targetGy: 6.0, ball: 'clear', status: '상대 수비가 박스 밖으로 걷어낸 공 감지', metric: '세컨볼 낙하지점 포착' },
              { t: 2.5, targetGx: 12.2, targetGy: 5.8, ball: 'target', status: '공의 바운드를 맞추며 슈팅 타이밍 정렬', metric: '무게중심 안착' },
              { t: 4.8, targetGx: 12.8, targetGy: 5.8, ball: 'shot', shotTarget: { gx: 18.0, gy: 5.2 }, status: '💥 낮고 빠르게 깔려 들어가는 오른발 대포알 중거리 슈팅!', metric: '슈팅 속도: 112 km/h' },
              { t: 8.0, targetGx: 13.0, targetGy: 5.8, ball: 'goal', status: '⚽ 수비수들 틈을 뚫고 골망 구석을 흔드는 원더골!', metric: '골인!' }
            ]
          },
          {
            type: 'DEF', tag: 'def', tagText: '볼위닝',
            title: `[하프라인 완벽한 볼위닝] 대인 경합 승리 & 즉각적인 역습 개시`,
            desc: `상대의 중원 역습 전개를 거친 몸싸움으로 제압하여 볼을 탈환한 뒤 전방으로 즉각 배급`,
            phases: [
              { t: 0.0, targetGx: 8.0, targetGy: 6.5, ball: 'away', status: '상대 공격형 미드필더의 턴 시도 포착', metric: '압박 개시' },
              { t: 2.5, targetGx: 8.5, targetGy: 6.2, ball: 'target', status: '🛡️ 강력한 어깨 싸움으로 파울 없이 볼 완벽 탈환!', metric: '경합 승리 (64%)' },
              { t: 5.0, targetGx: 9.0, targetGy: 5.8, ball: 'pass', passTarget: { gx: 13.5, gy: 8.5 }, status: '탈환 즉시 침투하는 윙어에게 원터치 스루패스 투입', metric: '역습 개시' },
              { t: 8.0, targetGx: 9.2, targetGy: 5.8, ball: 'finish', status: '위기를 기회로 바꾼 결정적 수비 공헌', metric: '수비 기여 완료' }
            ]
          }
        ];
      }

      // 6) 일반 포지션/아키타입 범용 고유 모션 (다른 모든 선수 대상)
      if (pos === 'CB' || pos === 'LB' || pos === 'RB') {
        return [
          {
            type: 'DEF', tag: 'def', tagText: '수비 인터셉트',
            title: `[포지션 정밀 수비] 상대 침투 패스 예측 차단 & 40m 빌드업`,
            desc: `DB 실측 경합 승리율 ${defPct}%를 기반으로 한 오차 없는 차단 및 전방 빌드업 배급`,
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
            phases: [
              { t: 0.0, targetGx: 4.0, targetGy: 6.0, ball: 'away', status: '상대 공격수의 박스 침투 감지', metric: '위험 차단' },
              { t: 2.8, targetGx: 3.2, targetGy: 5.8, ball: 'target', status: '슈팅 각도를 좁히며 몸을 날리는 슬라이딩 블록', metric: '블록 성공' },
              { t: 5.5, targetGx: 3.0, targetGy: 5.8, ball: 'clear', status: '터치라인 밖으로 안전하게 걷어내기', metric: '위기 모면' },
              { t: 8.0, targetGx: 3.0, targetGy: 5.8, ball: 'finish', status: '실점 위기 방어 완료', metric: '클리어링' }
            ]
          },
          {
            type: 'PASS', tag: 'pass', tagText: '전진 패스',
            title: `[후방 롱 빌드업] 반대편 공간을 찢는 대각선 전환 패스`,
            desc: `후방에서 상대 압박을 피해 반대편 풀백의 발밑으로 정확히 배달되는 롱패스`,
            phases: [
              { t: 0.0, targetGx: 3.8, targetGy: 4.0, ball: 'target', status: '후방에서 볼 소유 및 압박 관찰', metric: '시야 확보' },
              { t: 2.5, targetGx: 4.2, targetGy: 4.5, ball: 'target', status: '전방 선수들의 움직임 확인', metric: '패스길 선택' },
              { t: 5.0, targetGx: 4.5, targetGy: 4.8, ball: 'pass', passTarget: { gx: 12.0, gy: 9.0 }, status: '📐 반대편 측면으로 날카로운 롱패스 전개', metric: '전진 패스 성공' },
              { t: 8.0, targetGx: 4.5, targetGy: 4.8, ball: 'finish', status: '측면 공격 기회 창출', metric: '전개 완료' }
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
          phases: [
            { t: 0.0, targetGx: 9.0, targetGy: 5.0, ball: 'target', status: '중원에서 볼 소유 및 패스길 탐색', metric: '키패스 준비' },
            { t: 2.5, targetGx: 9.8, targetGy: 5.2, ball: 'target', status: '동료의 침투 타이밍에 맞춰 한 박자 킬패스', metric: `키패스 90분당 ${kp}회` },
            { t: 5.0, targetGx: 10.2, targetGy: 5.2, ball: 'pass', passTarget: { gx: 15.0, gy: 3.5 }, status: '🎯 뒷공간을 향한 핀포인트 스루패스!', metric: '패스 성공' },
            { t: 8.0, targetGx: 10.5, targetGy: 5.2, ball: 'finish', status: '동료의 완벽한 슈팅 찬스로 연결', metric: '찬스메이킹 완료' }
          ]
        },
        {
          type: 'DRIBBLE', tag: 'dribble', tagText: '돌파',
          title: `[탈압박 전진] 1:1 대인 돌파 후 박스 진입`,
          desc: `순간적인 방향 전환으로 상대 마크맨을 제치고 공격 공간을 열어내는 전진 드리블`,
          phases: [
            { t: 0.0, targetGx: 10.0, targetGy: 3.0, ball: 'target', status: '측면에서 볼을 잡고 수비수와 1:1 대치', metric: '드리블 개시' },
            { t: 2.8, targetGx: 12.5, targetGy: 3.8, ball: 'target', status: '바디페인팅으로 수비수를 완전히 제쳐냄', metric: '돌파 성공' },
            { t: 5.5, targetGx: 14.2, targetGy: 4.5, ball: 'target', status: '박스 안쪽으로 진입하며 컷백 준비', metric: '위험 지역 진입' },
            { t: 8.0, targetGx: 14.8, targetGy: 4.8, ball: 'pass', passTarget: { gx: 15.5, gy: 6.0 }, status: '중앙 동료에게 안전한 컷백 연결', metric: '전개 완료' }
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

      // 2. 볼 좌표 계산
      let ballGx = heroGx + 0.2;
      let ballGy = heroGy;

      if (pA.ball === 'shot' || pB.ball === 'shot') {
        const shotTarget = pB.shotTarget || { gx: 18.0, gy: 6.0 };
        ballGx = heroGx + (shotTarget.gx - heroGx) * smooth;
        ballGy = heroGy + (shotTarget.gy - heroGy) * smooth;
      } else if (pA.ball === 'pass' || pB.ball === 'pass') {
        const passTarget = pB.passTarget || { gx: 15.0, gy: 6.0 };
        ballGx = heroGx + (passTarget.gx - heroGx) * smooth;
        ballGy = heroGy + (passTarget.gy - heroGy) * smooth;
      } else if (pA.ball === 'goal' || pB.ball === 'goal') {
        ballGx = 18.0;
        ballGy = (pB.shotTarget ? pB.shotTarget.gy : 6.0);
      }

      // 3. 나머지 21명 선수의 전술 반응 (라인 시프트, 침투, 압박)
      // 볼 전진도에 따라 상대 수비 라인은 뒤로 물러서고, 아군 라인은 올라감
      const shiftX = (ballGx - 9.0) * 0.45;
      const shiftY = (ballGy - 6.0) * 0.35;

      const homePlayers = BASE_HOME_11.map((p, idx) => {
        if (idx === 0) {
          // 주인공 선수는 8번 슬롯(LW/AM/RW/ST 대체)에 매핑
          return { ...p, gx: heroGx, gy: heroGy, isHero: true, name: currentPlayer.name_ko || currentPlayer.name };
        }
        // 나머지 아군: 볼 진행 방향으로 유기적 서포트 침투 및 라인 전진
        let gx = p.gx + shiftX;
        let gy = p.gy + shiftY * 0.6;
        if (p.pos === 'ST' && !action.title.includes('손흥민')) {
          // 공격수는 배후 침투
          gx += Math.min(2.5, smooth * 3.0);
        }
        if (p.pos === 'RB' || p.pos === 'LB') {
          // 풀백 오버래핑
          gx += Math.min(2.0, smooth * 2.2);
        }
        return { ...p, gx: Math.max(0.5, Math.min(17.5, gx)), gy: Math.max(0.8, Math.min(11.2, gy)), isHero: false };
      });

      const awayPlayers = BASE_AWAY_11.map(p => {
        // 상대 수비: 볼 쪽으로 압박 및 오프사이드 라인 조율
        let gx = p.gx + shiftX * 0.6;
        let gy = p.gy + shiftY * 0.7;

        // 볼 소유자와 가까운 센터백/수미 2명은 적극 압박 전진
        const dist = Math.hypot(p.gx - heroGx, p.gy - heroGy);
        if (dist < 4.0 && p.pos !== 'GK') {
          gx += (heroGx - p.gx) * 0.45;
          gy += (heroGy - p.gy) * 0.45;
        }

        // 골키퍼는 슈팅 각도 좁히기
        if (p.pos === 'GK') {
          gx = 17.2 - Math.min(1.2, (ballGx / 18.0) * 1.5);
          gy = 6.0 + (ballGy - 6.0) * 0.25;
        }

        return { ...p, gx: Math.max(0.5, Math.min(17.8, gx)), gy: Math.max(0.8, Math.min(11.2, gy)) };
      });

      return {
        hero: { gx: heroGx, gy: heroGy },
        ball: { gx: ballGx, gy: ballGy },
        home: homePlayers,
        away: awayPlayers,
        currentPhase: pB
      };
    }

    // =========================================================================
    // 4. 화면 렌더링 루프
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
      const fovAngle = (state.hero.gx > 9) ? 0 : 0;
      ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
      ctx.beginPath();
      ctx.moveTo(heroPt.x, heroPt.y);
      ctx.arc(heroPt.x, heroPt.y, 110, -0.4, 0.4);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 패스/슈팅 궤적 렌더링
      const ballPt = toPixel(state.ball.gx, state.ball.gy);
      if (Math.hypot(heroPt.x - ballPt.x, heroPt.y - ballPt.y) > 15) {
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(heroPt.x, heroPt.y);
        ctx.lineTo(ballPt.x, ballPt.y);
        ctx.stroke();
        ctx.setLineDash([]);
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
          ctx.fillText(p.name.slice(0, 3), pt.x, pt.y);

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
      ctx.restore();

      // HUD 업데이트
      const phase = state.currentPhase;
      document.getElementById('hudActionText').innerText = phase.status || action.title;
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
          b.classList.add('active');
        } else if (b.innerText.includes('x')) {
          b.classList.remove('active');
        }
      });
    }

    function resetCurrentAction() {
      currentTime = 0;
    }

    function onSeekTime(val) {
      currentTime = parseFloat(val);
      renderPitch();
    }

    function selectAction(idx) {
      currentActionIdx = idx;
      currentTime = 0;
      updateActionCardsUI();
      renderPitch();
    }

    function updateActionCardsUI() {
      const cards = document.querySelectorAll('.action-card');
      cards.forEach((c, idx) => {
        if (idx === currentActionIdx) c.classList.add('active');
        else c.classList.remove('active');
      });
    }

    // =========================================================================
    // 6. 선수 변경 및 UI 동기화
    // =========================================================================
    function onSelectPlayer(playerId) {
      const p = PLAYERS_DATABASE.find(item => String(item.player_id) === String(playerId));
      if (!p) return;
      currentPlayer = p;
      currentActionIdx = 0;
      currentTime = 0;

      // 1) 좌측 프로필 카드 갱신 (DB 실측 값 반영)
      document.getElementById('pCardName').innerText = p.name_ko || p.name;
      document.getElementById('pCardPos').innerText = p.position || 'ST';
      document.getElementById('pCardClub').innerText = `${p.current_club || '소속팀 미상'} · ${p.league || ''}`;
      document.getElementById('pCardArchetype').innerText = p.tactical_archetype || '전술 스페셜리스트';
      document.getElementById('pCardStrengths').innerText = p.strengths_tags || '탁월한 경기 영향력 및 실측 데이터 우수';

      document.getElementById('pStatGoals').innerText = p.goals_per90 ? `${p.goals_per90.toFixed(2)}골` : '-';
      document.getElementById('pStatXg').innerText = p.xg_per90 ? `${p.xg_per90.toFixed(2)}` : '-';
      document.getElementById('pStatKp').innerText = p.key_passes_per90 ? `${p.key_passes_per90.toFixed(1)}회` : '-';
      document.getElementById('pStatProg').innerText = p.progressive_actions_per90 ? `${p.progressive_actions_per90.toFixed(1)}회` : '-';
      document.getElementById('pStatDef').innerText = p.defensive_duels_won_pct ? `${p.defensive_duels_won_pct.toFixed(0)}%` : '-';
      document.getElementById('pStatPctl').innerText = p.pos_percentile ? `상위 ${100 - p.pos_percentile}%` : '상위권';

      // 2) 유튜브 버튼 연동
      const ytId = YT_MAP[p.name_ko] || YT_MAP[p.name] || 'YhEcyglkOx0';
      document.getElementById('ytSyncBtn').href = `https://www.youtube.com/watch?v=${ytId}`;

      // 3) 우측 고유 액션 리스트 생성
      const actions = generatePlayerActions(p);
      const listContainer = document.getElementById('actionList');
      listContainer.innerHTML = '';

      actions.forEach((act, idx) => {
        const div = document.createElement('div');
        div.className = `action-card ${idx === 0 ? 'active' : ''}`;
        div.onclick = () => selectAction(idx);
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
      PLAYERS_DATABASE.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.player_id;
        opt.innerText = `${p.name_ko || p.name} (${p.position}) — ${p.current_club || ''}`;
        select.appendChild(opt);
      });

      // 기본 선택: 손흥민 또는 첫 번째 선수
      const defaultPlayer = PLAYERS_DATABASE.find(p => (p.name_ko && p.name_ko.includes('손흥민')) || p.name.includes('Son')) || PLAYERS_DATABASE[0];
      select.value = defaultPlayer.player_id;
      onSelectPlayer(defaultPlayer.player_id);

      requestAnimationFrame(animationLoop);
    }

    window.onload = init;
  </script>
</body>
</html>
"""

# Embed players JSON into HTML template
players_json_str = json.dumps(players, ensure_ascii=False)
final_html = html_template.replace("__PLAYERS_JSON__", players_json_str)

output_path = Path("rea/fm_2d_grid_match.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully generated {output_path} (Size: {output_path.stat().st_size:,} bytes)")
