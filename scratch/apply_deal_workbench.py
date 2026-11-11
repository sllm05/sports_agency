import re

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
      </div>"""

NEW_JS_FUNCTIONS = """
    // =========================================================================
    // TRANSFER DEAL & VALUATION DESK FUNCTIONS
    // =========================================================================
    let currentDealTarget = null;

    function syncZopaSlidersWithTarget() {
      const p = selectedPlayer || (agencyPlayers && agencyPlayers[0]);
      if (!p) return;
      currentDealTarget = p;

      const deskName = document.getElementById('deal-desk-target-name');
      if (deskName) deskName.textContent = `${p.name} (${p.current_club || '무소속'})`;

      const feeSlider = document.getElementById('zopa-fee-slider');
      const wageSlider = document.getElementById('zopa-wage-slider');

      const isMgr = Boolean(p.position === 'MGR' || p.is_manager || p.type === 'MANAGER' || (p.name && p.name.includes('(감독)')));
      const marketVal = p.market_value_eur || (isMgr ? 0 : 35000000);
      const weeklyWage = p.weekly_wage_eur || 120000;

      if (feeSlider) {
        feeSlider.value = Math.max(1000000, marketVal);
      }
      if (wageSlider) {
        wageSlider.value = Math.max(10000, weeklyWage);
      }

      recalcZopaModel();
    }

    function recalcZopaModel() {
      const feeSlider = document.getElementById('zopa-fee-slider');
      const wageSlider = document.getElementById('zopa-wage-slider');
      const yearsSelect = document.getElementById('zopa-years-select');
      const bonusInput = document.getElementById('zopa-bonus-input');
      const agentFeeInput = document.getElementById('zopa-agent-fee-input');

      const fee = parseInt(feeSlider ? feeSlider.value : '50000000', 10);
      const wage = parseInt(wageSlider ? wageSlider.value : '150000', 10);
      const years = parseInt(yearsSelect ? yearsSelect.value : '5', 10);
      const bonus = parseInt(bonusInput ? bonusInput.value : '2000000', 10);
      const agentFeePct = parseFloat(agentFeeInput ? agentFeeInput.value : '5.0');

      // Update labels
      const feeLabel = document.getElementById('zopa-fee-label');
      if (feeLabel) feeLabel.textContent = `€${fee.toLocaleString()}`;
      const wageLabel = document.getElementById('zopa-wage-label');
      if (wageLabel) wageLabel.textContent = `€${wage.toLocaleString()}/주`;

      // PSR Annual Amortization: (Fee + Bonus) / Years + Annual Wage
      const annualWage = wage * 52;
      const annualAmortization = (fee + bonus) / years;
      const annualPsrSquadCost = annualAmortization + annualWage;

      // Net Wage: Assuming European standard top tax bracket 45%
      const annualNetWage = annualWage * 0.55;
      const monthlyNetWage = annualNetWage / 12;

      // Agency 5-Year Revenue: Annual Wage * Agent Fee % * Years
      const annualAgencyFee = annualWage * (agentFeePct / 100);
      const totalAgencyRev = annualAgencyFee * years;

      // Update metrics
      const psrEl = document.getElementById('zopa-metric-psr');
      if (psrEl) psrEl.textContent = `€${(annualPsrSquadCost / 1000000).toFixed(1)}M / 년`;

      const psrBadge = document.getElementById('zopa-psr-badge');
      if (psrBadge) {
        if (annualPsrSquadCost <= 25000000) {
          psrBadge.textContent = '건전';
          psrBadge.className = 'px-1 rounded text-[9px] bg-emerald-950 text-emerald-300';
        } else if (annualPsrSquadCost <= 40000000) {
          psrBadge.textContent = '적정';
          psrBadge.className = 'px-1 rounded text-[9px] bg-sky-950 text-sky-300';
        } else {
          psrBadge.textContent = '주의 (고부담)';
          psrBadge.className = 'px-1 rounded text-[9px] bg-amber-950 text-amber-300';
        }
      }

      const netWageEl = document.getElementById('zopa-metric-net-wage');
      if (netWageEl) netWageEl.textContent = `€${(annualNetWage / 1000000).toFixed(2)}M / 년`;

      const agencyRevEl = document.getElementById('zopa-metric-agency-rev');
      if (agencyRevEl) agencyRevEl.textContent = `€${(totalAgencyRev / 1000000).toFixed(2)}M`;

      // ZOPA score calculation
      let zopaScore = 95;
      if (agentFeePct > 5.0) zopaScore -= 20;
      if (annualPsrSquadCost > 35000000) zopaScore -= 12;
      if (wage > 350000) zopaScore -= 8;
      zopaScore = Math.max(60, Math.min(99, zopaScore));

      const scoreEl = document.getElementById('zopa-metric-score');
      if (scoreEl) {
        scoreEl.textContent = `${zopaScore} / 100 (${zopaScore >= 90 ? 'HIGH' : (zopaScore >= 75 ? 'MODERATE' : 'TENSION')})`;
      }

      const statusPill = document.getElementById('zopa-status-pill');
      if (statusPill) {
        if (zopaScore >= 90) {
          statusPill.textContent = `타결 유력 (ZOPA ${zopaScore}%)`;
          statusPill.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
        } else if (zopaScore >= 75) {
          statusPill.textContent = `조건 조율 권장 (ZOPA ${zopaScore}%)`;
          statusPill.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40';
        } else {
          statusPill.textContent = `규정/재무 긴장 (ZOPA ${zopaScore}%)`;
          statusPill.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40';
        }
      }
    }

    async function loadClubMatchesForTarget() {
      const p = selectedPlayer || (agencyPlayers && agencyPlayers[0]);
      if (!p) return;
      currentDealTarget = p;

      const container = document.getElementById('deal-matched-clubs-container');
      if (!container) return;

      const leagueSelect = document.getElementById('deal-filter-league');
      const league = leagueSelect ? leagueSelect.value : 'ALL';

      container.innerHTML = `
        <div class="flex items-center justify-center p-8 text-xs text-zinc-500 gap-2">
          <span class="animate-spin text-sm">⚽</span>
          <span>5대 리그 구단 공백 및 실시간 전술 매칭 분석 중...</span>
        </div>
      `;

      try {
        const res = await fetch(`/api/transfer/club-matches?player_name=${encodeURIComponent(p.name)}&league=${league}&target_wage_increase_pct=30`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const matches = data.matches || [];

        const countBadge = document.getElementById('deal-match-count-badge');
        if (countBadge) countBadge.textContent = `${matches.length}개 구단 매칭됨`;

        if (matches.length === 0) {
          container.innerHTML = `
            <div class="p-6 text-center text-xs text-zinc-400 bg-[#0e1117] rounded-xl border border-white/[0.04]">
              현재 조건에 부합하는 긴급 영입 수요 구단이 없습니다. 필터 리그를 '전체'로 변경해 보세요.
            </div>
          `;
          return;
        }

        container.innerHTML = matches.map((m, idx) => {
          const fit = m.tactical_fit_score || 90;
          const urgency = m.recruitment_urgency || 'Medium';
          const urgencyBadge = urgency === 'High'
            ? '<span class="px-1.5 py-0.5 rounded text-[10px] bg-red-500/15 text-red-400 border border-red-500/30 font-bold">긴급 공백</span>'
            : '<span class="px-1.5 py-0.5 rounded text-[10px] bg-sky-500/15 text-sky-400 border border-sky-500/30">영입 관심</span>';

          const standing = m.club_live_standing || {};
          const rankText = standing.rank_position ? `리그 ${standing.rank_position}위` : m.league;

          return `
            <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.06] hover:border-emerald-500/40 transition space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-zinc-800 flex items-center justify-center text-xs font-bold text-emerald-400">
                    ${idx + 1}
                  </span>
                  <div>
                    <div class="text-xs font-bold text-white flex items-center gap-1.5">
                      <span>${m.club_name}</span>
                      <span class="text-[10px] text-zinc-400">· ${m.league} (${rankText})</span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-1.5">
                  ${urgencyBadge}
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 font-mono font-bold">
                    적합도 ${fit}%
                  </span>
                </div>
              </div>

              <div class="text-[11px] text-zinc-300 bg-[#0a0c10] p-2 rounded-lg border border-white/[0.03] space-y-0.5">
                <div class="text-emerald-400/90 font-medium">⚡ 영입 사유: ${m.recruitment_note || m.current_starter || '주전 스쿼드 보강 필요'}</div>
                <div class="text-zinc-400 text-[10px]">${m.tactical_style || ''}</div>
              </div>

              <div class="flex items-center justify-between text-[10px] text-zinc-400 pt-0.5">
                <div>
                  예상 주급 여력: <b class="text-white font-mono">€${(m.max_weekly_wage_offer_eur || 0).toLocaleString()}/주</b> · 
                  선발 확보율: <b class="text-emerald-400 font-mono">${m.expected_playing_time_share || 85}%</b>
                </div>
                <button onclick="openPitchDeckForCurrentTarget()"
                  class="px-2 py-1 rounded bg-sky-600/20 hover:bg-sky-600/40 border border-sky-500/30 text-sky-300 text-[10px] font-semibold transition">
                  맞춤 피치덱 ↗
                </button>
              </div>
            </div>
          `;
        }).join('');
      } catch (err) {
        container.innerHTML = `
          <div class="p-4 text-xs text-red-400 bg-red-950/20 rounded-xl border border-red-500/20">
            구단 매칭 로드 오류: ${err.message}
          </div>
        `;
      }
    }

    function openPitchDeckForCurrentTarget() {
      const p = selectedPlayer || (agencyPlayers && agencyPlayers[0]);
      if (!p) {
        showToast('먼저 스카우팅 로스터에서 대상을 선택해주세요.', 'warning');
        showPage('page-scouting');
        return;
      }
      const isMgr = Boolean(p.position === 'MGR' || p.is_manager || p.type === 'MANAGER' || (p.name && p.name.includes('(감독)')));
      generateRecruitmentPitch(p.id, isMgr ? 'MANAGER' : 'PLAYER', p.name);
    }

    function openDealMemoForCurrentTarget() {
      const p = selectedPlayer || (agencyPlayers && agencyPlayers[0]);
      if (!p) {
        showToast('먼저 스카우팅 로스터에서 대상을 선택해주세요.', 'warning');
        showPage('page-scouting');
        return;
      }
      const isMgr = Boolean(p.position === 'MGR' || p.is_manager || p.type === 'MANAGER' || (p.name && p.name.includes('(감독)')));
      openDealMemoModal(p.id, isMgr ? 'MANAGER' : 'PLAYER', p.name);
    }
"""

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. GNB button text
    content = content.replace('<span>⚔️ 이적·전술 협상 데스크</span>', '<span>⚔️ 이적 제안 & 재무 밸류에이션</span>')

    # 2. Header
    old_header = """            <h2 class="text-base font-bold text-white">이적 및 계약 협상 전략</h2>
            <p class="text-xs text-zinc-400">조건 설정 및 구단 디렉터와의 모의 협상 시뮬레이션</p>"""
    new_header = """            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <span>이적 제안 & 재무 밸류에이션 데스크</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-semibold font-mono">Transfer Deal & Valuation Workbench</span>
            </h2>
            <p class="text-xs text-zinc-400">실시간 구단 공백 매칭, 인터랙티브 ZOPA 재무 모델링(PSR/세후 연봉) 및 단장 제출용 피치덱 원스톱 승인</p>"""
    content = content.replace(old_header, new_header)

    # 3. Subnav button
    content = content.replace('<span>🗣️ 구단 단장 AI 협상 스파링</span>', '<span>📊 구단 이적 수요 & ZOPA 밸류에이션</span>')

    # 4. Old parameters + sparring block replacement
    # Look for start at `<!-- Strategy Parameters Setting Panel -->`
    # and end at `</div>\n      </div>\n\n    <!-- ======================================================================= -->\n    <!-- PAGE 4: TACTICS ENGINE`
    pattern = re.compile(r'<!-- Strategy Parameters Setting Panel -->.*?</div>\s*<!-- end of 2-Round Sparring -->|<!-- Strategy Parameters Setting Panel -->.*?</div>\s*</div>\s*(?=\s*<!-- ======================================================================= -->\s*<!-- PAGE 4: TACTICS)', re.DOTALL)
    
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + NEW_WORKBENCH_HTML + content[match.end():]
        print(f"Matched and replaced workbench in {path}")
    else:
        # Fallback search by strings
        start_str = "<!-- Strategy Parameters Setting Panel -->"
        end_marker = "<!-- PAGE 4: TACTICS ENGINE"
        s_idx = content.find(start_str)
        e_idx = content.find(end_marker)
        if s_idx != -1 and e_idx != -1:
            # find last </div> before e_idx
            sub = content[s_idx:e_idx]
            last_div = sub.rfind('</div>')
            content = content[:s_idx] + NEW_WORKBENCH_HTML + "\n\n    </div>\n\n    " + content[e_idx:]
            print(f"Replaced workbench via fallback in {path}")
        else:
            print(f"Could not find workbench block in {path}")

    # 5. showPage hook for page-strategy
    old_showpage = """      if (pageId === 'page-strategy') {
        if (selectedPlayer) updateCareerAgingChart(selectedPlayer);
      }"""
    new_showpage = """      if (pageId === 'page-strategy') {
        if (selectedPlayer) {
          updateCareerAgingChart(selectedPlayer);
          loadClubMatchesForTarget();
          syncZopaSlidersWithTarget();
        }
      }"""
    content = content.replace(old_showpage, new_showpage)

    # 6. Append JS functions right before closing </script>
    if "function syncZopaSlidersWithTarget" not in content:
        last_script = content.rfind('</script>')
        if last_script != -1:
            content = content[:last_script] + NEW_JS_FUNCTIONS + "\n  </script>" + content[last_script + len('</script>'):]
            print(f"Appended JS functions to {path}")

    # 7. Button text in scouting
    content = content.replace('이 선수로 협상 전략 수립하기 →', '이 선수로 이적 제안 & 밸류에이션 수립하기 →')
    content = content.replace('이 감독으로 협상 전략 수립하기 →', '이 감독으로 이적 제안 & 밸류에이션 수립하기 →')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Finished updating {path}")

update_file('src/sports_agency/api/static/index.html')
update_file('html/index.html')
