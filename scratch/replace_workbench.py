NEW_WORKBENCH_HTML = """      <!-- ======================================================================= -->
      <!-- CORE WORKBENCH: LIVE CLUB VACANCIES & ZERO-LATENCY ZOPA MODELER -->
      <!-- ======================================================================= -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

        <!-- Left Column (6 Cols): 실시간 구단 공백 & 영입 수요 매칭 레이더 -->
        <div class="lg:col-span-6 space-y-4">
          <div class="ui-card p-4 space-y-3 bg-[#11141a] border border-white/[0.08]">
            <div class="flex items-center justify-between border-b border-white/[0.06] pb-2.5">
              <div class="flex items-center gap-2">
                <span class="text-base">🔥</span>
                <div>
                  <h3 class="text-xs font-bold text-white flex items-center gap-2">
                    <span>실시간 구단 공백 & 영입 수요 매칭 레이더</span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono">Market Vacancy</span>
                  </h3>
                  <p class="text-[11px] text-zinc-400">포지션 공백, 부상 발생 및 전술적 궁합 기반 유럽 5대 리그 추천 구단</p>
                </div>
              </div>
              <button onclick="loadClubMatchesForTarget()"
                class="px-2.5 py-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-[11px] font-medium text-zinc-200 transition flex items-center gap-1 shadow-sm">
                <span>🔄 실시간 재스캔</span>
              </button>
            </div>

            <!-- Filter & Status Bar -->
            <div class="flex items-center justify-between text-xs pt-0.5">
              <div class="flex items-center gap-2">
                <span class="text-zinc-400 text-[11px]">필터 리그:</span>
                <select id="deal-filter-league" onchange="loadClubMatchesForTarget()"
                  class="bg-[#0e1117] border border-white/[0.08] rounded-lg px-2 py-1 text-xs text-white focus:outline-none focus:border-emerald-500">
                  <option value="ALL">유럽 5대 리그 전체 탐색</option>
                  <option value="Premier League">Premier League</option>
                  <option value="La Liga">La Liga</option>
                  <option value="Serie A">Serie A</option>
                  <option value="Bundesliga">Bundesliga</option>
                  <option value="Ligue 1">Ligue 1</option>
                </select>
              </div>
              <span id="deal-match-count-badge" class="text-[11px] text-emerald-400 font-mono font-semibold"></span>
            </div>

            <!-- Matched Clubs Container -->
            <div id="deal-matched-clubs-container" class="space-y-2.5 min-h-[300px]">
              <div class="flex items-center justify-center p-8 text-xs text-zinc-500">
                <span>구단 공백 및 전술 매칭 데이터 분석 중...</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column (6 Cols): 계약 조건 & ZOPA 실시간 재무 시뮬레이터 -->
        <div class="lg:col-span-6 space-y-4">
          <div class="ui-card p-4 space-y-3 bg-[#11141a] border border-white/[0.08]">
            <div class="flex items-center justify-between border-b border-white/[0.06] pb-2.5">
              <div class="flex items-center gap-2">
                <span class="text-base">💱</span>
                <div>
                  <h3 class="text-xs font-bold text-white flex items-center gap-2">
                    <span>계약 조건 & ZOPA 실시간 재무 시뮬레이터</span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] bg-sky-500/10 text-sky-400 border border-sky-500/30 font-mono">Zero-Latency Modeler</span>
                  </h3>
                  <p class="text-[11px] text-zinc-400">조건 조절 시 구단 PSR 상각액, 선수 실수령액, 에이전시 수수료 0초 즉시 계산</p>
                </div>
              </div>
              <span id="zopa-status-pill" class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                타결 유력 (ZOPA 94%)
              </span>
            </div>

            <!-- Sliders & Financial Inputs -->
            <div class="space-y-3 text-xs">
              <!-- Target Fee Slider -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-zinc-400">목표 이적료 (Transfer Fee)</span>
                  <span id="zopa-fee-label" class="font-bold text-white font-mono">€50,000,000</span>
                </div>
                <input id="zopa-fee-slider" type="range" min="1000000" max="250000000" step="1000000" value="50000000"
                  oninput="recalcZopaModel()" class="w-full accent-emerald-500 cursor-pointer" />
                <div class="flex justify-between text-[10px] text-zinc-500 mt-0.5">
                  <span>€1M (FA/유망주)</span>
                  <span>€50M (주전급)</span>
                  <span>€250M (월드클래스)</span>
                </div>
              </div>

              <!-- Weekly Wage Slider -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-zinc-400">목표 기본 주급 (Weekly Wage)</span>
                  <span id="zopa-wage-label" class="font-bold text-emerald-400 font-mono">€150,000/주</span>
                </div>
                <input id="zopa-wage-slider" type="range" min="10000" max="600000" step="5000" value="150000"
                  oninput="recalcZopaModel()" class="w-full accent-emerald-500 cursor-pointer" />
                <div class="flex justify-between text-[10px] text-zinc-500 mt-0.5">
                  <span>€10k/주</span>
                  <span>€150k/주 (빅클럽 핵심)</span>
                  <span>€600k/주 (슈퍼스타)</span>
                </div>
              </div>

              <!-- 3 Parameter Inputs: Contract Years, Signing Bonus, Agent Fee % -->
              <div class="grid grid-cols-3 gap-2.5 pt-1">
                <div>
                  <label class="text-[10px] text-zinc-400 block mb-0.5">계약 기간</label>
                  <select id="zopa-years-select" onchange="recalcZopaModel()"
                    class="w-full bg-[#0e1117] border border-white/[0.08] rounded-lg px-2 py-1 text-xs text-white">
                    <option value="3">3년</option>
                    <option value="4">4년</option>
                    <option value="5" selected>5년 (표준)</option>
                  </select>
                </div>
                <div>
                  <label class="text-[10px] text-zinc-400 block mb-0.5">사이닝 보너스 (€)</label>
                  <input id="zopa-bonus-input" type="number" value="2000000" step="500000" oninput="recalcZopaModel()"
                    class="w-full bg-[#0e1117] border border-white/[0.08] rounded-lg px-2 py-1 text-xs text-white font-mono" />
                </div>
                <div>
                  <label class="text-[10px] text-zinc-400 block mb-0.5">에이전트 수수료율 (FFAR 3~5%)</label>
                  <input id="zopa-agent-fee-input" type="number" value="5.0" step="0.5" min="1" max="10" oninput="recalcZopaModel()"
                    class="w-full bg-[#0e1117] border border-white/[0.08] rounded-lg px-2 py-1 text-xs text-white font-mono" />
                </div>
              </div>

              <!-- Live Financial Summary Metrics Grid -->
              <div class="grid grid-cols-2 gap-2 pt-2">
                <!-- Metric 1: 구단 연간 PSR 상각액 -->
                <div class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04]">
                  <div class="text-[10px] text-zinc-400 flex items-center justify-between">
                    <span>구단 연간 장부 상각 (PSR)</span>
                    <span id="zopa-psr-badge" class="px-1 rounded text-[9px] bg-emerald-950 text-emerald-300">건전</span>
                  </div>
                  <div id="zopa-metric-psr" class="text-sm font-bold text-white font-mono mt-1">€18.2M / 년</div>
                  <div class="text-[9px] text-zinc-500 mt-0.5">이적료 상각 + 연봉 + 수수료 합산</div>
                </div>

                <!-- Metric 2: 선수 연간 세후 실수령액 -->
                <div class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04]">
                  <div class="text-[10px] text-zinc-400 flex items-center justify-between">
                    <span>선수 세후 실수령액 (Net)</span>
                    <span class="text-[9px] text-zinc-500 font-mono">최고세율 45%</span>
                  </div>
                  <div id="zopa-metric-net-wage" class="text-sm font-bold text-emerald-300 font-mono mt-1">€4.29M / 년</div>
                  <div class="text-[9px] text-zinc-500 mt-0.5">월 실수령액 약 €357,500</div>
                </div>

                <!-- Metric 3: 에이전시 5개년 누적 수수료 -->
                <div class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04]">
                  <div class="text-[10px] text-zinc-400 flex items-center justify-between">
                    <span>에이전시 5개년 누적 수수료</span>
                    <span class="px-1 rounded text-[9px] bg-purple-950 text-purple-300">FIFA 제13조</span>
                  </div>
                  <div id="zopa-metric-agency-rev" class="text-sm font-bold text-purple-300 font-mono mt-1">€1.95M</div>
                  <div class="text-[9px] text-zinc-500 mt-0.5">주급 5.0% 기준 안정적 캐시플로우</div>
                </div>

                <!-- Metric 4: ZOPA 타결 지수 -->
                <div class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04]">
                  <div class="text-[10px] text-zinc-400">ZOPA 합의 타당성 지수</div>
                  <div id="zopa-metric-score" class="text-sm font-bold text-sky-300 font-mono mt-1">94 / 100 (HIGH)</div>
                  <div id="zopa-metric-eval" class="text-[9px] text-zinc-400 mt-0.5">구단 수용 가능성 및 재정 건전성 우수</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ======================================================================= -->
      <!-- BOTTOM EXECUTIVE SIGN-OFF & FAST-TRACK DESK -->
      <!-- ======================================================================= -->
      <div class="ui-card p-5 bg-gradient-to-r from-[#11141a] via-[#131a22] to-[#11141a] border border-emerald-500/30 space-y-3 shadow-lg">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-white/[0.06] pb-2.5">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center gap-2">
              <span>🚀 원스톱 실무 결재 & 공식 계약 체결 데스크</span>
              <span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500 text-black font-bold">Fast-Track</span>
            </h3>
            <p class="text-xs text-zinc-400">구단 단장용 공식 피치덱 검토 및 사내 영입 심사 품의서(Deal Memo) 서명 즉시 체결</p>
          </div>
          <div class="text-xs text-zinc-400">
            현재 대상: <b id="deal-desk-target-name" class="text-white">선택된 대상</b>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
          <!-- Action 1: Pitch Deck -->
          <button onclick="openPitchDeckForCurrentTarget()"
            class="p-3.5 rounded-xl bg-sky-950/40 hover:bg-sky-900/50 border border-sky-500/40 text-left transition space-y-1 group">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-sky-300 flex items-center gap-1.5">
                <span>📄 구단 단장 제출용 피치덱</span>
              </span>
              <span class="text-xs text-sky-400 group-hover:translate-x-0.5 transition font-semibold">열람 ↗</span>
            </div>
            <p class="text-[11px] text-zinc-400 leading-snug">
              DataMB 레이더 백분위, CIES 가치, 전술적 강점 및 부상 안정성이 요약된 공식 리포트
            </p>
          </button>

          <!-- Action 2: Deal Memo Sign-Off -->
          <button onclick="openDealMemoForCurrentTarget()"
            class="p-3.5 rounded-xl bg-gradient-to-r from-emerald-950/50 to-teal-950/50 hover:from-emerald-900/60 hover:to-teal-900/60 border border-emerald-500/60 text-left transition space-y-1 group shadow-lg shadow-emerald-950/30">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-emerald-300 flex items-center gap-1.5">
                <span>📋 사내 영입 심사서 & 계약 체결</span>
              </span>
              <span class="text-[9px] px-1.5 py-0.5 rounded bg-emerald-500 text-black font-bold">공식 체결</span>
            </div>
            <p class="text-[11px] text-zinc-300 leading-snug">
              FIFA FFAR 제12/13조 준수 검증, 5개년 수수료 품의 및 전속 대리 계약 즉시 등록
            </p>
          </button>

          <!-- Action 3: 2D Tactics Highlights -->
          <button onclick="openTacticsForSelectedPlayer()"
            class="p-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-white/[0.08] text-left transition space-y-1 group">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-zinc-200 flex items-center gap-1.5">
                <span>🎬 2D 전술 하이라이트 분석</span>
              </span>
              <span class="text-xs text-zinc-400 group-hover:translate-x-0.5 transition font-semibold">실행 ↗</span>
            </div>
            <p class="text-[11px] text-zinc-400 leading-snug">
              100x68 정밀 피치 상에서의 하프스페이스 침투, 키패스 챕터별 동선 리플레이
            </p>
          </button>
        </div>
      </div>
"""

def replace_workbench_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = None
    tactics_idx = None
    for i, line in enumerate(lines):
        if '<!-- Strategy Parameters Setting Panel -->' in line:
            start_idx = i
        if start_idx is not None and '<!-- PAGE 3: TACTICAL DESK & 2D MATCH ENGINE -->' in line:
            tactics_idx = i
            break

    if start_idx is None or tactics_idx is None:
        print(f"Indices not found in {filepath}: start_idx={start_idx}, tactics_idx={tactics_idx}")
        return

    # find the closing </div> of page-strategy before tactics_idx
    # Search backwards from tactics_idx
    close_strategy_idx = None
    for j in range(tactics_idx - 1, start_idx, -1):
        if lines[j].strip() == '</div>':
            close_strategy_idx = j
            break

    print(f"Replacing lines {start_idx} to {close_strategy_idx} in {filepath}")
    new_lines = lines[:start_idx] + [NEW_WORKBENCH_HTML + "\n"] + lines[close_strategy_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Successfully updated workbench in {filepath}")

replace_workbench_in_file('src/sports_agency/api/static/index.html')
replace_workbench_in_file('html/index.html')
