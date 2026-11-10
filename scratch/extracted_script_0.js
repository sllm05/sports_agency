
    let allPlayers = [];
    let selectedPlayer = null;
    let selectedTrack = 'TRACK_A_TRANSFER';
    let currentThreadId = null;
    let currentWorkflowState = null;
    let activeDocTab = 'career';
    let radarChartInstance = null;
    let activePageId = 'page-home';

    // -------------------------------------------------------------------------
    // Single-Page View Routing Controller
    // -------------------------------------------------------------------------
    function showPage(pageId) {
      if (pageId === 'page-admin') {
        const isAdmin = currentAuthUser && (currentAuthUser.email === 'admin@agent.com' || currentAuthUser.role === 'ADMIN' || currentAuthUser.is_admin);
        if (!isAdmin) {
          alert('⚠️ 대표 관리자(admin@agent.com) 전용 페이지입니다. 관리자 계정으로 로그인해주세요.');
          openAuthModal('login');
          fillAdminCredentials();
          return;
        }
      }

      activePageId = pageId;
      document.querySelectorAll('.page-view').forEach(p => p.classList.add('hidden'));

      const target = document.getElementById(pageId);
      if (target) {
        target.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }

      updateNavState(pageId);

      // Lazy load tab data
      if (pageId === 'page-portfolio') loadAgencyPortfolio();
      if (pageId === 'page-recruitment') loadAgencyRecruitmentTargets();
      if (pageId === 'page-admin') loadAdminDashboard();

      if (pageId === 'page-scouting' && selectedPlayer) {
        updateRadarChart(selectedPlayer);
      } else if (pageId === 'page-tactics') {
        initTacticsDesk();
      } else if (pageId === 'page-documents' && currentWorkflowState) {
        switchDocTab(activeDocTab || 'career');
      } else if (pageId === 'page-finance') {
        runStandalonePsrCalc();
      }

      window.location.hash = pageId.replace('page-', '');
    }

    function updateNavState(pageId) {
      const navKey = pageId.replace('page-', '');
      const buttons = [
        { id: 'nav-btn-home', key: 'home' },
        { id: 'nav-btn-portfolio', key: 'portfolio' },
        { id: 'nav-btn-recruitment', key: 'recruitment' },
        { id: 'nav-btn-scouting', key: 'scouting' },
        { id: 'nav-btn-strategy', key: 'strategy' },
        { id: 'nav-btn-tactics', key: 'tactics' },
        { id: 'nav-btn-documents', key: 'documents' },
        { id: 'nav-btn-finance', key: 'finance' },
        { id: 'nav-btn-regulations', key: 'regulations' },
        { id: 'nav-btn-admin-console', key: 'admin' },
      ];

      buttons.forEach(b => {
        const el = document.getElementById(b.id);
        if (!el) return;
        if (b.key === navKey) {
          el.className = 'nav-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-zinc-800 transition flex items-center gap-1.5 shadow-sm';
        } else {
          el.className = 'nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5';
        }
      });
    }

    // -------------------------------------------------------------------------
    // Dashboard Initialization
    // -------------------------------------------------------------------------
    async function initDashboard() {
      const hash = window.location.hash.replace('#', '');
      const initialPage = hash ? `page-${hash}` : 'page-home';

      initAuth();
      await Promise.all([
        loadSystemStatus(),
        loadQuotaStatus(),
        loadPlayers(),
        loadBosmanRadar(),
        loadUndervaluedProspects(),
        runStandalonePsrCalc(),
        loadAgencyPortfolio(),
        loadAgencyRecruitmentTargets(),
      ]);

      showPage(initialPage);
    }

    async function loadSystemStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        renderAuthStatus(data);
      } catch (e) {
        console.error(e);
      }
    }

    async function loadQuotaStatus() {
      try {
        const res = await fetch('/api/quota/status');
        if (!res.ok) return;
        const data = await res.json();
        const textEl = document.getElementById('api-quota-text');
        const badgeEl = document.getElementById('api-quota-badge');
        const dotEl = document.getElementById('api-quota-dot');
        if (textEl && dotEl && badgeEl) {
          textEl.innerText = `${data.calls_used}/${data.daily_limit}`;
          if (data.status === 'ACTIVE') {
            dotEl.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400';
            textEl.className = 'font-mono text-emerald-400 font-semibold';
            badgeEl.title = `API-Football 정상 가동 중 (잔여: ${data.calls_remaining}/${data.daily_limit}회)`;
          } else if (data.status === 'LIMIT_EXHAUSTED') {
            dotEl.className = 'w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse';
            textEl.className = 'font-mono text-amber-400 font-semibold';
            badgeEl.title = `API-Football 무료 100회 한도 소진 -> Football-Data.org 및 Google Grounding 자동 백업 가동 중`;
          } else {
            dotEl.className = 'w-1.5 h-1.5 rounded-full bg-zinc-500';
            textEl.className = 'font-mono text-zinc-400';
            badgeEl.title = `API-Football 키 미설정 -> Football-Data.org 백업 모드로 정상 작동 중 (클릭 시 갱신)`;
          }
        }
      } catch (e) {
        console.error('Quota fetch error', e);
      }
    }

    function renderAuthStatus(data) {
      const auth = data.gcp_auth || {};
      const vec = data.vector_db || {};
      const badge = document.getElementById('adc-badge');
      const dot = document.getElementById('adc-dot');
      const text = document.getElementById('adc-text');
      const projInput = document.getElementById('gcp-project-input');

      if (auth.project_id && auth.project_id !== 'your-gcp-project-id' && projInput) {
        projInput.value = auth.project_id;
      }

      if (auth.adc_authenticated) {
        badge.className = 'text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 flex items-center gap-1.5';
        dot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400';
        text.textContent = `Vertex AI 연동`;
      } else {
        badge.className = 'text-xs px-2.5 py-1 rounded-lg border border-white/[0.08] bg-[#12151c] text-zinc-400 flex items-center gap-1.5';
        dot.className = 'w-1.5 h-1.5 rounded-full bg-zinc-500';
        text.textContent = auth.project_id ? `ADC 대기` : '로컬 모드';
      }

      const homeStat = document.getElementById('home-vecdb-stat');
      if (homeStat) {
        homeStat.textContent = `${vec.rag_regulations_chunks || 687} 규정 + ${vec.scouting_notes_chunks || 3268} 전술`;
      }
    }

    async function saveGcpProject() {
      const proj = document.getElementById('gcp-project-input').value.trim();
      if (!proj) {
        alert('GCP Project ID를 입력해 주세요.');
        return;
      }
      const res = await fetch('/api/config/gcp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gcp_project: proj, gcp_location: 'global' })
      });
      const data = await res.json();
      renderAuthStatus(data);
    }

    async function refreshAuthStatus() {
      const res = await fetch('/api/auth/refresh', { method: 'POST' });
      const data = await res.json();
      renderAuthStatus(data);
    }

    async function syncFootballDataOrg() {
      const btn = document.getElementById('btn-sync-fd');
      btn.disabled = true;
      btn.textContent = '동기화 진행 중...';
      try {
        const res = await fetch('/api/sync/football-data-org', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ force_api_refresh: true })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '동기화 실패');
        await loadPlayers();
        alert(`공식 96구단 로스터 동기화 완료: ${data.summary.live_registered_players}명 등록됨`);
      } catch (e) {
        alert('Football-Data.org 동기화 오류: ' + e);
      } finally {
        btn.disabled = false;
        btn.textContent = '96구단 공식 로스터 동기화 실행';
      }
    }

    async function syncSelectedPlayerLive() {
      if (!selectedPlayer) return;
      const btn = document.getElementById('btn-live-player-sync');
      btn.disabled = true;
      btn.textContent = '실시간 검색 중...';
      try {
        const res = await fetch('/api/sync/live-player', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_name: selectedPlayer.name })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '실시간 패치 실패');
        await loadPlayers();
        selectPlayer(data.player);
        alert(`[${data.player.name}] 실시간 정보 동기화 완료`);
      } catch (e) {
        alert('선수 동기화 오류: ' + e);
      } finally {
        btn.disabled = false;
        btn.textContent = '소속팀·시세 실시간 검색 동기화';
      }
    }

    // -------------------------------------------------------------------------
    // Player Roster Filtering & Selection Logic
    // -------------------------------------------------------------------------
    let koreanRosterList = [];
    let filteredPlayersList = [];
    let currentDisplayLimit = 80;
    let onlyKoreanMode = false;

    async function loadPlayers() {
      const res = await fetch('/api/players');
      const data = await res.json();
      allPlayers = data.all_players || [];
      koreanRosterList = data.korean_roster || [];
      filteredPlayersList = allPlayers;

      populateClubDropdown('ALL');
      updateRosterCountText(allPlayers.length);
      renderPlayerGrid(filteredPlayersList, true);
    }

    function updateRosterCountText(filteredLen) {
      const total = allPlayers.length;
      const el = document.getElementById('roster-count');
      if (!el) return;
      if (filteredLen === total) {
        el.textContent = `${total.toLocaleString()}명 (96개 구단)`;
      } else {
        el.textContent = `${filteredLen.toLocaleString()}명 / 전체 ${total.toLocaleString()}명`;
      }
    }

    function populateClubDropdown(leagueFilter) {
      const clubSelect = document.getElementById('club-filter-select');
      if (!clubSelect) return;
      const clubsSet = new Set();
      allPlayers.forEach(p => {
        if (leagueFilter === 'ALL' || p.league === leagueFilter) {
          clubsSet.add(p.current_club);
        }
      });
      const clubs = Array.from(clubsSet).sort();
      clubSelect.innerHTML = `<option value="ALL">전체 구단 (${clubs.length}개)</option>` +
        clubs.map(c => `<option value="${c}">${c}</option>`).join('');
    }

    function onLeagueFilterChange() {
      const lg = document.getElementById('league-filter-select').value;
      populateClubDropdown(lg);
      onlyKoreanMode = false;
      currentDisplayLimit = 80;
      applyRosterFilters();
    }

    function applyRosterFilters() {
      const lg = document.getElementById('league-filter-select').value;
      const club = document.getElementById('club-filter-select').value;
      const pos = document.getElementById('pos-filter-select').value;
      const q = document.getElementById('player-search-input').value.trim().toLowerCase();

      filteredPlayersList = allPlayers.filter(p => {
        if (onlyKoreanMode && p.nationality !== 'South Korea') return false;
        if (lg !== 'ALL' && p.league !== lg) return false;
        if (club !== 'ALL' && p.current_club !== club) return false;
        if (pos !== 'ALL' && p.position !== pos) return false;
        if (q) {
          const matchName = p.name && p.name.toLowerCase().includes(q);
          const matchKo = p.name_ko && p.name_ko.toLowerCase().includes(q);
          const matchClub = p.current_club && p.current_club.toLowerCase().includes(q);
          const matchNat = p.nationality && p.nationality.toLowerCase().includes(q);
          const matchPos = p.position && p.position.toLowerCase() === q;
          if (!matchName && !matchKo && !matchClub && !matchNat && !matchPos) return false;
        }
        return true;
      });

      updateRosterCountText(filteredPlayersList.length);
      renderPlayerGrid(filteredPlayersList, false);
    }

    function loadMorePlayers() {
      currentDisplayLimit += 100;
      renderPlayerGrid(filteredPlayersList, false);
    }

    function filterManagersOnly() {
      onlyKoreanMode = false;
      document.getElementById('league-filter-select').value = 'ALL';
      populateClubDropdown('ALL');
      document.getElementById('pos-filter-select').value = 'MGR';
      document.getElementById('player-search-input').value = '';
      currentDisplayLimit = 100;
      applyRosterFilters();
    }

    function filterKoreanBig5() {
      onlyKoreanMode = true;
      document.getElementById('league-filter-select').value = 'ALL';
      populateClubDropdown('ALL');
      document.getElementById('pos-filter-select').value = 'ALL';
      document.getElementById('player-search-input').value = '';
      currentDisplayLimit = 80;
      applyRosterFilters();
    }

    function resetPlayerFilter() {
      onlyKoreanMode = false;
      document.getElementById('league-filter-select').value = 'ALL';
      populateClubDropdown('ALL');
      document.getElementById('pos-filter-select').value = 'ALL';
      document.getElementById('player-search-input').value = '';
      currentDisplayLimit = 80;
      applyRosterFilters();
    }

    function renderPlayerGrid(list, selectFirst = false) {
      const grid = document.getElementById('player-roster-grid');
      if (!grid) return;
      grid.innerHTML = '';

      const slice = list.slice(0, currentDisplayLimit);
      slice.forEach((p, idx) => {
        const card = document.createElement('button');
        card.id = `player-card-${p.player_id}`;
        card.onclick = () => selectPlayer(p);
        const isSelected = selectedPlayer && selectedPlayer.player_id === p.player_id;
        card.className = isSelected
          ? 'player-card text-left p-2.5 rounded-lg border border-emerald-500 bg-emerald-950/20 transition flex flex-col justify-between'
          : 'player-card text-left p-2.5 rounded-lg border border-white/[0.06] bg-[#0e1117] hover:border-zinc-600 transition flex flex-col justify-between';
        const displayName = p.name_ko !== p.name ? `${p.name_ko} (${p.name})` : p.name;
        card.innerHTML = `
          <div class="flex items-center justify-between w-full">
            <span class="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-zinc-800 text-zinc-300">${p.position}</span>
            <span class="text-[10px] text-zinc-500">${p.age}세 · ${p.contract_expires.slice(0,4)}만료</span>
          </div>
          <div class="mt-1">
            <div class="text-xs font-semibold text-white truncate">${displayName}</div>
            <div class="text-[10px] text-zinc-400 truncate">${p.current_club}</div>
          </div>
          <div class="mt-1.5 pt-1 border-t border-white/[0.04] flex items-center justify-between text-[10px]">
            <span class="text-emerald-400 font-semibold">€${(p.market_value_eur / 1000000).toFixed(1)}M</span>
            <span class="text-zinc-400">€${(p.weekly_wage_eur / 1000).toFixed(0)}k/주</span>
          </div>
        `;
        grid.appendChild(card);
        if (selectFirst && idx === 0) selectPlayer(p);
      });

      const loadMoreContainer = document.getElementById('load-more-container');
      const btnLoadMore = document.getElementById('btn-load-more');
      if (list.length > currentDisplayLimit) {
        loadMoreContainer.classList.remove('hidden');
        btnLoadMore.textContent = `+ 더 보기 (${currentDisplayLimit.toLocaleString()} / ${list.length.toLocaleString()}명)`;
      } else {
        loadMoreContainer.classList.add('hidden');
      }
    }

    function selectPlayer(p) {
      selectedPlayer = p;
      const targetType = (p.position === 'MGR') ? 'MANAGER' : 'PLAYER';
      if (typeof updateScoutingWatchlistButton === 'function') {
        updateScoutingWatchlistButton(p.player_id, targetType);
      }
      document.querySelectorAll('.player-card').forEach(el => {
        el.className = 'player-card text-left p-2.5 rounded-lg border border-white/[0.06] bg-[#0e1117] hover:border-zinc-600 transition flex flex-col justify-between';
      });
      const activeEl = document.getElementById(`player-card-${p.player_id}`);
      if (activeEl) {
        activeEl.className = 'player-card text-left p-2.5 rounded-lg border border-emerald-500 bg-emerald-950/20 transition flex flex-col justify-between';
      }

      const navName = document.getElementById('nav-player-name');
      if (navName) navName.textContent = p.name_ko || p.name;
      const homePlayerStat = document.getElementById('home-active-player-stat');
      if (homePlayerStat) homePlayerStat.textContent = `${p.name_ko} (${p.age}세, ${p.position})`;

      const stratName = document.getElementById('strat-target-name');
      const stratBadge = document.getElementById('strat-target-badge');
      if (stratName) stratName.textContent = `${p.name_ko} (${p.name})`;
      if (stratBadge) stratBadge.textContent = `${p.current_club} · ${p.position} · €${(p.market_value_eur/1000000).toFixed(1)}M`;

      const spCard = document.getElementById('selected-player-card');
      if (spCard) spCard.classList.remove('hidden');
      document.getElementById('sp-pos').textContent = `${p.position} (${p.secondary_positions})`;
      document.getElementById('sp-name').textContent = `${p.name_ko} (${p.name})`;
      document.getElementById('sp-club').textContent = `${p.current_club} · ${p.league} · 계약만료 ${p.contract_expires}`;
      document.getElementById('sp-val').textContent = `€${p.market_value_eur.toLocaleString()}`;
      document.getElementById('sp-wage').textContent = `주급 €${p.weekly_wage_eur.toLocaleString()}`;
      document.getElementById('sp-strengths').textContent = `전술 특성: ${p.strengths_summary}`;
      document.getElementById('sp-percentile-badge').textContent = `상위 ${100 - p.pos_percentile + 1}%`;

      const gbeAuto = p.intl_match_pct >= 70
        ? `<span class="text-emerald-400 font-semibold">GBE Auto-Pass (A매치 ${p.intl_match_pct}%)</span>`
        : `<span class="text-zinc-300 font-medium">A매치 ${p.intl_match_pct}% (GBE 점수 검토)</span>`;
      document.getElementById('sp-gbe-mini').innerHTML = `${gbeAuto}<br/>전진 액션 <b>${p.progressive_actions_per90}회/90분</b> · 키패스 <b>${p.key_passes_per90}회/90분</b>`;

      updateRadarChart(p);
      loadPlayerDeepAnalytics(p.name);
      previewPsrLive();
    }

    async function loadPlayerDeepAnalytics(playerName) {
      const box = document.getElementById('sp-deep-profile');
      if (!box) return;
      box.innerHTML = '<div class="text-zinc-500">프로파일 분석 중...</div>';
      try {
        const res = await fetch('/api/players/' + encodeURIComponent(playerName));
        if (!res.ok) return;
        const d = await res.json();
        const vp = d.valuation_and_profile || {};
        const pt = d.playstyle_and_tendencies || {};
        const mgr = d.club_manager_profile || {};
        const trs = d.transfer_history || [];
        const st = d.club_standing_and_finance || {};

        const mgrScores = mgr.name
          ? `전술유연성 <b>${mgr.tactical_flexibility_score}</b> · 공격코칭 <b>${mgr.attacking_coaching_score}</b> · 유망주신뢰 <b>${mgr.youth_trust_score}</b>`
          : '-';

        const posReq = (mgr.preferred_player_profiles && mgr.preferred_player_profiles[d.position]) || '전술 수행 및 공수 전환';

        box.innerHTML = `
          <div class="text-zinc-300 font-semibold">선수 심층 분석</div>
          <div>신체/A매치: ${vp.height_cm || 180}cm | A매치 ${vp.international_caps || 0}경기 ${vp.international_goals || 0}골 | 최고 시세 <span class="text-emerald-400">€${((vp.highest_market_value_eur || d.market_value_eur)/1000000).toFixed(1)}M</span></div>
          <div>플레이 아키타입: <span class="text-zinc-200 font-medium">${pt.tactical_archetype || '-'}</span></div>
          <div>핵심 강점: <span class="text-emerald-400">${pt.strengths_tags || '-'}</span></div>
          <div>보완점: <span class="text-zinc-400">${pt.weaknesses_tags || '-'}</span></div>
          <div class="pt-1 mt-1 border-t border-white/[0.04]">
            <div>소속팀 감독 (${mgr.name || '-'}): ${mgr.preferred_formation || '-'} | 승률 ${mgr.win_rate_pct || 0}%</div>
            <div>감독 요구사항: <span class="text-zinc-400">${posReq}</span></div>
          </div>
        `;
      } catch (e) {
        box.innerHTML = '';
      }
    }

    function updateRadarChart(p) {
      const canvas = document.getElementById('playerRadarChart');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const progScore = Math.min(99, Math.round((p.progressive_actions_per90 / 9.5) * 100));
      const keyPassScore = Math.min(99, Math.round((p.key_passes_per90 / 2.8) * 100));
      const gaScore = Math.min(99, Math.round(((p.goals_per90 + p.assists_per90) / 0.9) * 100));
      const duelScore = Math.min(99, Math.round(p.defensive_duels_won_pct));
      const pctScore = p.pos_percentile;

      if (radarChartInstance) radarChartInstance.destroy();
      radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['포지션 백분위', '전진 액션', '기회 창출', '공격포인트', '경합 성공률'],
          datasets: [{
            label: p.name_ko,
            data: [pctScore, progScore, keyPassScore, Math.max(35, gaScore), duelScore],
            backgroundColor: 'rgba(16, 185, 129, 0.2)',
            borderColor: '#10b981',
            pointBackgroundColor: '#10b981',
            borderWidth: 1.5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              min: 0,
              max: 100,
              ticks: { display: false },
              grid: { color: 'rgba(255, 255, 255, 0.08)' },
              angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
              pointLabels: { color: '#94a3b8', font: { size: 10, weight: '500' } }
            }
          },
          plugins: { legend: { display: false } }
        }
      });
    }

    // -------------------------------------------------------------------------
    // Strategy & Workflow Execution
    // -------------------------------------------------------------------------
    function selectTrack(mode) {
      selectedTrack = mode;
      const btnA = document.getElementById('btn-track-a');
      const btnB = document.getElementById('btn-track-b');
      if (mode === 'TRACK_A_TRANSFER') {
        btnA.className = 'text-left p-3 rounded-xl border border-emerald-500 bg-emerald-500/10 transition';
        btnB.className = 'text-left p-3 rounded-xl border border-white/[0.08] bg-[#0e1117] hover:border-zinc-600 transition';
      } else {
        btnB.className = 'text-left p-3 rounded-xl border border-emerald-500 bg-emerald-500/10 transition';
        btnA.className = 'text-left p-3 rounded-xl border border-white/[0.08] bg-[#0e1117] hover:border-zinc-600 transition';
      }
    }

    function updateSliderLabel(val) {
      document.getElementById('wage-slider-label').textContent = `+${val}%`;
    }

    async function startWorkflow() {
      if (!selectedPlayer) {
        alert('먼저 선수를 선택해 주세요.');
        showPage('page-scouting');
        return;
      }
      const btn = document.getElementById('btn-start-workflow');
      btn.disabled = true;
      btn.textContent = '협상 시뮬레이션 실행 중...';

      try {
        const contractOverride = {
          actual_weekly_wage_eur: parseInt(document.getElementById('ov-actual-wage').value || '0', 10),
          custom_market_value_eur: parseInt(document.getElementById('ov-market-val').value || '0', 10),
          contract_years: parseInt(document.getElementById('ov-contract-years').value || '4', 10),
          signing_bonus_eur: parseInt(document.getElementById('ov-signing-bonus').value || '0', 10),
          current_release_clause_eur: 0,
          agent_fee_pct: parseFloat(document.getElementById('ov-agent-fee').value || '7.0')
        };
        const payload = {
          player_name: selectedPlayer.name,
          track_mode: selectedTrack,
          target_wage_increase_pct: parseInt(document.getElementById('wage-slider').value, 10),
          priority_goal: document.getElementById('priority-select').value,
          preferred_league: document.getElementById('preferred-league-select').value,
          contract_override: contractOverride,
          auto_complete: false
        };
        const res = await fetch('/api/workflow/start', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        currentThreadId = data.thread_id;
        currentWorkflowState = data.state;

        renderAnalysisAndSparring(data);
      } catch (e) {
        alert('워크플로우 실행 중 오류: ' + e);
      } finally {
        btn.disabled = false;
        btn.textContent = '전략 수립 및 1차 모의 협상 시작 →';
      }
    }

    function renderAnalysisAndSparring(data) {
      const st = data.state;
      document.getElementById('analysis-section').classList.remove('hidden');
      document.getElementById('thread-badge').textContent = `ID: ${data.thread_id.slice(0, 8)}`;

      const statusBadge = document.getElementById('workflow-status-badge');
      const completeBanner = document.getElementById('workflow-complete-banner');

      if (data.status === 'WAITING_FOR_HUMAN_STRATEGY') {
        statusBadge.textContent = '2라운드 전략 선택 대기';
        statusBadge.className = 'text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300';
        document.getElementById('hitl-action-panel').classList.remove('hidden');
        if (completeBanner) completeBanner.classList.add('hidden');
      } else {
        statusBadge.textContent = '최종 합의 및 문서 생성 완료';
        statusBadge.className = 'text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300';
        document.getElementById('hitl-action-panel').classList.add('hidden');
        if (completeBanner) completeBanner.classList.remove('hidden');
      }

      document.getElementById('supervisor-note-box').textContent = st.supervisor_note || '';

      const pills = document.getElementById('model-usage-pills');
      pills.innerHTML = (st.model_usage_log || []).map(item => `
        <span class="px-2 py-0.5 rounded bg-[#0e1117] border border-white/[0.04] text-zinc-400">
          ${item.node}: <span class="text-zinc-200">${item.model}</span>
        </span>
      `).join('');

      document.getElementById('hermes-ai-summary').textContent = st.hermes_ai_summary || '';
      const band = (st.peer_wage_band || {}).wage_band_eur || {};
      const psr = st.psr_and_tax_breakdown || {};
      const psrHtml = psr.annual_psr_book_cost_eur ? `
        <div class="p-2 rounded bg-[#0e1117] border border-white/[0.04] space-y-0.5 mt-1">
          <div class="flex justify-between font-semibold text-zinc-200">
            <span>구단 연간 PSR 비용</span>
            <span>€${(psr.annual_psr_book_cost_eur || 0).toLocaleString()}/년</span>
          </div>
          <div class="text-[10px] text-zinc-400">
            세후 실수령: €${(psr.weekly_net_wage_eur || 0).toLocaleString()}/주 (세율 ${psr.top_income_tax_rate_pct}%)
          </div>
        </div>
      ` : '';
      document.getElementById('wage-band-bars').innerHTML = `
        <div class="flex justify-between p-1.5 rounded bg-[#0e1117]">
          <span class="text-zinc-400">보수적 (Q25)</span>
          <span class="font-medium text-zinc-300">€${(band.q25_conservative || 0).toLocaleString()}/주</span>
        </div>
        <div class="flex justify-between p-1.5 rounded bg-emerald-950/20 border border-emerald-500/30">
          <span class="text-emerald-400 font-medium">중앙값 (Median)</span>
          <span class="font-bold text-emerald-400">€${(band.median_fair || 0).toLocaleString()}/주</span>
        </div>
        <div class="flex justify-between p-1.5 rounded bg-[#0e1117]">
          <span class="text-zinc-400">상한 (Q75)</span>
          <span class="font-medium text-zinc-300">€${(band.q75_ambitious || 0).toLocaleString()}/주</span>
        </div>
        ${psrHtml}
      `;

      document.getElementById('hermes-tool-trace').innerHTML = (st.hermes_tool_trace || []).map(t =>
        `<div class="truncate">${t.xml_protocol.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>`
      ).join('');

      const news = st.live_club_news || {};
      document.getElementById('live-news-box').innerHTML = `
        <div class="text-[10px] text-zinc-500 uppercase">${news.source || 'Scouting Desk'}</div>
        <div class="text-xs font-semibold text-white">${news.headline || ''}</div>
        <div class="text-[11px] text-zinc-400">${news.tactical_context || ''}</div>
      `;

      const clubs = st.matched_clubs || [];
      const clubsEl = document.getElementById('matched-clubs-list');
      if (clubs.length > 0) {
        clubsEl.innerHTML = clubs.slice(0, 3).map((c, idx) => `
          <div class="p-2 rounded-lg bg-[#0e1117] border border-white/[0.04] text-xs space-y-0.5">
            <div class="flex justify-between font-semibold text-white">
              <span>${idx + 1}. ${c.club_name} (${c.league})</span>
              <span class="text-emerald-400">€${c.max_weekly_wage_offer_eur.toLocaleString()}/주</span>
            </div>
            <div class="text-[11px] text-zinc-400">현 주전: ${c.current_starter} (${c.starter_age}세)</div>
            <div class="text-[11px] text-zinc-400">감독: ${c.manager_name || '-'} (${c.manager_preferred_formation || '-'})</div>
          </div>
        `).join('');
      } else {
        clubsEl.innerHTML = `
          <div class="p-2 rounded-lg bg-[#0e1117] text-xs text-zinc-400">
            Track B (재계약 모드): 현 소속팀 협상에 집중합니다.
          </div>
        `;
      }

      const career = st.career_strategy || {};
      const badgeEl = document.getElementById('career-path-badge');
      const noteEl = document.getElementById('career-leverage-note');
      const roadEl = document.getElementById('career-roadmap-box');
      if (badgeEl) badgeEl.textContent = career.path_label || '전략 수립됨';
      if (noteEl) noteEl.textContent = career.contract_leverage || career.rationale || '';
      if (roadEl && career.three_year_roadmap) {
        roadEl.innerHTML = career.three_year_roadmap.map(y => `
          <div class="p-1 rounded bg-[#0e1117] text-[11px]">
            <span class="text-zinc-300 font-medium">${y.year}:</span>
            <span class="text-zinc-400">${y.phase}</span>
          </div>
        `).join('');
      }

      const legal = st.rag_legal_review || {};
      document.getElementById('legal-review-box').innerHTML = `
        <div class="p-2 rounded bg-[#0e1117]">
          <div class="font-medium text-emerald-400">${legal.gbe_work_permit_result || ''}</div>
          <div class="text-[10px] text-zinc-500">${legal.gbe_source || ''}</div>
        </div>
        <div class="p-2 rounded bg-[#0e1117]">
          <div class="font-medium text-zinc-300">${legal.non_eu_quota_result || ''}</div>
          <div class="text-[10px] text-zinc-500">${legal.non_eu_source || ''}</div>
        </div>
        <div class="p-2 rounded bg-[#0e1117]">
          <div class="text-[11px] text-zinc-400">${legal.ffar_fee_guidance || ''}</div>
          <div class="text-[10px] text-zinc-500">${legal.ffar_source || ''}</div>
        </div>
      `;

      document.getElementById('rag-chunks-list').innerHTML = (st.rag_retrieved_chunks || []).map(c => `
        <div class="p-1.5 rounded bg-[#0a0c10] text-[10px]">
          <div class="flex justify-between text-zinc-300">
            <span class="truncate">${c.title}</span>
            <span>유사도 ${c.similarity_score}</span>
          </div>
        </div>
      `).join('');

      renderSparringTranscript(st.sparring_transcript || []);
      document.getElementById('analysis-section').scrollIntoView({ behavior: 'smooth' });
    }

    function renderSparringTranscript(transcript) {
      const box = document.getElementById('sparring-chat-box');
      box.innerHTML = transcript.map(item => {
        const isAgent = item.speaker.includes('에이전트');
        return `
          <div class="flex flex-col ${isAgent ? 'items-start' : 'items-end'}">
            <div class="text-[11px] font-semibold mb-1 ${isAgent ? 'text-emerald-400' : 'text-zinc-400'}">
              [${item.round}] ${item.speaker}
            </div>
            <div class="max-w-2xl p-3 rounded-xl text-xs leading-relaxed ${
              isAgent
                ? 'bg-[#12151c] border border-emerald-500/30 text-zinc-200'
                : 'bg-[#12151c] border border-white/[0.06] text-zinc-300'
            }">
              ${item.message}
            </div>
          </div>
        `;
      }).join('');
    }

    async function resumeWorkflow(choice) {
      if (!currentThreadId) return;
      const panel = document.getElementById('hitl-action-panel');
      panel.innerHTML = '<div class="text-xs font-semibold text-emerald-400 py-3 text-center">선택한 전략으로 2라운드 협상 타결 및 문서를 생성하고 있습니다...</div>';

      try {
        const res = await fetch('/api/workflow/resume', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            thread_id: currentThreadId,
            human_action_choice: choice
          })
        });
        const data = await res.json();
        currentWorkflowState = data.state;

        renderAnalysisAndSparring(data);
      } catch (e) {
        alert('협상 재개 오류: ' + e);
      }
    }

    // -------------------------------------------------------------------------
    // Documents Viewer Logic
    // -------------------------------------------------------------------------
    function switchDocTab(tab) {
      activeDocTab = tab;
      const btnCareer = document.getElementById('tab-btn-career');
      const btnPrep = document.getElementById('tab-btn-prep');
      const btnPitch = document.getElementById('tab-btn-pitch');
      const printArea = document.getElementById('printable-area');

      const idleBtn = 'px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 text-zinc-300 hover:bg-zinc-700 transition';
      if (btnCareer) btnCareer.className = idleBtn;
      if (btnPrep) btnPrep.className = idleBtn;
      if (btnPitch) btnPitch.className = idleBtn;

      let content = '';
      if (tab === 'career') {
        if (btnCareer) btnCareer.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition';
        content = (currentWorkflowState && currentWorkflowState.career_report_md) || '';
      } else if (tab === 'prep') {
        if (btnPrep) btnPrep.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition';
        content = (currentWorkflowState && currentWorkflowState.deal_prep_md) || '';
      } else if (tab === 'pitch') {
        if (btnPitch) btnPitch.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition';
        content = (currentWorkflowState && currentWorkflowState.pitch_deck_md) || '';
      }

      if (content) {
        printArea.innerHTML = marked.parse(content);
      } else {
        printArea.innerHTML = `
          <div class="text-center py-16 text-zinc-500 space-y-2">
            <div class="text-sm font-semibold text-zinc-300">해당 문서가 아직 생성되지 않았습니다.</div>
            <p class="text-xs text-zinc-500 max-w-sm mx-auto">
              [이적 및 계약 협상]에서 모의 협상을 완료하면 3종 문서가 실시간으로 이곳에 렌더링됩니다.
            </p>
            <button onclick="showPage('page-strategy')"
              class="mt-2 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition">
              협상 전략 수립하러 가기 →
            </button>
          </div>
        `;
      }
    }

    function copyActiveMarkdown() {
      if (!currentWorkflowState) {
        alert('복사할 생성 문서가 없습니다.');
        return;
      }
      let md = currentWorkflowState.career_report_md || '';
      if (activeDocTab === 'prep') md = currentWorkflowState.deal_prep_md || '';
      else if (activeDocTab === 'pitch') md = currentWorkflowState.pitch_deck_md || '';
      navigator.clipboard.writeText(md || '');
      alert('마크다운이 클립보드에 복사되었습니다.');
    }

    function downloadActiveMarkdown() {
      if (!currentWorkflowState || !currentWorkflowState.saved_files) {
        alert('다운로드할 파일이 없습니다.');
        return;
      }
      let fullPath = currentWorkflowState.saved_files.career_report_file || currentWorkflowState.saved_files.root_career_file;
      if (activeDocTab === 'prep') {
        fullPath = currentWorkflowState.saved_files.deal_prep_file || currentWorkflowState.saved_files.internal_deal_prep_sheet;
      } else if (activeDocTab === 'pitch') {
        fullPath = currentWorkflowState.saved_files.pitch_deck_file || currentWorkflowState.saved_files.external_club_pitch_deck;
      }
      if (!fullPath) return;
      const fileName = fullPath.split(/[\\/]/).pop();
      window.open(`/api/outputs/${fileName}`, '_blank');
    }

    // -------------------------------------------------------------------------
    // Undervalued Prospects & Bosman Radar
    // -------------------------------------------------------------------------
    async function loadUndervaluedProspects() {
      const grid = document.getElementById('prospects-grid');
      if (!grid) return;
      grid.innerHTML = '<div class="text-xs text-zinc-500 py-3 col-span-3">유망주 스캔 중...</div>';
      try {
        const res = await fetch('/api/scout/prospects?max_age=23&min_percentile=75&limit=6');
        const data = await res.json();
        const list = data.prospects || [];
        grid.innerHTML = list.map(p => `
          <div onclick="selectProspectByName('${p.name}')"
            class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04] hover:border-zinc-600 transition cursor-pointer space-y-1 text-xs">
            <div class="flex items-center justify-between font-semibold text-white">
              <span>${p.name_ko} (${p.name})</span>
              <span class="text-[10px] text-zinc-400 font-mono">${p.position} · ${p.age}세</span>
            </div>
            <div class="text-[11px] text-zinc-400">${p.current_club} (${p.league})</div>
            <div class="flex items-center justify-between text-[11px] pt-1 border-t border-white/[0.04]">
              <span class="text-emerald-400 font-semibold">€${(p.market_value_eur/1000000).toFixed(1)}M</span>
              <span class="text-zinc-400">상위 ${100 - p.pos_percentile + 1}%</span>
            </div>
          </div>
        `).join('');
      } catch (e) {
        grid.innerHTML = '<div class="text-xs text-zinc-500 py-2 col-span-3">유망주 스캔 실패</div>';
      }
    }

    function selectProspectByName(name) {
      const found = allPlayers.find(p => p.name === name);
      if (found) {
        selectPlayer(found);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    async function loadBosmanRadar() {
      const pos = document.getElementById('bosman-pos-select').value;
      const lg = document.getElementById('bosman-league-select').value;
      const grid = document.getElementById('bosman-radar-grid');
      const badge = document.getElementById('bosman-count-badge');
      if (!grid) return;
      try {
        const res = await fetch(`/api/radar/bosman?position=${encodeURIComponent(pos)}&league=${encodeURIComponent(lg)}`);
        const data = await res.json();
        const list = data.targets || [];
        badge.textContent = `타겟 구단 ${list.length}개 포착`;
        grid.innerHTML = list.map(t => `
          <div class="p-2.5 rounded-lg bg-[#0e1117] border border-white/[0.04] space-y-1 text-xs">
            <div class="flex items-center justify-between font-semibold text-white">
              <span>${t.club_name} (${t.league})</span>
              <span class="text-[10px] text-emerald-400 font-mono">${t.priority_score}점</span>
            </div>
            <div class="text-[11px] text-zinc-300">${t.opportunity_type}</div>
            <div class="text-[11px] text-zinc-400">현 주전: ${t.current_starter} (${t.starter_age}세)</div>
            <div class="flex items-center justify-between pt-1 border-t border-white/[0.04] text-[10px] text-zinc-400">
              <span>이적료 예산 €${((t.max_transfer_fee_budget_eur || 0)/1000000).toFixed(1)}M</span>
              <span class="text-emerald-400 font-medium">최대 주급 €${(t.max_weekly_wage_offer_eur || 0).toLocaleString()}/주</span>
            </div>
          </div>
        `).join('');
      } catch (e) {
        console.error(e);
      }
    }

    function switchScoutingSubTab(tab) {
      ['prospects', 'bosman', 'custom'].forEach(t => {
        const panel = document.getElementById(`scout-panel-${t}`);
        if (panel) panel.classList.toggle('hidden', t !== tab);
      });
      document.getElementById('wb-tab-prospects').className = tab === 'prospects'
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 text-zinc-300 hover:bg-zinc-700 transition';
      document.getElementById('wb-tab-bosman').className = tab === 'bosman'
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 text-zinc-300 hover:bg-zinc-700 transition';
      document.getElementById('wb-tab-custom').className = tab === 'custom'
        ? 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition'
        : 'px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 text-zinc-300 hover:bg-zinc-700 transition';
    }

    async function registerCustomClient() {
      const payload = {
        name_ko: document.getElementById('cust-name-ko').value.trim(),
        name: document.getElementById('cust-name-en').value.trim(),
        position: document.getElementById('cust-pos').value,
        secondary_positions: document.getElementById('cust-sec-pos').value.trim(),
        current_club: document.getElementById('cust-club').value.trim(),
        league: document.getElementById('cust-league').value.trim(),
        age: parseInt(document.getElementById('cust-age').value || '20', 10),
        current_league_band: parseInt(document.getElementById('cust-band').value || '2', 10),
        market_value_eur: parseInt(document.getElementById('cust-val').value || '4500000', 10),
        weekly_wage_eur: parseInt(document.getElementById('cust-wage').value || '15000', 10),
        contract_expires: '2027-06-30',
        nationality: 'South Korea',
        goals_per90: 0.35,
        assists_per90: 0.22,
        xg_per90: 0.30,
        xa_per90: 0.20,
        progressive_actions_per90: 6.5,
        key_passes_per90: 1.7,
        defensive_duels_won_pct: 57.5,
        minutes_played: 2580,
        appearances: 31,
        intl_match_pct: 45,
        continental_minutes_pct: 60,
        is_eu_citizen: 0,
        strengths_summary: '드리블 돌파 및 양발 결정력',
        weaknesses_summary: ''
      };
      try {
        const res = await fetch('/api/players/custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '등록 실패');
        await loadPlayers();
        selectPlayer(data.player);
        alert(`외부 선수 [${data.player.name_ko}] 등록 완료`);
        showPage('page-strategy');
      } catch (e) {
        alert('선수 등록 오류: ' + e);
      }
    }

    // -------------------------------------------------------------------------
    // Financial PSR & Tax Simulator
    // -------------------------------------------------------------------------
    async function previewPsrLive() {
      if (!selectedPlayer) return;
      const box = document.getElementById('live-psr-mini-preview');
      if (!box) return;
      const ovWage = parseInt(document.getElementById('ov-actual-wage').value || '0', 10);
      const ovVal = parseInt(document.getElementById('ov-market-val').value || '0', 10);
      const years = parseInt(document.getElementById('ov-contract-years').value || '4', 10);
      const bonus = parseInt(document.getElementById('ov-signing-bonus').value || '0', 10);
      const feePct = parseFloat(document.getElementById('ov-agent-fee').value || '7.0');
      const incPct = parseInt(document.getElementById('wage-slider').value || '30', 10);

      const baseWage = ovWage > 0 ? ovWage : selectedPlayer.weekly_wage_eur;
      const targetWage = Math.round(baseWage * (1 + incPct / 100.0));
      const fee = selectedTrack === 'TRACK_B_RENEWAL' ? 0 : (ovVal > 0 ? ovVal : selectedPlayer.market_value_eur);
      const prefLg = document.getElementById('preferred-league-select').value;
      const league = prefLg !== 'ALL' ? prefLg : selectedPlayer.league;

      try {
        const res = await fetch('/api/finance/psr-tax', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            league,
            transfer_fee_eur: fee,
            weekly_wage_eur: targetWage,
            contract_years: years,
            agent_fee_pct: feePct,
            signing_bonus_eur: bonus
          })
        });
        const d = await res.json();
        box.innerHTML = `
          <div class="flex justify-between font-semibold text-zinc-200">
            <span>목표 주급 €${targetWage.toLocaleString()}/주 (${d.league})</span>
            <span>실수령: €${d.weekly_net_wage_eur.toLocaleString()}/주</span>
          </div>
          <div class="text-zinc-400 mt-0.5">
            구단 연간 PSR 장부 비용: <span class="text-zinc-200 font-semibold">€${d.annual_psr_book_cost_eur.toLocaleString()}/년</span>
          </div>
        `;
      } catch (e) {
        console.error(e);
      }
    }

    async function runStandalonePsrCalc() {
      const box = document.getElementById('standalone-psr-result');
      if (!box) return;
      const league = document.getElementById('calc-league').value;
      const fee = parseInt(document.getElementById('calc-fee').value || '0', 10);
      const wage = parseInt(document.getElementById('calc-wage').value || '0', 10);
      const years = parseInt(document.getElementById('calc-years').value || '4', 10);
      const bonus = parseInt(document.getElementById('calc-bonus').value || '0', 10);
      const pct = parseFloat(document.getElementById('calc-agent-pct').value || '7.0');

      try {
        const res = await fetch('/api/finance/psr-tax', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            league,
            transfer_fee_eur: fee,
            weekly_wage_eur: wage,
            contract_years: years,
            agent_fee_pct: pct,
            signing_bonus_eur: bonus
          })
        });
        const d = await res.json();
        box.innerHTML = `
          <div class="grid grid-cols-1 md:grid-cols-4 gap-2.5 mb-2.5">
            <div class="p-2.5 rounded-lg bg-[#12151c] border border-white/[0.04]">
              <div class="text-[11px] text-zinc-400">구단 연간 PSR 장부 비용</div>
              <div class="text-sm font-bold text-white mt-0.5">€${d.annual_psr_book_cost_eur.toLocaleString()} / 년</div>
              <div class="text-[10px] text-zinc-500 mt-0.5">이적료 상각: €${d.annual_transfer_amortization_eur.toLocaleString()}</div>
            </div>
            <div class="p-2.5 rounded-lg bg-[#12151c] border border-white/[0.04]">
              <div class="text-[11px] text-zinc-400">선수 세후 실수령액</div>
              <div class="text-sm font-bold text-emerald-400 mt-0.5">€${d.weekly_net_wage_eur.toLocaleString()}/주</div>
              <div class="text-[10px] text-zinc-500 mt-0.5">세전 연봉 €${d.annual_gross_wage_eur.toLocaleString()} · 세율 ${d.top_income_tax_rate_pct}%</div>
            </div>
            <div class="p-2.5 rounded-lg bg-[#12151c] border border-white/[0.04]">
              <div class="text-[11px] text-zinc-400">에이전트 수수료 (${d.agent_fee_pct}%)</div>
              <div class="text-sm font-bold text-zinc-200 mt-0.5">€${d.agent_commission_total_eur.toLocaleString()}</div>
              <div class="text-[10px] text-zinc-500 mt-0.5">사이닝 보너스: €${d.signing_bonus_eur.toLocaleString()}</div>
            </div>
            <div class="p-2.5 rounded-lg bg-[#12151c] border border-white/[0.04]">
              <div class="text-[11px] text-zinc-400">${d.contract_years}년 총 계약 비용</div>
              <div class="text-sm font-bold text-zinc-200 mt-0.5">€${d.total_deal_package_cost_eur.toLocaleString()}</div>
              <div class="text-[10px] text-zinc-500 mt-0.5">협상 관행: ${d.negotiation_basis}</div>
            </div>
          </div>
          <div class="text-xs text-zinc-400 bg-[#12151c] p-2.5 rounded-lg border border-white/[0.04]">
            리그 세제 정보: ${d.tax_regime_note}
          </div>
        `;
      } catch (e) {
        console.error(e);
      }
    }

    // -------------------------------------------------------------------------
    // Regulations Vector RAG Search
    // -------------------------------------------------------------------------
    async function runInteractiveRagSearch() {
      const query = document.getElementById('rag-search-input').value.trim();
      const sType = document.getElementById('rag-search-type').value;
      const pos = selectedPlayer ? selectedPlayer.position : 'RB';
      const res = await fetch('/api/rag/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, search_type: sType, position: pos, top_k: 4 })
      });
      const data = await res.json();
      const container = document.getElementById('rag-lab-results');

      if (data.search_type === 'LEGAL_REGULATIONS') {
        container.innerHTML = (data.results || []).map(r => `
          <div class="p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] space-y-1">
            <div class="flex justify-between items-center">
              <span class="text-xs font-semibold text-white">${r.title}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">
                유사도: ${r.similarity_score}
              </span>
            </div>
            <div class="text-[11px] text-zinc-400">출처: ${r.source_citation} (${r.effective_date})</div>
            <pre class="text-[11px] text-zinc-300 whitespace-pre-wrap font-sans mt-0.5">${r.content}</pre>
          </div>
        `).join('');
      } else {
        container.innerHTML = (data.results || []).map(r => `
          <div class="p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] space-y-1">
            <div class="flex justify-between items-center">
              <span class="text-xs font-semibold text-white">${r.club_name} (${r.league} · ${r.position})</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">
                유사도: ${r.tactical_similarity_score}
              </span>
            </div>
            <div class="text-xs text-zinc-300">${r.tactical_note}</div>
          </div>
        `).join('');
      }
    }

    // =======================================================================
    // API-Football Precision Features: Injury Verification & Prospect Onboarding
    // =======================================================================
    async function runPrecisionMedicalCheck() {
      const resContainer = document.getElementById('precision-medical-result');
      if (!resContainer) return;

      const playerName = CURRENT_PLAYER_NAME || document.getElementById('strat-target-name')?.innerText || '손흥민';
      resContainer.classList.remove('hidden');
      resContainer.innerHTML = `
        <div class="flex items-center gap-2 text-xs text-red-300">
          <svg class="animate-spin h-3.5 w-3.5 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
          </svg>
          <span>API-Football 공식 의무 기록 및 부상 데이터 실시간 인출 중... (${playerName})</span>
        </div>
      `;

      try {
        const resp = await fetch('/api/live/precision-check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_name: playerName })
        });
        const data = await resp.json();
        const inj = data.injuries || {};
        const count = inj.injuries_count || (inj.injuries ? inj.injuries.length : 0);
        const sourceLabel = inj.source || 'API-Football Official';
        const isFallback = inj.fallback_used;

        let itemsHtml = '';
        if (inj.injuries && inj.injuries.length > 0) {
          itemsHtml = `
            <div class="mt-2 space-y-1.5 max-h-40 overflow-y-auto pr-1">
              ${inj.injuries.slice(-6).reverse().map(i => `
                <div class="p-2 rounded-lg bg-red-950/30 border border-red-500/20 text-xs flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-1.5 h-1.5 rounded-full ${i.injury_type === 'Missing Fixture' ? 'bg-red-400' : 'bg-amber-400'}"></span>
                    <span class="font-semibold text-white">${i.reason}</span>
                    <span class="text-zinc-400 text-[11px]">(${i.injury_type})</span>
                  </div>
                  <span class="text-[11px] text-zinc-400 font-mono">${(i.fixture_date || '').split('T')[0]}</span>
                </div>
              `).join('')}
            </div>
          `;
        } else if (inj.summary) {
          itemsHtml = `<div class="mt-1 text-xs text-zinc-300 leading-relaxed">${inj.summary}</div>`;
        } else {
          itemsHtml = `<div class="mt-1 text-xs text-emerald-400 font-medium">✓ 현재 공식 결장 및 부상 의무 기록이 없습니다. (정상 출전 가능)</div>`;
        }

        resContainer.innerHTML = `
          <div class="flex items-center justify-between pb-2 border-b border-red-500/20">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-red-200">공식 의무 기록 리포트 (Official Medical Status)</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded ${isFallback ? 'bg-zinc-800 text-zinc-400' : 'bg-red-500/20 text-red-300 font-mono'}">
                ${sourceLabel}
              </span>
            </div>
            <button onclick="document.getElementById('precision-medical-result').classList.add('hidden')"
              class="text-[11px] text-zinc-400 hover:text-white">✕ 닫기</button>
          </div>
          <div class="pt-1">
            <div class="text-xs text-zinc-200">
              <span class="font-semibold text-white">${inj.official_name || playerName}</span>: 총 <span class="font-bold text-red-400">${count}건</span>의 의무 기록 확인
            </div>
            ${itemsHtml}
          </div>
        `;

        loadQuotaStatus();
      } catch (err) {
        resContainer.innerHTML = `
          <div class="text-xs text-red-400">부상 검증 중 통신 오류가 발생했습니다: ${err.message}</div>
        `;
      }
    }

    async function onboardExternalProspectUI() {
      const inputEl = document.getElementById('external-prospect-input');
      const btnEl = document.getElementById('btn-onboard-prospect');
      const resEl = document.getElementById('onboard-result-box');
      if (!inputEl || !resEl) return;

      const playerName = inputEl.value.trim();
      if (!playerName) {
        alert('유망주 이름을 입력해 주세요 (예: Seol, Yang Min-Hyeok, Estevao 등).');
        return;
      }

      btnEl.disabled = true;
      btnEl.innerHTML = `
        <svg class="animate-spin h-3 w-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        <span>인출 중...</span>
      `;
      resEl.classList.remove('hidden');
      resEl.innerHTML = `<span class="text-zinc-400 text-xs">API-Football 전 세계 1,100개 리그 DB에서 '${playerName}' 공식 프로필 및 2024 실측 스탯 인출 중...</span>`;

      try {
        const resp = await fetch('/api/prospects/onboard-external', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ player_name: playerName, season: 2024 })
        });
        const data = await resp.json();

        if (resp.ok && data.success) {
          resEl.innerHTML = `
            <div class="flex items-center gap-3">
              ${data.photo ? `<img src="${data.photo}" alt="${data.name}" class="w-10 h-10 rounded-full border border-emerald-500/40 object-cover bg-zinc-900" />` : ''}
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-white">${data.name} (${data.name_ko})</span>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-semibold">${data.league}</span>
                </div>
                <div class="text-[11px] text-zinc-300 mt-0.5">
                  소속: <span class="text-white font-medium">${data.club}</span> · 포지션: ${data.position} · 나이: ${data.age}세 · 국적: ${data.nationality}
                </div>
                <div class="text-[10px] text-zinc-400 mt-0.5 font-mono">
                  실측 출전: ${data.appearances}경기 ${data.minutes}분 (${data.goals}골 ${data.assists}도움, 평점: ${data.rating})
                </div>
              </div>
            </div>
            <div class="mt-2 text-[11px] text-emerald-400 font-medium">
              ✓ SQLite DB 및 벡터 스토어 인덱싱 완료! 이제 스카우팅 및 협상 데스크에서 바로 선택할 수 있습니다.
            </div>
          `;
          inputEl.value = '';
          await loadPlayers();
          loadQuotaStatus();
        } else {
          resEl.innerHTML = `<div class="text-xs text-amber-400">등록 실패: ${data.detail || data.error || '선수 정보를 찾을 수 없습니다.'}</div>`;
        }
      } catch (err) {
        resEl.innerHTML = `<div class="text-xs text-red-400">등록 중 통신 오류 발생: ${err.message}</div>`;
      } finally {
        btnEl.disabled = false;
        btnEl.innerHTML = `<span>등록</span>`;
      }
    }

    // =========================================================================
    // 2D Tactical Grid Match Engine & Real Highlight Analytics Module
    // (StatsBomb 120x80m Open Data, FM Autonomous Grid AI & Video Sync)
    // =========================================================================
    let tacticsCanvas = null;
    let tacticsCtx = null;
    let tacticsData = null;
    let currentPlayerTacticsData = null;
    let tacticsMode = 'match'; // 'match' | 'player' | 'sim'
    let isTacticsRunning = true;
    let tacticsSpeed = 1;
    let tacticsAnimId = null;
    let tacticsClockSeconds = 5428; // 90:28
    let tacticsSelectedPlayerId = 'H11'; // 손흥민
    let tacticsGoalBannerTimer = 0;

    let tacticsOverlays = {
      grid: true,
      zones: false,
      fov: true,
      spotlight: true,
      actionMap: true
    };

    let isReelPlaying = false;
    let reelStep = 0;
    let reelTransitionTimer = 0;
    let hoveredActionPin = null;

    const TACTICS_PITCH_MARGIN = 32;
    let TACTICS_PITCH_W = 1016;
    let TACTICS_PITCH_H = 596;
    const TACTICS_GRID_COLS = 18;
    const TACTICS_GRID_ROWS = 12;
    let TACTICS_CELL_W = TACTICS_PITCH_W / TACTICS_GRID_COLS;
    let TACTICS_CELL_H = TACTICS_PITCH_H / TACTICS_GRID_ROWS;

    let tacticsTrajectories = [];
    let tacticsPlayers = [];
    let tacticsBall = {
      x: 0, y: 0, vx: 0, vy: 0,
      owner: null, inFlight: false,
      lastTouchTeam: 'home',
      tx: 0, ty: 0
    };

    let activeHighlightAnim = null; // Multi-step animation controller
    let currentReplayContext = { mode: 'match', highlightId: 'goal_kor_02', momentIdx: 0, playerName: null };
    let livingMatchTimer = 0;
    let livingBallOwnerId = null;
    let livingPassCooldown = 0;

    // Team Templates for Simulation & Base Formation (2022 World Cup Kor vs Por)
    const TACTICS_HOME_ROSTER = [
      { id: 'H1',  num: 1,  name: '김승규', pos: 'GK', col: 0.8,  row: 5.5, spd: 68, pas: 72, def: 88 },
      { id: 'H2',  num: 15, name: '김문환', pos: 'RB', col: 3.5,  row: 1.5, spd: 82, pas: 76, def: 78 },
      { id: 'H3',  num: 4,  name: '김민재', pos: 'CB', col: 3.0,  row: 4.2, spd: 86, pas: 82, def: 93 },
      { id: 'H4',  num: 19, name: '김영권', pos: 'CB', col: 3.0,  row: 6.8, spd: 74, pas: 80, def: 84 },
      { id: 'H5',  num: 3,  name: '김진수', pos: 'LB', col: 3.5,  row: 9.5, spd: 80, pas: 78, def: 77 },
      { id: 'H6',  num: 5,  name: '정우영', pos: 'DM', col: 6.2,  row: 4.3, spd: 72, pas: 83, def: 82 },
      { id: 'H7',  num: 6,  name: '황인범', pos: 'DM', col: 6.5,  row: 6.7, spd: 78, pas: 88, def: 79 },
      { id: 'H8',  num: 18, name: '이강인', pos: 'RW', col: 10.5, row: 2.2, spd: 82, pas: 94, def: 60 },
      { id: 'H9',  num: 10, name: '이재성', pos: 'AM', col: 10.0, row: 5.5, spd: 78, pas: 85, def: 74 },
      { id: 'H10', num: 11, name: '황희찬', pos: 'LW', col: 11.2, row: 8.8, spd: 92, pas: 78, def: 58 },
      { id: 'H11', num: 7,  name: '손흥민', pos: 'ST', col: 13.5, row: 5.5, spd: 93, pas: 86, def: 52 }
    ];

    const TACTICS_AWAY_ROSTER = [
      { id: 'A1',  num: 22, name: '디.코스타', pos: 'GK', col: 16.5, row: 5.5, spd: 68, pas: 76, def: 88 },
      { id: 'A2',  num: 2,  name: '달로트',   pos: 'RB', col: 13.5, row: 9.2, spd: 88, pas: 82, def: 80 },
      { id: 'A3',  num: 3,  name: '페페',     pos: 'CB', col: 14.5, row: 6.8, spd: 76, pas: 78, def: 91 },
      { id: 'A4',  num: 24, name: '안.실바', pos: 'CB', col: 14.5, row: 4.2, spd: 80, pas: 80, def: 84 },
      { id: 'A5',  num: 20, name: '칸셀루',   pos: 'LB', col: 13.5, row: 1.8, spd: 89, pas: 85, def: 79 },
      { id: 'A6',  num: 18, name: '네베스',   pos: 'DM', col: 11.2, row: 5.5, spd: 74, pas: 89, def: 82 },
      { id: 'A7',  num: 23, name: '누네스',   pos: 'CM', col: 9.2,  row: 7.2, spd: 84, pas: 83, def: 78 },
      { id: 'A8',  num: 16, name: '비티냐',   pos: 'CM', col: 9.2,  row: 3.8, spd: 80, pas: 88, def: 76 },
      { id: 'A9',  num: 17, name: '주앙 마리우', pos: 'RW', col: 7.0, row: 8.8, spd: 78, pas: 84, def: 65 },
      { id: 'A10', num: 21, name: '호르타',   pos: 'LW', col: 7.0,  row: 2.2, spd: 84, pas: 80, def: 62 },
      { id: 'A11', num: 7,  name: '호날두',   pos: 'ST', col: 4.5,  row: 5.5, spd: 82, pas: 78, def: 42 }
    ];

    function tacticsGridToPixel(col, row) {
      return {
        x: TACTICS_PITCH_MARGIN + (col + 0.5) * TACTICS_CELL_W,
        y: TACTICS_PITCH_MARGIN + (row + 0.5) * TACTICS_CELL_H
      };
    }

    function tacticsPixelToGrid(x, y) {
      const col = Math.max(0, Math.min(TACTICS_GRID_COLS - 1, Math.floor((x - TACTICS_PITCH_MARGIN) / TACTICS_CELL_W)));
      const row = Math.max(0, Math.min(TACTICS_GRID_ROWS - 1, Math.floor((y - TACTICS_PITCH_MARGIN) / TACTICS_CELL_H)));
      return { col, row };
    }

    // Convert StatsBomb 120m x 80m coordinate to Canvas Pixel
    function statsBombToPixel(sbX, sbY) {
      const col = (sbX / 120.0) * TACTICS_GRID_COLS - 0.5;
      const row = (sbY / 80.0) * TACTICS_GRID_ROWS - 0.5;
      return tacticsGridToPixel(col, row);
    }

    async function initTacticsDesk() {
      if (!tacticsCanvas) {
        tacticsCanvas = document.getElementById('pitchCanvasTactics');
        if (!tacticsCanvas) return;
        tacticsCtx = tacticsCanvas.getContext('2d');

        TACTICS_PITCH_W = tacticsCanvas.width - TACTICS_PITCH_MARGIN * 2;
        TACTICS_PITCH_H = tacticsCanvas.height - TACTICS_PITCH_MARGIN * 2;
        TACTICS_CELL_W = TACTICS_PITCH_W / TACTICS_GRID_COLS;
        TACTICS_CELL_H = TACTICS_PITCH_H / TACTICS_GRID_ROWS;

        // Canvas click handler for player selection & Action Pin interaction
        tacticsCanvas.addEventListener('click', (e) => {
          const rect = tacticsCanvas.getBoundingClientRect();
          const scaleX = tacticsCanvas.width / rect.width;
          const scaleY = tacticsCanvas.height / rect.height;
          const clickX = (e.clientX - rect.left) * scaleX;
          const clickY = (e.clientY - rect.top) * scaleY;

          // 1. Check if Action Map pin was clicked
          if (tacticsOverlays.actionMap && currentPlayerTacticsData && currentPlayerTacticsData.action_map) {
            for (const act of currentPlayerTacticsData.action_map) {
              const pt = statsBombToPixel(act.location[0], act.location[1]);
              if (Math.hypot(pt.x - clickX, pt.y - clickY) < 22) {
                if (act.highlight_idx !== undefined) {
                  playTargetPlayerHighlight(act.highlight_idx);
                  updateCommentary(act.type, `[📍 활약 구역 선택] ${act.time_str} ${act.title} (${act.zone}) 전술 리플레이 실행!`);
                  return;
                }
              }
            }
          }

          // 2. Find clicked player
          let closestPlayer = null;
          let minDist = 30;
          tacticsPlayers.forEach(p => {
            const dist = Math.hypot(p.x - clickX, p.y - clickY);
            if (dist < minDist) {
              minDist = dist;
              closestPlayer = p;
            }
          });

          if (closestPlayer) {
            tacticsSelectedPlayerId = closestPlayer.id;
            updateCommentary('TACTIC', `${closestPlayer.team === 'home' ? '대한민국' : '포르투갈'} #${closestPlayer.num} ${closestPlayer.name} (${closestPlayer.pos}) 선택됨. 그리드 [${closestPlayer.baseCol.toFixed(1)}, ${closestPlayer.baseRow.toFixed(1)}]`);
          }
        });

        // Canvas hover handler for Action Map Pins & Interactive Cursor
        tacticsCanvas.addEventListener('mousemove', (e) => {
          const rect = tacticsCanvas.getBoundingClientRect();
          const scaleX = tacticsCanvas.width / rect.width;
          const scaleY = tacticsCanvas.height / rect.height;
          const mouseX = (e.clientX - rect.left) * scaleX;
          const mouseY = (e.clientY - rect.top) * scaleY;

          hoveredActionPin = null;
          if (tacticsOverlays.actionMap && currentPlayerTacticsData && currentPlayerTacticsData.action_map) {
            for (const act of currentPlayerTacticsData.action_map) {
              const pt = statsBombToPixel(act.location[0], act.location[1]);
              if (Math.hypot(pt.x - mouseX, pt.y - mouseY) < 20) {
                hoveredActionPin = act;
                break;
              }
            }
          }
          tacticsCanvas.style.cursor = hoveredActionPin ? 'pointer' : 'default';
        });

        tacticsCanvas.addEventListener('mouseleave', () => {
          hoveredActionPin = null;
          tacticsCanvas.style.cursor = 'default';
        });
      }

      // Fetch Real Highlights Data from Backend
      if (!tacticsData) {
        try {
          const res = await fetch('/api/tactics/match-highlights');
          if (res.ok) {
            tacticsData = await res.json();
            renderTacticsEventLog();
          }
        } catch (err) {
          console.error('Tactics Data load error:', err);
        }
      }

      // If a player is selected from Scouting Desk, load that player's club match & tactical analysis
      if (selectedPlayer && (!currentPlayerTacticsData || (currentPlayerTacticsData.player_info && currentPlayerTacticsData.player_info.name !== selectedPlayer.name && currentPlayerTacticsData.player_info.name_ko !== selectedPlayer.name_ko))) {
        await loadPlayerTacticsHighlights(selectedPlayer.name || selectedPlayer.name_ko);
      } else if (!currentPlayerTacticsData) {
        initTacticsPlayers();
        // Start by loading the iconic winning goal moment (90:28 Hwang Hee-Chan & Son Heung-Min)
        playMatchHighlight('goal_kor_02');
      }

      if (!tacticsAnimId) {
        tacticsLoop();
      }
    }

    function initTacticsPlayers() {
      tacticsPlayers = [];
      TACTICS_HOME_ROSTER.forEach(p => {
        const pt = tacticsGridToPixel(p.col, p.row);
        tacticsPlayers.push({
          ...p,
          team: 'home',
          baseCol: p.col,
          baseRow: p.row,
          x: pt.x,
          y: pt.y,
          tx: pt.x,
          ty: pt.y,
          angle: 0,
          stamina: 96
        });
      });

      TACTICS_AWAY_ROSTER.forEach(p => {
        const pt = tacticsGridToPixel(p.col, p.row);
        tacticsPlayers.push({
          ...p,
          team: 'away',
          baseCol: p.col,
          baseRow: p.row,
          x: pt.x,
          y: pt.y,
          tx: pt.x,
          ty: pt.y,
          angle: Math.PI,
          stamina: 94
        });
      });

      const ballPt = tacticsGridToPixel(9.0, 5.5);
      tacticsBall.x = ballPt.x;
      tacticsBall.y = ballPt.y;
      tacticsBall.vx = 0;
      tacticsBall.vy = 0;
      tacticsBall.owner = null;
      tacticsBall.inFlight = false;
    }

    function renderTacticsEventLog() {
      const logEl = document.getElementById('tactics-event-log');
      if (!logEl || !tacticsData) return;

      let html = '';
      if (tacticsData.key_match_highlights) {
        tacticsData.key_match_highlights.forEach(h => {
          const isKor = h.team === 'home';
          html += `
            <div onclick="playMatchHighlight('${h.id}')"
              class="p-2 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.04] cursor-pointer transition flex items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="font-mono text-[11px] font-bold ${isKor ? 'text-emerald-400' : 'text-rose-400'}">${h.display_time}</span>
                <span class="font-semibold text-white">${h.title}</span>
              </div>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-zinc-800 text-zinc-400 font-mono">xG ${h.xg.toFixed(2)}</span>
            </div>
          `;
        });
      }

      if (tacticsData.player_moments) {
        tacticsData.player_moments.forEach(pm => {
          pm.moments.forEach((m, idx) => {
            html += `
              <div onclick="playPlayerMoment('${pm.player_name}', ${idx})"
                class="p-2 rounded-lg bg-[#0a0c10] hover:bg-zinc-800 border border-white/[0.03] cursor-pointer transition flex items-center justify-between gap-2 text-[11px]">
                <div class="flex items-center gap-2">
                  <span class="font-mono text-zinc-400">${m.time}</span>
                  <span class="text-zinc-300 font-medium">${pm.player_name}: ${m.title}</span>
                </div>
                <span class="text-[10px] text-zinc-500 font-mono">${m.type}</span>
              </div>
            `;
          });
        });
      }

      logEl.innerHTML = html;
    }

    // Play Match Highlight (100% Real StatsBomb Coordinates & Animation)
    function playMatchHighlight(highlightId) {
      if (!tacticsData || !tacticsData.key_match_highlights) return;
      const h = tacticsData.key_match_highlights.find(item => item.id === highlightId);
      if (!h) return;

      isTacticsRunning = true;
      const icon = document.getElementById('btn-tactics-play-icon');
      const text = document.getElementById('btn-tactics-play-text');
      if (icon && text) {
        icon.textContent = '⏸️';
        text.textContent = '일시정지';
      }

      currentReplayContext = { mode: 'match', highlightId: highlightId, momentIdx: 0, playerName: null };
      tacticsTrajectories = [];
      activeHighlightAnim = null;

      // Update UI Clock, Commentary & Scores
      document.getElementById('tactics-clock').textContent = h.display_time;
      updateCommentary('HIGHLIGHT', `[${h.display_time}] ${h.title}: ${h.description}`);

      if (h.id === 'goal_por_01') {
        document.getElementById('tactics-score-home').textContent = '0';
        document.getElementById('tactics-score-away').textContent = '1';
        seekTacticsVideo(293); // 04:53 in official match
        animateHortaGoal(h);
      } else if (h.id === 'goal_kor_01') {
        document.getElementById('tactics-score-home').textContent = '1';
        document.getElementById('tactics-score-away').textContent = '1';
        seekTacticsVideo(1603); // 26:43
        animateKimYoungGwonGoal(h);
      } else if (h.id === 'goal_kor_02') {
        document.getElementById('tactics-score-home').textContent = '2';
        document.getElementById('tactics-score-away').textContent = '1';
        seekTacticsVideo(5428); // 90:28
        animateHwangHeeChanWinner(h);
      }
    }

    // Goal 1: Horta 04:53
    function animateHortaGoal(h) {
      const startPt = statsBombToPixel(h.start_location[0], h.start_location[1]);
      const dalot = tacticsPlayers.find(p => p.num === 2 && p.team === 'away');
      const horta = tacticsPlayers.find(p => p.num === 21 && p.team === 'away');
      const crossStart = { x: startPt.x + 55, y: startPt.y + 70 };
      const crossEnd = { x: startPt.x + 10, y: startPt.y + 15 };

      if (dalot) {
        dalot.x = crossStart.x;
        dalot.y = crossStart.y;
      }
      if (horta) {
        horta.x = startPt.x - 30;
        horta.y = startPt.y - 12;
        horta.angle = Math.PI;
        tacticsSelectedPlayerId = horta.id;
      }

      tacticsBall.x = crossStart.x;
      tacticsBall.y = crossStart.y;

      activeHighlightAnim = {
        type: 'WC_HORTA',
        step: 0,
        timer: 0,
        targetPlayer: horta,
        tacticalTag: '[🚀 달로트 우측면 돌파 & 컷백 크로스]',
        tagColor: '#f59e0b',
        dalot: dalot,
        horta: horta,
        crossPt: crossEnd,
        finishPt: startPt,
        h: h
      };
    }

    // Goal 2: Kim Young-Gwon 26:43 Equalizer
    function animateKimYoungGwonGoal(h) {
      const cornerPt = statsBombToPixel(h.corner_location[0], h.corner_location[1]);
      const finishPt = statsBombToPixel(h.start_location[0], h.start_location[1]);
      const deflectPt = { x: finishPt.x - 18, y: finishPt.y - 12 };

      const kangin = tacticsPlayers.find(p => p.num === 18 && p.team === 'home');
      const kim = tacticsPlayers.find(p => p.num === 19 && p.team === 'home');
      const ronaldo = tacticsPlayers.find(p => p.num === 7 && p.team === 'away');

      if (kangin) { kangin.x = cornerPt.x; kangin.y = cornerPt.y; }
      if (ronaldo) { ronaldo.x = deflectPt.x; ronaldo.y = deflectPt.y; }
      if (kim) {
        kim.x = finishPt.x - 20;
        kim.y = finishPt.y + 15;
        tacticsSelectedPlayerId = kim.id;
      }

      tacticsBall.x = cornerPt.x;
      tacticsBall.y = cornerPt.y;

      activeHighlightAnim = {
        type: 'WC_KIM',
        step: 0,
        timer: 0,
        targetPlayer: kim,
        tacticalTag: '[🎯 이강인 택배 코너킥 & 문전 쇄도]',
        tagColor: '#38bdf8',
        kangin: kangin,
        kim: kim,
        ronaldo: ronaldo,
        cornerPt: cornerPt,
        deflectPt: deflectPt,
        finishPt: finishPt,
        h: h
      };
    }

    // Goal 3: Hwang Hee-Chan 90:28 Winner (Son Heung-Min 70m Sprint & Nutmeg Pass)
    function animateHwangHeeChanWinner(h) {
      const son = tacticsPlayers.find(p => p.num === 7 && p.team === 'home');
      const hwang = tacticsPlayers.find(p => p.num === 11 && p.team === 'home');
      const dalot = tacticsPlayers.find(p => p.num === 2 && p.team === 'away');
      const pepe = tacticsPlayers.find(p => p.num === 3 && p.team === 'away');
      const keeper = tacticsPlayers.find(p => p.num === 22 && p.team === 'away');

      const waypoints = h.son_carry_coords.map(pt => statsBombToPixel(pt.x, pt.y));
      const shotPt = statsBombToPixel(h.shot_location[0], h.shot_location[1]);
      const passStartPt = statsBombToPixel(h.pass_start[0], h.pass_start[1]);

      // Place defenders in freeze frame
      if (dalot) { const pt = tacticsGridToPixel(15.1, 7.9); dalot.x = pt.x; dalot.y = pt.y; }
      if (pepe) { const pt = tacticsGridToPixel(16.5, 7.2); pepe.x = pt.x; pepe.y = pt.y; }
      if (keeper) { const pt = tacticsGridToPixel(17.5, 6.0); keeper.x = pt.x; keeper.y = pt.y; }

      // Setup multi-step sequence
      activeHighlightAnim = {
        type: 'WC_HWANG',
        step: 0,
        timer: 0,
        targetPlayer: son,
        tacticalTag: '[⚡ 손흥민 70m 단독 폭풍 드리블 질주]',
        tagColor: '#fbbf24',
        waypoints: waypoints,
        passStart: passStartPt,
        shotPt: shotPt,
        son: son,
        hwang: hwang,
        goalText: '황희찬 극장 역전 결승골 (손흥민 70m 어시스트!)'
      };

      if (son) {
        son.x = waypoints[0].x;
        son.y = waypoints[0].y;
        tacticsSelectedPlayerId = son.id;
      }
      if (hwang) {
        const hwangStart = tacticsGridToPixel(12.0, 7.2);
        hwang.x = hwangStart.x;
        hwang.y = hwangStart.y;
      }

      tacticsBall.x = waypoints[0].x;
      tacticsBall.y = waypoints[0].y;
    }

    // =========================================================================
    // FM 2D Realistic Team Unit Movement Engine
    // All 22 players shift compactness, press/drop deep, and micro-shuffle with the ball
    // =========================================================================
    function updateFMTeamUnitMovement(ballX, ballY, heroIds = []) {
      if (!tacticsPlayers || tacticsPlayers.length === 0) return;
      const pitchLeft = TACTICS_PITCH_MARGIN + 12;
      const pitchRight = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 12;
      const pitchTop = TACTICS_PITCH_MARGIN + 14;
      const pitchBottom = TACTICS_PITCH_MARGIN + TACTICS_PITCH_H - 14;

      const pitchMidX = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W * 0.5;
      const pitchMidY = TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.5;

      const ballProgX = (ballX - TACTICS_PITCH_MARGIN) / TACTICS_PITCH_W; // 0 (left goal) to 1 (right goal)
      const ballOffsetY = (ballY - pitchMidY) / (TACTICS_PITCH_H * 0.5); // -1 (top) to +1 (bottom)

      const t = Date.now() * 0.003;

      tacticsPlayers.forEach(p => {
        if (heroIds.includes(p.id)) return;

        const basePt = tacticsGridToPixel(p.baseCol, p.baseRow);
        let targetX = basePt.x;
        let targetY = basePt.y;

        const isHome = p.team === 'home';
        const isGk = p.pos === 'GK';

        if (isGk) {
          // Goalkeeper positioning relative to ball
          targetY = pitchMidY + ballOffsetY * 24;
          targetX = isHome ? (TACTICS_PITCH_MARGIN + 24) : (pitchRight - 14);
        } else {
          // 1. Tactical Unit Compression & Line Shifting:
          // Attacking team pushes up lines; Defending team drops back
          if (isHome) {
            const pushDist = (ballProgX - 0.5) * (p.pos.includes('B') ? 48 : 72);
            targetX = basePt.x + pushDist;
          } else {
            const dropDist = (ballProgX - 0.5) * (p.pos.includes('B') ? 38 : 58);
            targetX = basePt.x + dropDist;
          }

          // 2. Lateral Touchline Compactness (Team shifts toward ball side)
          const lateralShift = ballOffsetY * 26 * (p.pos.includes('W') ? 0.65 : 1.0);
          targetY = basePt.y + lateralShift;

          // 3. FM Footwork & Shuffle Cadence (Living players never stand frozen)
          const shufflePhase = p.num * 1.73;
          const microX = Math.sin(t * 1.7 + shufflePhase) * 2.4;
          const microY = Math.cos(t * 1.3 + shufflePhase) * 1.9;
          targetX += microX;
          targetY += microY;

          // 4. Proximity Pressing & Covering Reactions
          const distToBall = Math.hypot(ballX - p.x, ballY - p.y);
          if (distToBall < 120) {
            if (!isHome) {
              // Defenders step out to jockey / pressure dribbler
              const ang = Math.atan2(ballY - p.y, ballX - p.x);
              targetX += Math.cos(ang) * 14;
              targetY += Math.sin(ang) * 14;
            } else {
              // Teammates offer passing angle
              const ang = Math.atan2(p.y - ballY, p.x - ballX);
              targetX += Math.cos(ang) * 9;
              targetY += Math.sin(ang) * 9;
            }
          }
        }

        targetX = Math.max(pitchLeft, Math.min(pitchRight, targetX));
        targetY = Math.max(pitchTop, Math.min(pitchBottom, targetY));

        const lerp = isGk ? 0.05 : 0.038;
        p.x += (targetX - p.x) * lerp * tacticsSpeed;
        p.y += (targetY - p.y) * lerp * tacticsSpeed;

        // Player vision tracking ball
        p.angle = Math.atan2(ballY - p.y, ballX - p.x);
      });
    }

    // FM Reel Continuous Playback Engine
    function playPlayerFullMatchReel() {
      if (!currentPlayerTacticsData || !currentPlayerTacticsData.key_match_highlights) return;
      isReelPlaying = true;
      reelStep = 0;
      updateCommentary('REEL', `[🎬 90분 종합 활약상 연속 재생] ${currentPlayerTacticsData.player_info.name_ko}의 90분 풀타임 핵심 시그니처 시퀀스(득점·킬패스·볼탈환)를 연속 재생합니다.`);
      renderPlayerChapterButtons(currentPlayerTacticsData);
      playTargetPlayerHighlight(0);
    }

    function advanceFMReel() {
      if (!isReelPlaying || !currentPlayerTacticsData || !currentPlayerTacticsData.key_match_highlights) return;
      reelStep++;
      if (reelStep < currentPlayerTacticsData.key_match_highlights.length) {
        const nextM = currentPlayerTacticsData.key_match_highlights[reelStep];
        updateCommentary('REEL', `[🕒 MATCH CLOCK 전진...] ➔ ${nextM.display_time} [${nextM.title}] 로 전환합니다.`);
        setTimeout(() => {
          if (isReelPlaying) {
            playTargetPlayerHighlight(reelStep);
          }
        }, 1400);
      } else {
        isReelPlaying = false;
        renderPlayerChapterButtons(currentPlayerTacticsData);
        const s = currentPlayerTacticsData.match_summary || {};
        const pKo = currentPlayerTacticsData.player_info.name_ko || currentPlayerTacticsData.player_info.name;
        updateCommentary('SUMMARY', `[⭐ 90분 전술 분석 완료] ${pKo} FM 평점: ${s.rating || '8.7'}${s.mom ? ' (MoM 선정)' : ''} | 볼터치 ${s.touches || 74}회, 키패스 ${s.key_passes || 4}회, 패스 성공률 ${s.pass_accuracy || 89}%, 리커버리 ${s.recoveries || 6}회, 활동량 ${s.distance_km || 11.4}km.`);
      }
    }

    // Master step-by-step highlight animation engine (Authentic Multi-Phase Play Sequences)
    function updateHighlightAnimation() {
      if (!activeHighlightAnim) return;
      const anim = activeHighlightAnim;
      anim.timer += tacticsSpeed;

      // 1. Organic FM Team Unit Movement for all other players
      const heroIds = [];
      if (anim.targetPlayer) heroIds.push(anim.targetPlayer.id);
      if (anim.buildupPasser) heroIds.push(anim.buildupPasser.id);
      if (anim.assister) heroIds.push(anim.assister.id);
      if (anim.oppDefender) heroIds.push(anim.oppDefender.id);
      if (anim.oppGk) heroIds.push(anim.oppGk.id);
      if (anim.forwardRunner) heroIds.push(anim.forwardRunner.id);
      if (anim.wingSupport) heroIds.push(anim.wingSupport.id);
      if (anim.oppCarrier) heroIds.push(anim.oppCarrier.id);
      if (anim.son) heroIds.push(anim.son.id);
      if (anim.hwang) heroIds.push(anim.hwang.id);
      if (anim.dalot) heroIds.push(anim.dalot.id);
      if (anim.horta) heroIds.push(anim.horta.id);
      if (anim.kangin) heroIds.push(anim.kangin.id);
      if (anim.kim) heroIds.push(anim.kim.id);
      if (anim.ronaldo) heroIds.push(anim.ronaldo.id);

      updateFMTeamUnitMovement(tacticsBall.x, tacticsBall.y, heroIds);

      // ----------------------------------------------------
      // TYPE: TARGET_GOAL (Multi-Pass Buildup -> Assist Cross -> Box Sprint -> Volley Finish -> Net & Celebration)
      // ----------------------------------------------------
      if (anim.type === 'TARGET_GOAL') {
        const pKo = (currentPlayerTacticsData && currentPlayerTacticsData.player_info)
          ? (currentPlayerTacticsData.player_info.name_ko || currentPlayerTacticsData.player_info.name)
          : anim.targetPlayer.name;

        // Step 0: 후방/중원 1차 빌드업 전개 (80 frames ~ 1.33s)
        if (anim.step === 0) {
          anim.tacticalTag = '[📐 시야 & 1차 빌드업 전개]';
          anim.tagColor = '#38bdf8';

          if (anim.buildupPasser) {
            tacticsSelectedPlayerId = anim.buildupPasser.id;
            anim.buildupPasser.x += 0.25 * tacticsSpeed;
            anim.buildupPasser.angle = Math.atan2(anim.assisterStartPt.y - anim.buildupPasser.y, anim.assisterStartPt.x - anim.buildupPasser.x);
          }

          const passProg = Math.min(1.0, anim.timer / 80);
          tacticsBall.x = anim.buildupStartPt.x + (anim.assisterStartPt.x - anim.buildupStartPt.x) * passProg;
          tacticsBall.y = anim.buildupStartPt.y + (anim.assisterStartPt.y - anim.buildupStartPt.y) * passProg;

          if (anim.assister) {
            anim.assister.x += (anim.assisterStartPt.x - anim.assister.x) * 0.04 * tacticsSpeed;
            anim.assister.y += (anim.assisterStartPt.y - anim.assister.y) * 0.04 * tacticsSpeed;
            anim.assister.angle = Math.atan2(anim.buildupStartPt.y - anim.assister.y, anim.buildupStartPt.x - anim.assister.x);
          }

          anim.targetPlayer.x += (anim.targetStartPt.x + 10 - anim.targetPlayer.x) * 0.02 * tacticsSpeed;

          if (anim.timer >= 80) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.buildupStartPt.x, y1: anim.buildupStartPt.y,
              x2: anim.assisterStartPt.x, y2: anim.assisterStartPt.y,
              color: '#38bdf8', dashed: true, alpha: 1.0,
              label: `[빌드업] #${anim.buildupPasser ? anim.buildupPasser.num : '6'} ➔ #${anim.assister ? anim.assister.num : '7'}`
            });
            updateCommentary('BUILDUP', `[1단계 빌드업 전개] #${anim.buildupPasser ? anim.buildupPasser.num : '6'} ${anim.buildupPasser ? anim.buildupPasser.name : '미드필더'} ➔ #${anim.assister ? anim.assister.num : '7'} ${anim.assister ? anim.assister.name : '윙어'} 파이널 서드 전진 연계 패스 성공!`);
          }
        }
        // Step 1: 파이널 서드 연계 및 타겟 공격수 오프더볼 공간 침투 (110 frames ~ 1.83s)
        else if (anim.step === 1) {
          tacticsSelectedPlayerId = anim.targetPlayer.id;
          anim.tacticalTag = '[🚀 폭발적 가속 오프더볼 공간 침투]';
          anim.tagColor = '#fbbf24';

          // Assister carries forward to crossing point with FM foot touch cadence
          if (anim.assister) {
            anim.assister.x += (anim.assisterCrossPt.x - anim.assister.x) * 0.045 * tacticsSpeed;
            anim.assister.y += (anim.assisterCrossPt.y - anim.assister.y) * 0.045 * tacticsSpeed;
            anim.assister.angle = Math.atan2(anim.actionPt.y - anim.assister.y, anim.actionPt.x - anim.assister.x);
          }

          // Target Player makes explosive off-the-ball sprint run into penalty box
          anim.targetPlayer.x += (anim.actionPt.x - anim.targetPlayer.x) * 0.045 * tacticsSpeed;
          anim.targetPlayer.y += (anim.actionPt.y - anim.targetPlayer.y) * 0.045 * tacticsSpeed;
          anim.targetPlayer.angle = Math.atan2(anim.goalPt.y - anim.targetPlayer.y, anim.goalPt.x - anim.targetPlayer.x);

          if (anim.oppDefender) {
            anim.oppDefender.x += (anim.actionPt.x + 20 - anim.oppDefender.x) * 0.025 * tacticsSpeed;
            anim.oppDefender.y += (anim.actionPt.y + 12 - anim.oppDefender.y) * 0.025 * tacticsSpeed;
          }

          // In first phase, ball is with assister dribbling with touch pulses. In second phase, cross whips into box.
          if (anim.timer <= 45) {
            if (anim.assister) {
              const touchPhase = (anim.timer % 16) / 16;
              const touchPush = Math.sin(touchPhase * Math.PI) * 4.5;
              const swayY = Math.sin(anim.timer * 0.3) * 2.2;
              tacticsBall.x = anim.assister.x + 7 + touchPush;
              tacticsBall.y = anim.assister.y + swayY;
            }
          } else {
            const crossProg = Math.min(1.0, (anim.timer - 45) / 65);
            tacticsBall.x = anim.assisterCrossPt.x + (anim.actionPt.x - anim.assisterCrossPt.x) * crossProg;
            tacticsBall.y = anim.assisterCrossPt.y + (anim.actionPt.y - anim.assisterCrossPt.y) * crossProg;
          }

          if (anim.timer >= 110) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.assisterCrossPt.x, y1: anim.assisterCrossPt.y,
              x2: anim.actionPt.x, y2: anim.actionPt.y,
              color: '#f59e0b', dashed: true, alpha: 1.0,
              label: `[어시스트 컷백] #${anim.assister ? anim.assister.num : '7'} ➔ #${anim.targetPlayer.num} ${pKo}`
            });
            updateCommentary('ASSIST', `[2단계 어시스트] #${anim.assister ? anim.assister.num : '7'} ${anim.assister ? anim.assister.name : '윙어'}의 정밀 컷백 크로스! #${anim.targetPlayer.num} ${pKo} 수비 뒷공간 침투 쇄도!`);
          }
        }
        // Step 2: 결정적 논스톱 다이렉트 슈팅 & 골키퍼 다이빙 (60 frames ~ 1.0s)
        else if (anim.step === 2) {
          anim.tacticalTag = '[⚡ 시그니처 원터치 다이렉트 피니시]';
          anim.tagColor = '#10b981';

          const shotProg = Math.min(1.0, anim.timer / 60);
          tacticsBall.x = anim.actionPt.x + (anim.goalPt.x - anim.actionPt.x) * shotProg;
          tacticsBall.y = anim.actionPt.y + (anim.goalPt.y - anim.actionPt.y) * shotProg;

          if (anim.oppGk) {
            anim.oppGk.x += (anim.goalPt.x - 14 - anim.oppGk.x) * 0.04 * tacticsSpeed;
            anim.oppGk.y += (anim.goalPt.y - anim.oppGk.y) * 0.04 * tacticsSpeed;
          }

          if (anim.timer >= 60) {
            anim.step = 3;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.actionPt.x, y1: anim.actionPt.y,
              x2: anim.goalPt.x, y2: anim.goalPt.y,
              color: '#10b981', dashed: false, alpha: 1.0,
              label: `[GOAL!] 다이렉트 득점 (xG ${anim.m.xg})`
            });
            document.getElementById('tactics-score-home').textContent = '2';
            document.getElementById('tactics-score-away').textContent = '1';
            triggerGoalBanner(`${pKo} 시그니처 득점! (xG ${anim.m.xg})`);
            updateCommentary('SHOT', `[3단계 슈팅] #${anim.targetPlayer.num} ${pKo} 박스 정면 오른발 논스톱 다이렉트 슈팅 골! (xG ${anim.m.xg})`);
          }
        }
        // Step 3: 골망 출렁임 (60 frames ~ 1.0s)
        else if (anim.step === 3) {
          anim.tacticalTag = '[⚽ GOAL! 결정적 득점 성공]';
          anim.tagColor = '#10b981';

          tacticsBall.x = anim.goalPt.x + Math.sin(anim.timer * 0.4) * 2.0;
          tacticsBall.y = anim.goalPt.y;

          if (anim.timer >= 60) {
            anim.step = 4;
            anim.timer = 0;
          }
        }
        // Step 4: 세리머니 질주 (90 frames ~ 1.5s)
        else if (anim.step === 4) {
          anim.tacticalTag = '[🎉 득점 세리머니]';
          anim.tagColor = '#10b981';

          anim.targetPlayer.x += 0.5 * tacticsSpeed;
          anim.targetPlayer.y += 0.35 * tacticsSpeed;

          if (anim.assister) {
            anim.assister.x += (anim.targetPlayer.x - 22 - anim.assister.x) * 0.035 * tacticsSpeed;
            anim.assister.y += (anim.targetPlayer.y - anim.assister.y) * 0.035 * tacticsSpeed;
          }
          if (anim.buildupPasser) {
            anim.buildupPasser.x += (anim.targetPlayer.x - 45 - anim.buildupPasser.x) * 0.025 * tacticsSpeed;
            anim.buildupPasser.y += (anim.targetPlayer.y - anim.buildupPasser.y) * 0.025 * tacticsSpeed;
          }

          if (anim.timer >= 90) {
            anim.step = 5;
            anim.timer = 0;
            anim.finished = true;
            updateCommentary('REVIEW', `[리플레이 완료] ⚽ #${anim.targetPlayer.num} ${pKo} 득점 시퀀스 분석 완료. [🔄 시퀀스 리플레이 다시보기] 버튼을 누르면 처음부터 다시 재생됩니다.`);
            if (isReelPlaying) {
              advanceFMReel();
            }
          }
        }
        // Step 5: 리플레이 완료 상태 유지
        else if (anim.step === 5) {
          anim.tacticalTag = '[📊 전술 분석 완료: 공간 침투 및 슈팅 궤적 보존]';
          anim.tagColor = '#10b981';
          anim.finished = true;
          anim.targetPlayer.x += Math.sin(anim.timer * 0.03) * 0.12;
        }
      }

      // ----------------------------------------------------
      // TYPE: TARGET_KEY_PASS (Buildup -> 35m Killer Diagonal Through-Pass -> Forward Strike -> GK Save)
      // ----------------------------------------------------
      else if (anim.type === 'TARGET_KEY_PASS') {
        const pKo = (currentPlayerTacticsData && currentPlayerTacticsData.player_info)
          ? (currentPlayerTacticsData.player_info.name_ko || currentPlayerTacticsData.player_info.name)
          : anim.targetPlayer.name;

        // Step 0: 후방 빌드업 전개 (80 frames ~ 1.33s)
        if (anim.step === 0) {
          anim.tacticalTag = '[🔄 탈압박 볼 키핑 & 전방 시야 확보]';
          anim.tagColor = '#38bdf8';

          tacticsSelectedPlayerId = anim.buildupPasser ? anim.buildupPasser.id : anim.targetPlayer.id;
          const passProg = Math.min(1.0, anim.timer / 80);
          tacticsBall.x = anim.buildupStartPt.x + (anim.actionPt.x - anim.buildupStartPt.x) * passProg;
          tacticsBall.y = anim.buildupStartPt.y + (anim.actionPt.y - anim.buildupStartPt.y) * passProg;

          anim.targetPlayer.x += (anim.actionPt.x - anim.targetPlayer.x) * 0.04 * tacticsSpeed;
          anim.targetPlayer.y += (anim.actionPt.y - anim.targetPlayer.y) * 0.04 * tacticsSpeed;

          if (anim.forwardRunner) {
            anim.forwardRunner.x += (anim.targetPt.x - 30 - anim.forwardRunner.x) * 0.02 * tacticsSpeed;
            anim.forwardRunner.y += (anim.targetPt.y - anim.forwardRunner.y) * 0.02 * tacticsSpeed;
          }

          if (anim.timer >= 80) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.buildupStartPt.x, y1: anim.buildupStartPt.y,
              x2: anim.actionPt.x, y2: anim.actionPt.y,
              color: '#38bdf8', dashed: true, alpha: 1.0,
              label: `[후방 빌드업] ➔ #${anim.targetPlayer.num} ${pKo}`
            });
            updateCommentary('PASS', `[1단계 빌드업] 후방에서 플레이메이커 #${anim.targetPlayer.num} ${pKo}에게 전진 패스 배달!`);
          }
        }
        // Step 1: 35m 대각선 킬러 스루패스 & 스트라이커 뒷공간 침투 (110 frames ~ 1.83s)
        else if (anim.step === 1) {
          tacticsSelectedPlayerId = anim.targetPlayer.id;
          anim.tacticalTag = '[🎯 35m 레이저 킬스루패스 (xA 찬스 창출)]';
          anim.tagColor = '#38bdf8';

          const passProg = Math.min(1.0, anim.timer / 110);
          tacticsBall.x = anim.actionPt.x + (anim.targetPt.x - anim.actionPt.x) * passProg;
          tacticsBall.y = anim.actionPt.y + (anim.targetPt.y - anim.actionPt.y) * passProg;

          if (anim.forwardRunner) {
            anim.forwardRunner.x += (anim.targetPt.x - anim.forwardRunner.x) * 0.045 * tacticsSpeed;
            anim.forwardRunner.y += (anim.targetPt.y - anim.forwardRunner.y) * 0.045 * tacticsSpeed;
            anim.forwardRunner.angle = Math.atan2(anim.goalPt.y - anim.forwardRunner.y, anim.goalPt.x - anim.forwardRunner.x);
          }

          if (anim.timer >= 110) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.actionPt.x, y1: anim.actionPt.y,
              x2: anim.targetPt.x, y2: anim.targetPt.y,
              color: '#38bdf8', dashed: true, alpha: 1.0,
              label: `[35m 킬러 스루패스] #${anim.targetPlayer.num} ${pKo} (xA ${anim.m.xa})`
            });
            updateCommentary('CHANCE', `[2단계 킬패스] #${anim.targetPlayer.num} ${pKo} 상대 수비 라인을 단번에 무너뜨리는 35m 레이저 킬스루패스 배달!`);
          }
        }
        // Step 2: 침투 공격수 유효 슈팅 & 상대 골키퍼 선방 (70 frames ~ 1.17s)
        else if (anim.step === 2) {
          anim.tacticalTag = '[💥 침투 공격수 유효 슈팅 & GK 선방]';
          anim.tagColor = '#f59e0b';

          if (anim.forwardRunner) tacticsSelectedPlayerId = anim.forwardRunner.id;
          const shotProg = Math.min(1.0, anim.timer / 70);
          tacticsBall.x = anim.targetPt.x + (anim.goalPt.x - anim.targetPt.x) * shotProg;
          tacticsBall.y = anim.targetPt.y + (anim.goalPt.y - anim.targetPt.y) * shotProg;

          if (anim.oppGk) {
            anim.oppGk.x += (anim.goalPt.x - 12 - anim.oppGk.x) * 0.045 * tacticsSpeed;
            anim.oppGk.y += (anim.goalPt.y - anim.oppGk.y) * 0.045 * tacticsSpeed;
          }

          if (anim.timer >= 70) {
            anim.step = 3;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.targetPt.x, y1: anim.targetPt.y,
              x2: anim.goalPt.x, y2: anim.goalPt.y,
              color: '#f59e0b', dashed: false, alpha: 1.0,
              label: '[유효 슈팅] 골키퍼 다이빙 선방!'
            });
            updateCommentary('SHOT', `[3단계 슈팅 & 선방] 침투 공격수의 강력한 유효 슈팅! 상대 골키퍼의 동물적 다이빙 세이브!`);
          }
        }
        // Step 3: 리플레이 완료 대기 (80 frames ~ 1.33s)
        else if (anim.step === 3) {
          anim.tacticalTag = '[📊 전술 분석 완료: 35m 패스 시야 및 침투 궤적 보존]';
          anim.tagColor = '#38bdf8';

          if (anim.timer >= 80) {
            anim.step = 4;
            anim.finished = true;
            updateCommentary('REVIEW', `[리플레이 완료] 🎯 #${anim.targetPlayer.num} ${pKo} 35m 킬패스 찬스 메이킹 시퀀스 완료. [🔄 시퀀스 리플레이 다시보기] 지원.`);
            if (isReelPlaying) {
              advanceFMReel();
            }
          }
        }
        else if (anim.step === 4) {
          anim.tacticalTag = '[📊 전술 분석 완료: 35m 패스 시야 및 침투 궤적 보존]';
          anim.tagColor = '#38bdf8';
          anim.finished = true;
        }
      }

      // ----------------------------------------------------
      // TYPE: TARGET_RECOVERY (High-Intensity Press -> Slide Interception -> 40m Sprint Carry -> Final-Third Layoff)
      // ----------------------------------------------------
      else if (anim.type === 'TARGET_RECOVERY') {
        const pKo = (currentPlayerTacticsData && currentPlayerTacticsData.player_info)
          ? (currentPlayerTacticsData.player_info.name_ko || currentPlayerTacticsData.player_info.name)
          : anim.targetPlayer.name;

        // Step 0: 상대 빌드업 전개 & 타겟 선수 전방 압박 쇄도 (80 frames ~ 1.33s)
        if (anim.step === 0) {
          tacticsSelectedPlayerId = anim.targetPlayer.id;
          anim.tacticalTag = '[🛡️ 상대 빌드업 경로 예측 고강도 압박]';
          anim.tagColor = '#818cf8';

          anim.targetPlayer.x += (anim.actionPt.x - anim.targetPlayer.x) * 0.045 * tacticsSpeed;
          anim.targetPlayer.y += (anim.actionPt.y - anim.targetPlayer.y) * 0.045 * tacticsSpeed;
          anim.targetPlayer.angle = Math.atan2(anim.actionPt.y - anim.targetPlayer.y, anim.actionPt.x - anim.targetPlayer.x);

          if (anim.oppCarrier) {
            anim.oppCarrier.x += (anim.actionPt.x - 8 - anim.oppCarrier.x) * 0.02 * tacticsSpeed;
          }

          if (anim.timer >= 80) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.actionPt.x - 45, y1: anim.actionPt.y - 20,
              x2: anim.actionPt.x, y2: anim.actionPt.y,
              color: '#818cf8', dashed: true, alpha: 1.0,
              label: `[전방 압박 볼 탈환] #${anim.targetPlayer.num} ${pKo}`
            });
            updateCommentary('TACKLE', `[1단계 볼 탈환] #${anim.targetPlayer.num} ${pKo} 상대 빌드업 경로 완벽 예측 후 고강도 태클 인터셉트 성공!`);
          }
        }
        // Step 1: 40m 폭풍 프로그레시브 캐리 질주 (130 frames ~ 2.17s)
        else if (anim.step === 1) {
          anim.tacticalTag = '[⚡ 40m 폭풍 전진 질주 파괴적 캐리]';
          anim.tagColor = '#fbbf24';

          const carryAngle = Math.atan2(anim.carryEnd.y - anim.targetPlayer.y, anim.carryEnd.x - anim.targetPlayer.x);
          anim.targetPlayer.angle = carryAngle;
          const strideSway = Math.sin(anim.timer * 0.28) * 3.0;
          const perpAngle = carryAngle + Math.PI / 2;

          anim.targetPlayer.x += (anim.carryEnd.x - anim.targetPlayer.x) * 0.035 * tacticsSpeed;
          anim.targetPlayer.y += (anim.carryEnd.y - anim.targetPlayer.y) * 0.035 * tacticsSpeed;

          // Realistic FM Dribble Mechanics: Cyclical foot touches push ball ahead, ball rolls & decelerates, player sprints
          const dribblePhase = (anim.timer % 18) / 18;
          const ballLeadDist = 8 + Math.sin(dribblePhase * Math.PI) * 9;
          tacticsBall.x = anim.targetPlayer.x + Math.cos(carryAngle) * ballLeadDist + Math.cos(perpAngle) * (strideSway * 0.6);
          tacticsBall.y = anim.targetPlayer.y + Math.sin(carryAngle) * ballLeadDist + Math.sin(perpAngle) * (strideSway * 0.6);

          if (anim.oppCarrier) {
            anim.oppCarrier.x += (anim.targetPlayer.x - 28 - anim.oppCarrier.x) * 0.028 * tacticsSpeed;
            anim.oppCarrier.y += (anim.targetPlayer.y + 6 - anim.oppCarrier.y) * 0.028 * tacticsSpeed;
            anim.oppCarrier.angle = Math.atan2(anim.targetPlayer.y - anim.oppCarrier.y, anim.targetPlayer.x - anim.oppCarrier.x);
          }

          if (anim.wingSupport) {
            anim.wingSupport.x += (anim.carryEnd.x + 45 - anim.wingSupport.x) * 0.03 * tacticsSpeed;
            anim.wingSupport.y += (anim.carryEnd.y + 25 - anim.wingSupport.y) * 0.03 * tacticsSpeed;
            anim.wingSupport.angle = Math.atan2(anim.carryEnd.y - anim.wingSupport.y, anim.carryEnd.x - anim.wingSupport.x);
          }

          if (anim.timer >= 130) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.actionPt.x, y1: anim.actionPt.y,
              x2: anim.carryEnd.x, y2: anim.carryEnd.y,
              color: '#fbbf24', dashed: false, alpha: 1.0,
              label: `[40m 전진 캐리] #${anim.targetPlayer.num} ${pKo}`
            });
            updateCommentary('CARRY', `[2단계 전진 캐리] #${anim.targetPlayer.num} ${pKo} 탈압박 후 가속도를 살려 40m를 단숨에 전진 질주!`);
          }
        }
        // Step 2: 파이널 서드 찬스 연계 패스 (80 frames ~ 1.33s)
        else if (anim.step === 2) {
          anim.tacticalTag = '[🎯 박스 침투 동료 컷백 찬스 연계]';
          anim.tagColor = '#38bdf8';

          if (anim.wingSupport) {
            const passProg = Math.min(1.0, anim.timer / 80);
            tacticsBall.x = anim.carryEnd.x + (anim.wingSupport.x - anim.carryEnd.x) * passProg;
            tacticsBall.y = anim.carryEnd.y + (anim.wingSupport.y - anim.carryEnd.y) * passProg;
          }

          if (anim.timer >= 80) {
            anim.step = 3;
            anim.timer = 0;
            if (anim.wingSupport) {
              tacticsTrajectories.push({
                x1: anim.carryEnd.x, y1: anim.carryEnd.y,
                x2: anim.wingSupport.x, y2: anim.wingSupport.y,
                color: '#38bdf8', dashed: true, alpha: 1.0,
                label: `[찬스 연계 컷백] ➔ #${anim.wingSupport.num} ${anim.wingSupport.name}`
              });
              updateCommentary('CHANCE', `[3단계 찬스 연계] 전방 침투 동료 #${anim.wingSupport.num} ${anim.wingSupport.name}에게 결정적 컷백 연결!`);
            }
          }
        }
        // Step 3: 리플레이 완료 대기 (80 frames ~ 1.33s)
        else if (anim.step === 3) {
          anim.tacticalTag = '[📊 전술 분석 완료: 프레싱 탈환 및 전진 캐리 궤적 보존]';
          anim.tagColor = '#818cf8';

          if (anim.timer >= 80) {
            anim.step = 4;
            anim.finished = true;
            updateCommentary('REVIEW', `[리플레이 완료] 🛡️ #${anim.targetPlayer.num} ${pKo} 볼탈환 & 40m 전진 캐리 시퀀스 완료. [🔄 시퀀스 리플레이 다시보기] 지원.`);
            if (isReelPlaying) {
              advanceFMReel();
            }
          }
        }
        else if (anim.step === 4) {
          anim.tacticalTag = '[📊 전술 분석 완료: 프레싱 탈환 및 전진 캐리 궤적 보존]';
          anim.tagColor = '#818cf8';
          anim.finished = true;
        }
      }

      // ----------------------------------------------------
      // TYPE: WC_HWANG (World Cup Hwang Hee-Chan Winner - 70m Sprint & Nutmeg Pass & Finish)
      // ----------------------------------------------------
      else if (anim.type === 'WC_HWANG') {
        // Step 0: 손흥민 70m 폭풍 질주 (160 frames ~ 2.67s)
        if (anim.step === 0) {
          tacticsSelectedPlayerId = anim.son ? anim.son.id : 'H11';
          anim.targetPlayer = anim.son;
          anim.tacticalTag = '[⚡ 손흥민 70m 단독 드리블 폭풍 질주]';
          anim.tagColor = '#fbbf24';

          const wpIdx = Math.min(anim.waypoints.length - 1, Math.floor((anim.timer / 160) * anim.waypoints.length));
          const targetPt = anim.waypoints[wpIdx];
          if (anim.son) {
            const runAngle = Math.atan2(targetPt.y - anim.son.y, targetPt.x - anim.son.x);
            anim.son.angle = runAngle;
            anim.son.x += (targetPt.x - anim.son.x) * 0.045 * tacticsSpeed;
            anim.son.y += (targetPt.y - anim.son.y) * 0.045 * tacticsSpeed;

            // FM Realistic Dribble Foot-Touch Mechanics for Son 70m sprint
            const dribblePhase = (anim.timer % 16) / 16;
            const touchPush = Math.sin(dribblePhase * Math.PI) * 8.5;
            const strideSway = Math.sin(anim.timer * 0.32) * 2.8;
            const perpAngle = runAngle + Math.PI / 2;
            tacticsBall.x = anim.son.x + Math.cos(runAngle) * (8 + touchPush) + Math.cos(perpAngle) * strideSway;
            tacticsBall.y = anim.son.y + Math.sin(runAngle) * (8 + touchPush) + Math.sin(perpAngle) * strideSway;
          }

          if (anim.hwang) {
            anim.hwang.x += (anim.shotPt.x - 30 - anim.hwang.x) * 0.03 * tacticsSpeed;
            anim.hwang.y += (anim.shotPt.y - anim.hwang.y) * 0.03 * tacticsSpeed;
          }

          if (anim.timer >= 160) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.passStart.x, y1: anim.passStart.y,
              x2: anim.shotPt.x, y2: anim.shotPt.y,
              color: '#fbbf24', dashed: true, alpha: 1.0, label: '손흥민 가랑이 사이 킬스루패스'
            });
            updateCommentary('ASSIST', '[2단계 어시스트] 손흥민, 포르투갈 수비수 3명 사이로 환상적인 가랑이 킬스루패스 배달!');
          }
        }
        // Step 1: 황희찬 박스 침투 논스톱 오른발 슈팅 (70 frames ~ 1.17s)
        else if (anim.step === 1) {
          tacticsSelectedPlayerId = anim.hwang ? anim.hwang.id : 'H10';
          anim.targetPlayer = anim.hwang;
          anim.tacticalTag = '[🎯 가랑이 킬스루패스 & 황희찬 슈팅]';
          anim.tagColor = '#10b981';

          tacticsBall.x += (anim.shotPt.x - tacticsBall.x) * 0.06 * tacticsSpeed;
          tacticsBall.y += (anim.shotPt.y - tacticsBall.y) * 0.06 * tacticsSpeed;

          if (anim.hwang) {
            anim.hwang.x += (anim.shotPt.x - anim.hwang.x) * 0.06 * tacticsSpeed;
            anim.hwang.y += (anim.shotPt.y - anim.hwang.y) * 0.06 * tacticsSpeed;
          }

          if (anim.timer >= 70) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.shotPt.x, y1: anim.shotPt.y,
              x2: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 5, y2: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.52,
              color: '#10b981', dashed: false, alpha: 1.0, label: '황희찬 논스톱 슈팅 골! (xG 0.42)'
            });
            document.getElementById('tactics-score-home').textContent = '2';
            document.getElementById('tactics-score-away').textContent = '1';
            triggerGoalBanner(anim.goalText);
            updateCommentary('SHOT', '[3단계 슈팅] 쇄도하던 황희찬의 침착한 오른발 논스톱 다이렉트 슈팅 골망 흔들림!');
          }
        }
        // Step 2: 골 세리머니 (90 frames ~ 1.5s)
        else if (anim.step === 2) {
          anim.tacticalTag = '[🎉 90:28 극장 역전 결승골 세리머니]';
          anim.tagColor = '#10b981';

          if (anim.hwang) {
            anim.hwang.x += 0.5 * tacticsSpeed;
            anim.hwang.y += 0.3 * tacticsSpeed;
          }
          if (anim.son) {
            anim.son.x += (anim.hwang.x - anim.son.x) * 0.035 * tacticsSpeed;
            anim.son.y += (anim.hwang.y - anim.son.y) * 0.035 * tacticsSpeed;
          }

          if (anim.timer >= 90) {
            anim.step = 3;
            anim.timer = 0;
            anim.finished = true;
            updateCommentary('REVIEW', '[리플레이 완료] ⚽ 대한민국 2:1 포르투갈 90:28 역전 결승골 시퀀스 분석 완료. [🔄 시퀀스 리플레이 다시보기] 지원.');
          }
        }
        // Step 3: 리플레이 완료 유지
        else if (anim.step === 3) {
          anim.tacticalTag = '[📊 전술 분석 완료: 70m 스프린트 & 킬패스 궤적 보존]';
          anim.tagColor = '#10b981';
          anim.finished = true;
        }
      }

      // ----------------------------------------------------
      // TYPE: WC_HORTA (Horta 04:53 Goal)
      // ----------------------------------------------------
      else if (anim.type === 'WC_HORTA') {
        if (anim.step === 0) {
          anim.targetPlayer = anim.horta;
          anim.tacticalTag = '[🚀 달로트 우측면 돌파 & 컷백 크로스]';
          anim.tagColor = '#f59e0b';

          if (anim.dalot) {
            anim.dalot.x += (anim.crossPt.x - anim.dalot.x) * 0.04 * tacticsSpeed;
            anim.dalot.y += (anim.crossPt.y - anim.dalot.y) * 0.04 * tacticsSpeed;
            tacticsBall.x = anim.dalot.x - 6;
            tacticsBall.y = anim.dalot.y;
          }
          if (anim.horta) {
            anim.horta.x += (anim.finishPt.x - anim.horta.x) * 0.035 * tacticsSpeed;
            anim.horta.y += (anim.finishPt.y - anim.horta.y) * 0.035 * tacticsSpeed;
          }
          if (anim.timer >= 80) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.crossPt.x, y1: anim.crossPt.y,
              x2: anim.finishPt.x, y2: anim.finishPt.y,
              color: '#f59e0b', dashed: true, alpha: 1.0, label: '달로트 우측면 컷백 크로스'
            });
            updateCommentary('ASSIST', '[1단계 어시스트] 달로트의 우측면 폭풍 돌파 후 완벽한 박스 중앙 컷백 크로스!');
          }
        } else if (anim.step === 1) {
          anim.tacticalTag = '[⚡ 호르타 니어포스트 다이렉트 선제골]';
          anim.tagColor = '#ef4444';

          tacticsBall.x += (anim.finishPt.x - tacticsBall.x) * 0.06 * tacticsSpeed;
          tacticsBall.y += (anim.finishPt.y - tacticsBall.y) * 0.06 * tacticsSpeed;

          if (anim.timer >= 60) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.finishPt.x, y1: anim.finishPt.y,
              x2: TACTICS_PITCH_MARGIN + 8, y2: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.5,
              color: '#ef4444', dashed: false, alpha: 1.0, label: '호르타 선제골 (xG 0.29)'
            });
            document.getElementById('tactics-score-home').textContent = '0';
            document.getElementById('tactics-score-away').textContent = '1';
            triggerGoalBanner('포르투갈 리카르도 호르타 선제골 (xG 0.29)');
            updateCommentary('SHOT', '[2단계 슈팅] 리카르도 호르타 니어포스트 쇄도 원터치 다이렉트 선제골!');
          }
        } else if (anim.step === 2) {
          anim.tacticalTag = '[📊 전술 분석 완료: 측면 돌파 & 크로스 궤적 보존]';
          anim.tagColor = '#ef4444';

          if (anim.timer >= 80) {
            anim.step = 3;
            anim.timer = 0;
            anim.finished = true;
            updateCommentary('REVIEW', '[리플레이 완료] ⚽ 포르투갈 04:53 선제골 시퀀스 분석 완료. [🔄 시퀀스 리플레이 다시보기] 지원.');
          }
        } else if (anim.step === 3) {
          anim.tacticalTag = '[📊 전술 분석 완료: 측면 돌파 & 크로스 궤적 보존]';
          anim.tagColor = '#ef4444';
          anim.finished = true;
        }
      }

      // ----------------------------------------------------
      // TYPE: WC_KIM (Kim Young-Gwon 26:43 Equalizer)
      // ----------------------------------------------------
      else if (anim.type === 'WC_KIM') {
        if (anim.step === 0) {
          anim.targetPlayer = anim.kim;
          anim.tacticalTag = '[🎯 이강인 정밀 택배 인스윙 코너킥]';
          anim.tagColor = '#38bdf8';

          const cornerProg = Math.min(1.0, anim.timer / 90);
          tacticsBall.x = anim.cornerPt.x + (anim.deflectPt.x - anim.cornerPt.x) * cornerProg;
          tacticsBall.y = anim.cornerPt.y + (anim.deflectPt.y - anim.cornerPt.y) * cornerProg;

          if (anim.kim) {
            anim.kim.x += (anim.finishPt.x - anim.kim.x) * 0.03 * tacticsSpeed;
            anim.kim.y += (anim.finishPt.y - anim.kim.y) * 0.03 * tacticsSpeed;
          }

          if (anim.timer >= 90) {
            anim.step = 1;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.cornerPt.x, y1: anim.cornerPt.y,
              x2: anim.deflectPt.x, y2: anim.deflectPt.y,
              color: '#38bdf8', dashed: true, alpha: 1.0, label: '이강인 택배 코너킥'
            });
            updateCommentary('CORNER', '[1단계 코너킥] 이강인의 날카로운 왼발 인스윙 코너킥이 문전으로 배달!');
          }
        } else if (anim.step === 1) {
          anim.tacticalTag = '[⚡ 호날두 등 굴절 & 김영권 발리 동점골]';
          anim.tagColor = '#10b981';

          tacticsBall.x += (anim.finishPt.x - tacticsBall.x) * 0.07 * tacticsSpeed;
          tacticsBall.y += (anim.finishPt.y - tacticsBall.y) * 0.07 * tacticsSpeed;

          if (anim.timer >= 60) {
            anim.step = 2;
            anim.timer = 0;
            tacticsTrajectories.push({
              x1: anim.deflectPt.x, y1: anim.deflectPt.y,
              x2: anim.finishPt.x, y2: anim.finishPt.y,
              color: '#fbbf24', dashed: true, alpha: 1.0, label: '호날두 등 굴절'
            });
            tacticsTrajectories.push({
              x1: anim.finishPt.x, y1: anim.finishPt.y,
              x2: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 8, y2: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.48,
              color: '#10b981', dashed: false, alpha: 1.0, label: '김영권 왼발 발리 동점골! (xG 0.62)'
            });
            document.getElementById('tactics-score-home').textContent = '1';
            document.getElementById('tactics-score-away').textContent = '1';
            triggerGoalBanner('대한민국 김영권 동점골! (1:1)');
            updateCommentary('SHOT', '[2단계 발리 득점] 호날두 등에 맞고 흐른 볼을 김영권이 침착한 왼발 발리슛으로 동점골 폭발!');
          }
        } else if (anim.step === 2) {
          anim.tacticalTag = '[📊 전술 분석 완료: 세트피스 코너킥 및 발리 궤적 보존]';
          anim.tagColor = '#10b981';

          if (anim.timer >= 80) {
            anim.step = 3;
            anim.timer = 0;
            anim.finished = true;
            updateCommentary('REVIEW', '[리플레이 완료] ⚽ 대한민국 26:43 김영권 동점골 시퀀스 분석 완료. [🔄 시퀀스 리플레이 다시보기] 지원.');
          }
        } else if (anim.step === 3) {
          anim.tacticalTag = '[📊 전술 분석 완료: 세트피스 코너킥 및 발리 궤적 보존]';
          anim.tagColor = '#10b981';
          anim.finished = true;
        }
      }

      // ----------------------------------------------------
      // TYPE: WC_MOMENT (Player Signature Individual Moment)
      // ----------------------------------------------------
      else if (anim.type === 'WC_MOMENT') {
        if (anim.step === 0) {
          tacticsSelectedPlayerId = anim.targetPlayer ? anim.targetPlayer.id : 'H11';
          anim.tacticalTag = `[★ ${anim.pm.player_name}: ${anim.m.title}]`;
          anim.tagColor = '#38bdf8';

          if (anim.targetPlayer) {
            anim.targetPlayer.x += (anim.actionPt.x - anim.targetPlayer.x) * 0.045 * tacticsSpeed;
            anim.targetPlayer.y += (anim.actionPt.y - anim.targetPlayer.y) * 0.045 * tacticsSpeed;
            tacticsBall.x = anim.targetPlayer.x + 8;
            tacticsBall.y = anim.targetPlayer.y;
          }
          if (anim.timer >= 70) {
            anim.step = 1;
            anim.timer = 0;
            if (anim.m.type === 'SHOT') {
              tacticsTrajectories.push({
                x1: anim.actionPt.x, y1: anim.actionPt.y,
                x2: anim.goalPt.x, y2: anim.goalPt.y,
                color: '#f59e0b', dashed: false, alpha: 1.0, label: `${anim.m.title} (xG ${anim.m.xg})`
              });
            } else if (anim.m.type === 'KEY_PASS' || anim.m.type === 'ASSIST') {
              tacticsTrajectories.push({
                x1: anim.actionPt.x, y1: anim.actionPt.y,
                x2: anim.actionPt.x + 80, y2: anim.actionPt.y + 40,
                color: '#38bdf8', dashed: true, alpha: 1.0, label: anim.m.title
              });
            } else if (anim.m.type === 'DEFENSE') {
              tacticsTrajectories.push({
                x1: anim.actionPt.x - 40, y1: anim.actionPt.y - 20,
                x2: anim.actionPt.x, y2: anim.actionPt.y,
                color: '#818cf8', dashed: true, alpha: 1.0, label: anim.m.title
              });
            }
          }
        } else if (anim.step === 1) {
          anim.tacticalTag = `[🎯 ${anim.m.title} 분석 시퀀스]`;
          anim.tagColor = '#10b981';

          if (anim.m.type === 'SHOT') {
            tacticsBall.x += (anim.goalPt.x - tacticsBall.x) * 0.06 * tacticsSpeed;
            tacticsBall.y += (anim.goalPt.y - tacticsBall.y) * 0.06 * tacticsSpeed;
          }
          if (anim.timer >= 70) {
            anim.step = 2;
            anim.timer = 0;
            anim.finished = true;
            updateCommentary('REVIEW', `[리플레이 완료] 🎯 ${anim.pm.player_name}: ${anim.m.title} 분석 완료. [🔄 시퀀스 리플레이 다시보기] 지원.`);
          }
        } else if (anim.step === 2) {
          anim.finished = true;
        }
      }
    }

    // Play Player Moment
    function playPlayerMoment(playerName, momentIdx) {
      if (!tacticsData || !tacticsData.player_moments) return;
      const pm = tacticsData.player_moments.find(p => p.player_name === playerName || p.player_en.includes(playerName));
      if (!pm || !pm.moments[momentIdx]) return;

      const m = pm.moments[momentIdx];
      isTacticsRunning = true;
      const icon = document.getElementById('btn-tactics-play-icon');
      const text = document.getElementById('btn-tactics-play-text');
      if (icon && text) {
        icon.textContent = '⏸️';
        text.textContent = '일시정지';
      }

      currentReplayContext = { mode: 'match', highlightId: null, playerName: playerName, momentIdx: momentIdx };
      tacticsTrajectories = [];
      activeHighlightAnim = null;

      document.getElementById('tactics-clock').textContent = m.time;
      updateCommentary('MOMENT', `[${m.time}] ${pm.player_name} (${pm.role}): ${m.title} - ${m.desc}`);

      const targetPlayer = tacticsPlayers.find(p => p.name === pm.player_name && p.team === 'home') || tacticsPlayers.find(p => p.team === 'home' && p.id === 'H11');
      const actionPt = statsBombToPixel(m.location[0], m.location[1]);

      if (targetPlayer) {
        targetPlayer.x = actionPt.x - 20;
        targetPlayer.y = actionPt.y;
        tacticsSelectedPlayerId = targetPlayer.id;
      }

      tacticsBall.x = actionPt.x - 12;
      tacticsBall.y = actionPt.y;

      const goalPt = { x: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 10, y: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.45 };
      const oppGk = tacticsPlayers.find(p => p.team === 'away' && p.pos === 'GK');

      activeHighlightAnim = {
        type: 'WC_MOMENT',
        step: 0,
        timer: 0,
        m: m,
        pm: pm,
        targetPlayer: targetPlayer,
        oppGk: oppGk,
        actionPt: actionPt,
        goalPt: goalPt
      };
    }

    // Dynamic Player Tactical Highlights Loader
    async function loadPlayerTacticsHighlights(playerName) {
      if (!playerName) return;
      try {
        updateCommentary('TACTIC', `스카우팅 타겟 [${playerName}] 공식 전술 데이터 & 2D 매치 리플레이 분석 중...`);
        const res = await fetch(`/api/tactics/player-highlights?player_name=${encodeURIComponent(playerName)}`);
        if (!res.ok) {
          console.warn('Player highlights not found, fallback to showcase');
          return;
        }
        const data = await res.json();
        currentPlayerTacticsData = data;
        tacticsMode = 'player';

        // Update Mode Button styling & dynamic titles
        const btnMatch = document.getElementById('tactics-mode-match');
        const btnPlayer = document.getElementById('tactics-mode-player');
        const btnSim = document.getElementById('tactics-mode-sim');
        const btnMatchTitle = document.getElementById('tactics-mode-match-title');
        const btnMatchSub = document.getElementById('tactics-mode-match-sub');
        const btnPlayerTitle = document.getElementById('tactics-mode-player-title');
        const btnPlayerSub = document.getElementById('tactics-mode-player-sub');

        if (btnMatch) btnMatch.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-1.5';
        if (btnSim) btnSim.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-1.5';
        if (btnPlayer) {
          btnPlayer.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm';
        }

        if (btnMatchTitle) btnMatchTitle.textContent = `🏆 ${data.match_info.home_team} 공식 경기`;
        if (btnMatchSub) btnMatchSub.textContent = `(${data.match_info.home_team} vs ${data.match_info.away_team})`;

        if (btnPlayerTitle) btnPlayerTitle.textContent = `🎯 ${data.player_info.name_ko} 시그니처 3모먼트`;
        if (btnPlayerSub) btnPlayerSub.textContent = `(${data.player_info.position} 득점·키패스·볼탈환)`;

        // 1. Update Scoreboard
        const homeEl = document.getElementById('tactics-team-home');
        const awayEl = document.getElementById('tactics-team-away');
        const formHomeEl = document.getElementById('tactics-form-home');
        const formAwayEl = document.getElementById('tactics-form-away');
        if (homeEl) homeEl.textContent = data.match_info.home_team;
        if (awayEl) awayEl.textContent = data.match_info.away_team;
        if (formHomeEl) formHomeEl.textContent = `(${data.match_info.home_formation})`;
        if (formAwayEl) formAwayEl.textContent = `(${data.match_info.away_formation})`;
        document.getElementById('tactics-score-home').textContent = '2';
        document.getElementById('tactics-score-away').textContent = '1';
        document.getElementById('tactics-status-badge').textContent = `${data.player_info.name_ko} (${data.match_info.home_team}) 전술 분석`;

        // Update Pitch Legend with actual club names & stars
        const legHome = document.getElementById('legend-home-team');
        const legAway = document.getElementById('legend-away-team');
        if (legHome) {
          legHome.innerHTML = `🔵 <b class="text-zinc-200">${data.match_info.home_team}</b>: ${data.match_info.home_top_names || ''} 등`;
        }
        if (legAway) {
          legAway.innerHTML = `🔴 <b class="text-zinc-200">${data.match_info.away_team}</b>: ${data.match_info.away_top_names || ''} 등`;
        }

        // Update Direct External Video Watch Link
        const ytId = data.match_info.youtube_highlight_id || 'h2EwOys6evI';
        const ytExtBtn = document.getElementById('tactics-yt-external-btn');
        if (ytExtBtn) {
          ytExtBtn.href = data.match_info.youtube_watch_url || `https://www.youtube.com/watch?v=${ytId}`;
        }

        // 2. Load Home & Away Rosters onto 2D Pitch
        tacticsPlayers = [];
        data.home_roster.forEach(p => {
          const pt = tacticsGridToPixel(p.col, p.row);
          tacticsPlayers.push({
            ...p,
            team: 'home',
            baseCol: p.col,
            baseRow: p.row,
            x: pt.x,
            y: pt.y,
            tx: pt.x,
            ty: pt.y,
            angle: 0,
            stamina: 96
          });
        });

        data.away_roster.forEach(p => {
          const pt = tacticsGridToPixel(p.col, p.row);
          tacticsPlayers.push({
            ...p,
            team: 'away',
            baseCol: p.col,
            baseRow: p.row,
            x: pt.x,
            y: pt.y,
            tx: pt.x,
            ty: pt.y,
            angle: Math.PI,
            stamina: 94
          });
        });

        // Focus spotlight on target player
        tacticsSelectedPlayerId = data.player_info.target_slot_id;

        // 3. Update Video Iframe with Verified Embed-Allowed Clip
        const ytFrame = document.getElementById('tactics-yt-frame');
        if (ytFrame) {
          ytFrame.src = `https://www.youtube.com/embed/${ytId}?enablejsapi=1&rel=0&modestbranding=1`;
          ytFrame.title = `${data.player_info.name} Official Highlights`;
        }

        // 4. Update Opta Stats Card with Player's Real Metrics
        renderPlayerOptaStats(data);

        // 5. Update Quick Chapter Buttons
        renderPlayerChapterButtons(data);

        // 6. Update Timeline Event Log
        renderPlayerEventLog(data);

        // 7. Auto-play Moment 1 (Signature Action)
        playTargetPlayerHighlight(0);

        if (!tacticsAnimId) {
          tacticsLoop();
        }
      } catch (err) {
        console.error('Error loading player tactics highlights:', err);
      }
    }

    // Play Target Player's Custom Moment (0: Signature Goal/Finishing, 1: Key Pass/Assist, 2: Recovery/Carry)
    function playTargetPlayerHighlight(momentIdx) {
      if (!currentPlayerTacticsData || !currentPlayerTacticsData.key_match_highlights) return;
      const m = currentPlayerTacticsData.key_match_highlights[momentIdx];
      if (!m) return;

      isTacticsRunning = true;
      const icon = document.getElementById('btn-tactics-play-icon');
      const text = document.getElementById('btn-tactics-play-text');
      if (icon && text) {
        icon.textContent = '⏸️';
        text.textContent = '일시정지';
      }

      currentReplayContext = { mode: 'player', momentIdx: momentIdx, highlightId: null };
      tacticsTrajectories = [];
      activeHighlightAnim = null;

      // Update UI Clock, Commentary & Scores
      document.getElementById('tactics-clock').textContent = m.display_time;
      updateCommentary(m.type, `[${m.display_time}] ${m.title}: ${m.description}`);

      const targetPlayer = tacticsPlayers.find(p => p.is_target || p.id === m.target_player_id) || tacticsPlayers.find(p => p.team === 'home' && p.pos !== 'GK') || tacticsPlayers[10];
      if (!targetPlayer) return;

      tacticsSelectedPlayerId = targetPlayer.id;

      const actionPt = statsBombToPixel(m.start_location[0], m.start_location[1]);
      const goalCenterPt = { x: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 8, y: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.5 };
      const oppGk = tacticsPlayers.find(p => p.team === 'away' && p.pos === 'GK') || tacticsPlayers[11];

      const homeTeammates = tacticsPlayers.filter(p => p.team === 'home' && p.id !== targetPlayer.id && p.pos !== 'GK');
      const oppDefender = tacticsPlayers.find(p => p.team === 'away' && (p.pos === 'CB' || p.pos === 'DM')) || tacticsPlayers[13];

      if (m.type === 'GOAL') {
        document.getElementById('tactics-score-home').textContent = '2';
        document.getElementById('tactics-score-away').textContent = '1';

        const buildupPasser = homeTeammates.find(p => p.pos === 'DM' || p.pos === 'CM' || p.pos === 'CB') || homeTeammates[0] || tacticsPlayers[0];
        const assister = homeTeammates.find(p => p.id !== buildupPasser.id && (p.pos === 'LW' || p.pos === 'RW' || p.pos === 'AM' || p.pos === 'CF')) || homeTeammates[1] || homeTeammates[0];

        const buildupStartPt = { x: Math.max(TACTICS_PITCH_MARGIN + 110, actionPt.x - 170), y: actionPt.y + (actionPt.y > TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.5 ? -35 : 35) };
        const assisterStartPt = { x: actionPt.x - 85, y: actionPt.y - 65 };
        const assisterCrossPt = { x: actionPt.x - 35, y: actionPt.y - 45 };
        const targetStartPt = { x: actionPt.x - 80, y: actionPt.y + 25 };

        if (buildupPasser) {
          buildupPasser.x = buildupStartPt.x;
          buildupPasser.y = buildupStartPt.y;
          buildupPasser.angle = Math.atan2(assisterStartPt.y - buildupStartPt.y, assisterStartPt.x - buildupStartPt.x);
        }

        if (assister) {
          assister.x = assisterStartPt.x - 20;
          assister.y = assisterStartPt.y - 10;
          assister.angle = Math.atan2(buildupStartPt.y - assister.y, buildupStartPt.x - assister.x);
        }

        targetPlayer.x = targetStartPt.x;
        targetPlayer.y = targetStartPt.y;
        targetPlayer.angle = Math.atan2(actionPt.y - targetStartPt.y, actionPt.x - targetStartPt.x);

        if (oppDefender) {
          oppDefender.x = actionPt.x + 25;
          oppDefender.y = actionPt.y - 12;
        }
        if (oppGk) {
          oppGk.x = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 20;
          oppGk.y = goalCenterPt.y;
        }

        tacticsBall.x = buildupStartPt.x;
        tacticsBall.y = buildupStartPt.y;
        tacticsBall.inFlight = true;

        activeHighlightAnim = {
          type: 'TARGET_GOAL',
          step: 0,
          timer: 0,
          m: m,
          targetPlayer: targetPlayer,
          buildupPasser: buildupPasser,
          assister: assister,
          oppDefender: oppDefender,
          oppGk: oppGk,
          tacticalTag: '[📐 시야 & 1차 빌드업 전개]',
          tagColor: '#38bdf8',
          actionPt: actionPt,
          buildupStartPt: buildupStartPt,
          assisterStartPt: assisterStartPt,
          assisterCrossPt: assisterCrossPt,
          targetStartPt: targetStartPt,
          goalPt: { x: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 6, y: actionPt.y * 0.25 + goalCenterPt.y * 0.75 }
        };
      } else if (m.type === 'KEY_PASS') {
        const targetPt = statsBombToPixel(m.target_location[0], m.target_location[1]);
        const buildupPasser = homeTeammates.find(p => p.pos === 'DM' || p.pos === 'CB' || p.pos === 'LB' || p.pos === 'RB') || homeTeammates[0];
        const forwardRunner = homeTeammates.find(p => p.id !== buildupPasser.id && (p.pos === 'CF' || p.pos === 'LW' || p.pos === 'RW')) || homeTeammates[1] || homeTeammates[0];

        const buildupStartPt = { x: Math.max(TACTICS_PITCH_MARGIN + 100, actionPt.x - 140), y: actionPt.y + 30 };
        const playmakerStartPt = { x: actionPt.x - 25, y: actionPt.y };

        if (buildupPasser) {
          buildupPasser.x = buildupStartPt.x;
          buildupPasser.y = buildupStartPt.y;
          buildupPasser.angle = Math.atan2(actionPt.y - buildupStartPt.y, actionPt.x - buildupStartPt.x);
        }

        targetPlayer.x = playmakerStartPt.x;
        targetPlayer.y = playmakerStartPt.y;
        targetPlayer.angle = Math.atan2(targetPt.y - playmakerStartPt.y, targetPt.x - playmakerStartPt.x);

        if (forwardRunner) {
          forwardRunner.x = actionPt.x + 20;
          forwardRunner.y = actionPt.y + 15;
          forwardRunner.angle = Math.atan2(targetPt.y - forwardRunner.y, targetPt.x - forwardRunner.x);
        }

        if (oppGk) {
          oppGk.x = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 20;
          oppGk.y = goalCenterPt.y;
        }

        tacticsBall.x = buildupStartPt.x;
        tacticsBall.y = buildupStartPt.y;
        tacticsBall.inFlight = true;

        activeHighlightAnim = {
          type: 'TARGET_KEY_PASS',
          step: 0,
          timer: 0,
          m: m,
          targetPlayer: targetPlayer,
          buildupPasser: buildupPasser,
          forwardRunner: forwardRunner,
          oppGk: oppGk,
          tacticalTag: '[🔄 탈압박 볼 키핑 & 전방 시야 확보]',
          tagColor: '#38bdf8',
          buildupStartPt: buildupStartPt,
          actionPt: actionPt,
          targetPt: targetPt,
          goalPt: { x: TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 8, y: TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.46 }
        };
      } else if (m.type === 'RECOVERY') {
        const carryEnd = statsBombToPixel(m.carry_end[0], m.carry_end[1]);
        const oppCarrier = tacticsPlayers.find(p => p.team === 'away' && p.pos !== 'GK') || tacticsPlayers[15];
        const wingSupport = homeTeammates.find(p => p.id !== targetPlayer.id && (p.pos === 'CF' || p.pos === 'LW' || p.pos === 'RW' || p.pos === 'AM' || p.pos === 'CM')) || homeTeammates[0];

        if (oppCarrier) {
          oppCarrier.x = actionPt.x - 22;
          oppCarrier.y = actionPt.y - 12;
          oppCarrier.angle = 0;
        }

        if (wingSupport) {
          wingSupport.x = carryEnd.x + 35;
          wingSupport.y = carryEnd.y + 20;
          wingSupport.angle = Math.atan2(carryEnd.y - wingSupport.y, carryEnd.x - wingSupport.x);
        }

        targetPlayer.x = actionPt.x - 55;
        targetPlayer.y = actionPt.y + 22;
        targetPlayer.angle = Math.atan2(actionPt.y - targetPlayer.y, actionPt.x - targetPlayer.x);

        tacticsBall.x = actionPt.x - 22;
        tacticsBall.y = actionPt.y - 12;
        tacticsBall.inFlight = false;

        activeHighlightAnim = {
          type: 'TARGET_RECOVERY',
          step: 0,
          timer: 0,
          m: m,
          targetPlayer: targetPlayer,
          oppCarrier: oppCarrier,
          wingSupport: wingSupport,
          tacticalTag: '[🛡️ 상대 빌드업 경로 예측 고강도 압박]',
          tagColor: '#818cf8',
          actionPt: actionPt,
          carryEnd: carryEnd
        };
      }
    }

    function renderPlayerChapterButtons(data) {
      const container = document.getElementById('tactics-chapter-buttons');
      if (!container || !data || !data.key_match_highlights) return;

      const pName = data.player_info.name_ko || data.player_info.name;
      const hintEl = document.getElementById('tactics-chapter-hint');
      if (hintEl) {
        hintEl.textContent = `타겟: [${pName} (${data.player_info.position})] ${data.player_info.club} vs ${data.match_info.away_team} 전술 리플레이`;
      }

      let html = '';
      const reelActive = isReelPlaying
        ? 'bg-amber-500 text-black border-amber-400 font-extrabold shadow-lg animate-pulse'
        : 'bg-gradient-to-r from-amber-500/20 to-orange-500/20 text-amber-300 border-amber-500/40 hover:bg-amber-500/30';
      html += `
        <button onclick="playPlayerFullMatchReel()"
          class="px-3 py-1.5 rounded-lg border ${reelActive} text-xs font-bold transition flex items-center gap-1.5 shadow-md">
          <span>${isReelPlaying ? '⏸️' : '▶️'} 90분 종합 활약상 연속 재생 (Full FM Reel)</span>
        </button>
      `;

      data.key_match_highlights.forEach((m, idx) => {
        const isGoal = m.type === 'GOAL';
        const colorClass = isGoal ? 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10' : (m.type === 'KEY_PASS' ? 'text-sky-400 border-sky-500/40 bg-sky-500/10' : 'text-indigo-400 border-indigo-500/40 bg-indigo-500/10');
        const icon = isGoal ? '⚽' : (m.type === 'KEY_PASS' ? '🎯' : '🛡️');
        html += `
          <button onclick="playTargetPlayerHighlight(${idx})"
            class="px-2.5 py-1.5 rounded-lg border ${colorClass} hover:opacity-90 text-xs font-semibold transition flex items-center gap-1.5 shadow-sm">
            <span class="font-mono font-bold">${m.display_time}</span>
            <span>${icon} ${m.title}</span>
          </button>
        `;
      });

      html += `
        <button onclick="resetToWorldCupShowcase()"
          class="px-2 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-400 hover:text-white transition flex items-center gap-1.5">
          <span>🇰🇷 2022 카타르 월드컵 쇼케이스(대한민국 vs 포르투갈)로 변경</span>
        </button>
      `;

      container.innerHTML = html;
    }

    function renderPlayerEventLog(data) {
      const logEl = document.getElementById('tactics-event-log');
      if (!logEl || !data || !data.key_match_highlights) return;

      let html = '';
      data.key_match_highlights.forEach((m, idx) => {
        const isGoal = m.type === 'GOAL';
        const badgeColor = isGoal ? 'text-emerald-400' : (m.type === 'KEY_PASS' ? 'text-sky-400' : 'text-indigo-400');
        const metric = m.xg ? `xG ${m.xg}` : (m.xa ? `xA ${m.xa}` : m.type);
        html += `
          <div onclick="playTargetPlayerHighlight(${idx})"
            class="p-2 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.04] cursor-pointer transition flex items-center justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="font-mono text-[11px] font-bold ${badgeColor}">${m.display_time}</span>
              <span class="font-semibold text-white">${m.title}</span>
            </div>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">${metric}</span>
          </div>
        `;
      });

      logEl.innerHTML = html;
    }

    function renderPlayerOptaStats(data) {
      const p = data.player_info;
      const s = data.opta_stats || {};

      const possHome = document.getElementById('stat-poss-home');
      const possAway = document.getElementById('stat-poss-away');
      const barPossHome = document.getElementById('bar-poss-home');
      const barPossAway = document.getElementById('bar-poss-away');
      if (possHome && possAway && barPossHome && barPossAway) {
        possHome.textContent = '58%';
        possAway.textContent = '42%';
        barPossHome.style.width = '58%';
        barPossAway.style.width = '42%';
      }

      const shotsHome = document.getElementById('stat-shots-home');
      const shotsAway = document.getElementById('stat-shots-away');
      if (shotsHome && shotsAway) {
        const g90 = s.goals_per90 ? `${s.goals_per90}G/90` : '15 (7)';
        shotsHome.textContent = `${g90} (${p.position})`;
        shotsAway.textContent = '10 (4)';
      }

      const xgHome = document.getElementById('stat-xg-home');
      const xgAway = document.getElementById('stat-xg-away');
      const barXgHome = document.getElementById('bar-xg-home');
      const barXgAway = document.getElementById('bar-xg-away');
      if (xgHome && xgAway && barXgHome && barXgAway) {
        const xgVal = s.xg_per90 ? s.xg_per90.toFixed(2) : '1.45';
        xgHome.textContent = `${xgVal} xG/90`;
        xgAway.textContent = '0.85';
        barXgHome.style.width = '63%';
        barXgAway.style.width = '37%';
      }

      const passHome = document.getElementById('stat-pass-home');
      const passAway = document.getElementById('stat-pass-away');
      if (passHome && passAway) {
        const kp = s.key_passes_per90 ? `${s.key_passes_per90} KP/90` : '512';
        passHome.textContent = kp;
        passAway.textContent = '380';
      }
    }

    function resetToWorldCupShowcase() {
      currentPlayerTacticsData = null;
      tacticsMode = 'match';

      const btnMatch = document.getElementById('tactics-mode-match');
      const btnPlayer = document.getElementById('tactics-mode-player');
      const btnSim = document.getElementById('tactics-mode-sim');
      if (btnMatch) btnMatch.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm';
      if (btnPlayer) {
        btnPlayer.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-1.5';
      }
      if (btnSim) btnSim.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-1.5';

      const btnMatchTitle = document.getElementById('tactics-mode-match-title');
      const btnMatchSub = document.getElementById('tactics-mode-match-sub');
      if (btnMatchTitle) btnMatchTitle.textContent = '🏆 실제 경기 하이라이트';
      if (btnMatchSub) btnMatchSub.textContent = '(대한민국 2:1 포르투갈)';

      const btnPlayerTitle = document.getElementById('tactics-mode-player-title');
      const btnPlayerSub = document.getElementById('tactics-mode-player-sub');
      if (btnPlayerTitle) btnPlayerTitle.textContent = '👤 선수별 집중 모먼트';
      if (btnPlayerSub) btnPlayerSub.textContent = '(손흥민·이강인·황희찬·김민재)';

      const homeEl = document.getElementById('tactics-team-home');
      const awayEl = document.getElementById('tactics-team-away');
      const formHomeEl = document.getElementById('tactics-form-home');
      const formAwayEl = document.getElementById('tactics-form-away');
      if (homeEl) homeEl.textContent = '대한민국';
      if (awayEl) awayEl.textContent = '포르투갈';
      if (formHomeEl) formHomeEl.textContent = '(4-2-3-1)';
      if (formAwayEl) formAwayEl.textContent = '(4-3-3)';
      document.getElementById('tactics-score-home').textContent = '2';
      document.getElementById('tactics-score-away').textContent = '1';
      document.getElementById('tactics-status-badge').textContent = 'FT 16강 진출';

      const legHome = document.getElementById('legend-home-team');
      const legAway = document.getElementById('legend-away-team');
      if (legHome) legHome.innerHTML = '🔵 <b class="text-zinc-200">대한민국</b>: 손흥민·황희찬·이강인·김민재 등';
      if (legAway) legAway.innerHTML = '🔴 <b class="text-zinc-200">포르투갈</b>: 호날두·페페·달로트·호르타 등';

      const ytExtBtn = document.getElementById('tactics-yt-external-btn');
      if (ytExtBtn) ytExtBtn.href = 'https://www.youtube.com/watch?v=DVNwiAPuPTY';

      initTacticsPlayers();
      renderDefaultChapterButtons();
      renderTacticsEventLog();

      const ytFrame = document.getElementById('tactics-yt-frame');
      if (ytFrame) {
        ytFrame.src = 'https://www.youtube.com/embed/DVNwiAPuPTY?enablejsapi=1&rel=0&modestbranding=1';
        ytFrame.title = '2022 World Cup South Korea vs Portugal Highlight';
      }

      playMatchHighlight('goal_kor_02');
    }

    function renderDefaultChapterButtons() {
      const container = document.getElementById('tactics-chapter-buttons');
      if (!container) return;
      const hintEl = document.getElementById('tactics-chapter-hint');
      if (hintEl) hintEl.textContent = '버튼 클릭 시 해당 좌표 2D 피치 이동 및 영상 싱크 재생';

      container.innerHTML = `
        <button onclick="playMatchHighlight('goal_por_01')"
          class="px-2.5 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-300 hover:text-white transition flex items-center gap-1.5">
          <span class="text-rose-400 font-mono font-bold">04:53</span>
          <span>⚽ 호르타 선제골 (xG 0.29)</span>
        </button>
        <button onclick="playMatchHighlight('goal_kor_01')"
          class="px-2.5 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-300 hover:text-white transition flex items-center gap-1.5">
          <span class="text-emerald-400 font-mono font-bold">26:43</span>
          <span>⚽ 김영권 동점골 (이강인 코너킥 기점, xG 0.62)</span>
        </button>
        <button onclick="playMatchHighlight('goal_kor_02')"
          class="px-2.5 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/40 text-xs text-emerald-300 hover:text-white transition flex items-center gap-1.5 font-semibold">
          <span class="text-emerald-400 font-mono font-bold">90:28</span>
          <span>⚽ 황희찬 극장 역전 결승골 (손흥민 70m 질주 어시스트, xG 0.42)</span>
        </button>
        <button onclick="playPlayerMoment('손흥민', 0)"
          class="px-2.5 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-300 hover:text-white transition flex items-center gap-1.5">
          <span class="text-amber-400 font-mono font-bold">15:21</span>
          <span>🎯 손흥민 감아차기 슈팅</span>
        </button>
        <button onclick="playPlayerMoment('이강인', 1)"
          class="px-2.5 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-300 hover:text-white transition flex items-center gap-1.5">
          <span class="text-blue-400 font-mono font-bold">41:18</span>
          <span>🎯 이강인 30m 킬스루패스</span>
        </button>
        <button onclick="playPlayerMoment('김민재', 1)"
          class="px-2.5 py-1.5 rounded-lg bg-[#0e1117] hover:bg-zinc-800 border border-white/[0.08] text-xs text-zinc-300 hover:text-white transition flex items-center gap-1.5">
          <span class="text-indigo-400 font-mono font-bold">34:20</span>
          <span>🛡️ 김민재 호날두 1:1 차단 태클</span>
        </button>
      `;
    }

    // Cross-link from Scouting Desk to Tactics Desk
    async function openTacticsForSelectedPlayer() {
      showPage('page-tactics');

      const p = selectedPlayer;
      if (!p) {
        resetToWorldCupShowcase();
        return;
      }

      const pName = p.name || p.name_ko || '';
      await loadPlayerTacticsHighlights(pName);
    }

    // Switch between Match, Player Moments & Autonomous FM Sim
    function switchTacticsMode(mode) {
      tacticsMode = mode;
      const btnMatch = document.getElementById('tactics-mode-match');
      const btnPlayer = document.getElementById('tactics-mode-player');
      const btnSim = document.getElementById('tactics-mode-sim');

      [btnMatch, btnPlayer, btnSim].forEach(btn => {
        if (!btn) return;
        btn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700 transition flex items-center gap-1.5';
      });

      if (mode === 'match') {
        if (btnMatch) btnMatch.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm';
        if (currentPlayerTacticsData) {
          // Stay in target player's club match context
          playTargetPlayerHighlight(0);
          updateCommentary('MATCH', `[공식 경기 전술] ${currentPlayerTacticsData.match_info.home_team} 2 : 1 ${currentPlayerTacticsData.match_info.away_team} 소속팀 공식 전술 대형 & 하이라이트`);
        } else if (selectedPlayer) {
          loadPlayerTacticsHighlights(selectedPlayer.name || selectedPlayer.name_ko);
        } else {
          resetToWorldCupShowcase();
        }
      } else if (mode === 'player') {
        if (btnPlayer) btnPlayer.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm';
        if (currentPlayerTacticsData) {
          playTargetPlayerHighlight(0);
        } else if (selectedPlayer) {
          loadPlayerTacticsHighlights(selectedPlayer.name || selectedPlayer.name_ko);
        } else {
          loadPlayerTacticsHighlights('손흥민');
        }
      } else if (mode === 'sim') {
        if (btnSim) btnSim.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 text-white transition flex items-center gap-1.5 shadow-sm';
        tacticsTrajectories = [];
        activeHighlightAnim = null;
        updateCommentary('SIM', 'FM 2D 자율 시뮬레이션 가동! 18×12 바둑판 그리드 상에서 22명 AI 선수가 자율적으로 전술 패스 및 압박을 수행합니다.');
      }
    }

    function toggleTacticsPlay() {
      isTacticsRunning = !isTacticsRunning;
      const icon = document.getElementById('btn-tactics-play-icon');
      const text = document.getElementById('btn-tactics-play-text');
      if (icon && text) {
        icon.textContent = isTacticsRunning ? '⏸️' : '▶️';
        text.textContent = isTacticsRunning ? '일시정지' : '재생';
      }
    }

    function setTacticsSpeed(s) {
      tacticsSpeed = s;
      ['btn-speed-1', 'btn-speed-2', 'btn-speed-4'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.className = 'px-2 py-1 rounded text-zinc-400 hover:text-white';
      });
      const activeEl = document.getElementById(`btn-speed-${s}`);
      if (activeEl) activeEl.className = 'px-2 py-1 rounded text-white bg-zinc-800 font-semibold';
    }

    function toggleTacticsOverlay(key) {
      const chk = document.getElementById(`chk-${key}`);
      if (chk) tacticsOverlays[key] = chk.checked;
    }

    function resetTacticsMatch() {
      isTacticsRunning = true;
      const icon = document.getElementById('btn-tactics-play-icon');
      const text = document.getElementById('btn-tactics-play-text');
      if (icon && text) {
        icon.textContent = '⏸️';
        text.textContent = '일시정지';
      }

      tacticsTrajectories = [];
      activeHighlightAnim = null;

      if (currentReplayContext.mode === 'player' && currentPlayerTacticsData) {
        playTargetPlayerHighlight(currentReplayContext.momentIdx || 0);
      } else if (currentReplayContext.mode === 'match') {
        if (currentReplayContext.highlightId) {
          playMatchHighlight(currentReplayContext.highlightId);
        } else if (currentReplayContext.playerName !== null) {
          playPlayerMoment(currentReplayContext.playerName, currentReplayContext.momentIdx || 0);
        } else {
          playMatchHighlight('goal_kor_02');
        }
      } else if (currentPlayerTacticsData) {
        playTargetPlayerHighlight(0);
      } else {
        initTacticsPlayers();
        playMatchHighlight('goal_kor_02');
      }
    }

    function replayCurrentHighlight() {
      resetTacticsMatch();
    }

    function updateCommentary(badge, text) {
      const badgeEl = document.getElementById('tactics-comm-badge');
      const textEl = document.getElementById('tactics-comm-text');
      if (badgeEl) badgeEl.textContent = badge;
      if (textEl) textEl.textContent = text;
    }

    function triggerGoalBanner(text) {
      const banner = document.getElementById('tactics-goal-banner');
      const goalText = document.getElementById('tactics-goal-text');
      if (banner && goalText) {
        goalText.textContent = text;
        banner.classList.remove('hidden');
        tacticsGoalBannerTimer = 180;
      }
    }

    // Video Sync Seek (YouTube iframe or local MP4 video)
    function seekTacticsVideo(timeInSec) {
      const ytFrame = document.getElementById('tactics-yt-frame');
      const localVid = document.getElementById('tactics-local-video');
      const statusEl = document.getElementById('video-sync-status');

      if (localVid && !localVid.classList.contains('hidden')) {
        localVid.currentTime = timeInSec;
        localVid.play().catch(() => {});
        if (statusEl) statusEl.textContent = `SYNC: ${Math.floor(timeInSec / 60)}:${('0' + (timeInSec % 60)).slice(-2)}`;
      } else if (ytFrame) {
        // Reload YouTube embed with new start parameter using active match's videoId
        const videoId = (currentPlayerTacticsData && currentPlayerTacticsData.match_info && currentPlayerTacticsData.match_info.youtube_highlight_id)
          ? currentPlayerTacticsData.match_info.youtube_highlight_id
          : 'DVNwiAPuPTY';
        ytFrame.src = `https://www.youtube.com/embed/${videoId}?enablejsapi=1&rel=0&modestbranding=1&start=${Math.floor(timeInSec)}&autoplay=1`;
        if (statusEl) statusEl.textContent = `SYNC: ${Math.floor(timeInSec / 60)}:${('0' + (timeInSec % 60)).slice(-2)}`;
      }
    }

    function handleTacticsVideoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const ytFrame = document.getElementById('tactics-yt-frame');
      const localVid = document.getElementById('tactics-local-video');
      const statusEl = document.getElementById('video-sync-status');

      if (ytFrame && localVid) {
        ytFrame.classList.add('hidden');
        localVid.classList.remove('hidden');
        localVid.src = URL.createObjectURL(file);
        localVid.play().catch(() => {});
        if (statusEl) statusEl.textContent = `LOCAL MP4: ${file.name.slice(0, 15)}...`;
      }
    }

    // =========================================================================
    // Main 2D Tactical Pitch Canvas Render Engine
    // =========================================================================
    function drawTacticsPitch() {
      if (!tacticsCtx || !tacticsCanvas) return;
      const ctx = tacticsCtx;
      const W = tacticsCanvas.width;
      const H = tacticsCanvas.height;
      const margin = TACTICS_PITCH_MARGIN;
      const pw = TACTICS_PITCH_W;
      const ph = TACTICS_PITCH_H;

      ctx.clearRect(0, 0, W, H);

      // Pitch Grass Background
      ctx.fillStyle = '#061714';
      ctx.fillRect(0, 0, W, H);

      // Subtle Alternating Turf Stripes (18 vertical stripes)
      for (let c = 0; c < TACTICS_GRID_COLS; c++) {
        ctx.fillStyle = (c % 2 === 0) ? '#081c18' : '#0a211d';
        ctx.fillRect(margin + c * TACTICS_CELL_W, margin, TACTICS_CELL_W, ph);
      }

      // 5 Half-Space Tactical Zones Overlay (Guardiola 5-Corridor Framework)
      if (tacticsOverlays.zones) {
        const zoneHeight = ph / 5;
        const zoneNames = ['Left Wing', 'Left Half-Space', 'Central Corridor', 'Right Half-Space', 'Right Wing'];
        const zoneColors = [
          'rgba(59, 130, 246, 0.03)',
          'rgba(16, 185, 129, 0.06)',
          'rgba(245, 158, 11, 0.03)',
          'rgba(16, 185, 129, 0.06)',
          'rgba(59, 130, 246, 0.03)'
        ];

        for (let z = 0; z < 5; z++) {
          ctx.fillStyle = zoneColors[z];
          ctx.fillRect(margin, margin + z * zoneHeight, pw, zoneHeight);

          ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
          ctx.lineWidth = 1;
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.moveTo(margin, margin + z * zoneHeight);
          ctx.lineTo(margin + pw, margin + z * zoneHeight);
          ctx.stroke();
          ctx.setLineDash([]);

          ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
          ctx.font = '9px monospace';
          ctx.fillText(zoneNames[z], margin + 8, margin + z * zoneHeight + 14);
        }
      }

      // 18x12 Tactical Grid Overlay
      if (tacticsOverlays.grid) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
        ctx.lineWidth = 1;

        for (let c = 0; c <= TACTICS_GRID_COLS; c++) {
          const x = margin + c * TACTICS_CELL_W;
          ctx.beginPath();
          ctx.moveTo(x, margin);
          ctx.lineTo(x, margin + ph);
          ctx.stroke();
        }

        for (let r = 0; r <= TACTICS_GRID_ROWS; r++) {
          const y = margin + r * TACTICS_CELL_H;
          ctx.beginPath();
          ctx.moveTo(margin, y);
          ctx.lineTo(margin + pw, y);
          ctx.stroke();
        }
      }

      // Official Pitch Markings (White)
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 2;

      // Touchlines & Goal lines
      ctx.strokeRect(margin, margin, pw, ph);

      // Halfway Line
      const midX = margin + pw * 0.5;
      ctx.beginPath();
      ctx.moveTo(midX, margin);
      ctx.lineTo(midX, margin + ph);
      ctx.stroke();

      // Center Circle & Spot
      const midY = margin + ph * 0.5;
      ctx.beginPath();
      ctx.arc(midX, midY, 65, 0, Math.PI * 2);
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(midX, midY, 3, 0, Math.PI * 2);
      ctx.fill();

      // Penalty Boxes (18-yard box: approx 3.0 grid cols wide)
      const penBoxW = TACTICS_CELL_W * 3.0;
      const penBoxH = TACTICS_CELL_H * 6.0;
      const penBoxY = margin + (ph - penBoxH) * 0.5;

      // Home Penalty Box (Left)
      ctx.strokeRect(margin, penBoxY, penBoxW, penBoxH);
      // Away Penalty Box (Right)
      ctx.strokeRect(margin + pw - penBoxW, penBoxY, penBoxW, penBoxH);

      // 6-Yard Goal Areas
      const goalAreaW = TACTICS_CELL_W * 1.0;
      const goalAreaH = TACTICS_CELL_H * 3.0;
      const goalAreaY = margin + (ph - goalAreaH) * 0.5;

      ctx.strokeRect(margin, goalAreaY, goalAreaW, goalAreaH);
      ctx.strokeRect(margin + pw - goalAreaW, goalAreaY, goalAreaW, goalAreaH);

      // Penalty Spots
      ctx.beginPath();
      ctx.arc(margin + TACTICS_CELL_W * 2.0, midY, 2.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(margin + pw - TACTICS_CELL_W * 2.0, midY, 2.5, 0, Math.PI * 2);
      ctx.fill();

      // Goals (Outside Touchline)
      const goalNetH = TACTICS_CELL_H * 2.0;
      const goalNetY = margin + (ph - goalNetH) * 0.5;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
      ctx.strokeRect(margin - 12, goalNetY, 12, goalNetH);
      ctx.strokeRect(margin + pw, goalNetY, 12, goalNetH);

      // Draw Trajectories (Pass & Shot Lines)
      tacticsTrajectories.forEach(tr => {
        ctx.save();
        if (tr.alpha !== undefined) ctx.globalAlpha = Math.max(0, Math.min(1, tr.alpha));
        ctx.strokeStyle = tr.color;
        ctx.lineWidth = tr.dashed ? 2 : 3;
        if (tr.dashed) ctx.setLineDash([6, 4]);
        else ctx.setLineDash([]);

        ctx.beginPath();
        ctx.moveTo(tr.x1, tr.y1);
        ctx.lineTo(tr.x2, tr.y2);
        ctx.stroke();
        ctx.setLineDash([]);

        // Arrowhead
        const angle = Math.atan2(tr.y2 - tr.y1, tr.x2 - tr.x1);
        ctx.fillStyle = tr.color;
        ctx.beginPath();
        ctx.moveTo(tr.x2, tr.y2);
        ctx.lineTo(tr.x2 - 10 * Math.cos(angle - Math.PI / 6), tr.y2 - 10 * Math.sin(angle - Math.PI / 6));
        ctx.lineTo(tr.x2 - 10 * Math.cos(angle + Math.PI / 6), tr.y2 - 10 * Math.sin(angle + Math.PI / 6));
        ctx.closePath();
        ctx.fill();

        // Trajectory Label
        if (tr.label) {
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 10px sans-serif';
          ctx.shadowColor = 'rgba(0,0,0,0.8)';
          ctx.shadowBlur = 4;
          const labelX = (tr.x1 + tr.x2) * 0.5;
          const labelY = (tr.y1 + tr.y2) * 0.5 - 6;
          ctx.fillText(tr.label, labelX - 20, labelY);
          ctx.shadowBlur = 0;
        }
        ctx.restore();
      });

      // Draw Action Map (90-Minute FM Player Spatial Touch & Decisive Action Pins)
      if (tacticsOverlays.actionMap && currentPlayerTacticsData && currentPlayerTacticsData.action_map && currentPlayerTacticsData.action_map.length > 0) {
        const acts = currentPlayerTacticsData.action_map;

        // 1. Dotted Flow Line connecting sequential actions across the 90 minutes
        ctx.save();
        ctx.strokeStyle = 'rgba(251, 191, 36, 0.4)';
        ctx.lineWidth = 1.8;
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        acts.forEach((act, idx) => {
          const pt = statsBombToPixel(act.location[0], act.location[1]);
          if (idx === 0) ctx.moveTo(pt.x, pt.y);
          else ctx.lineTo(pt.x, pt.y);
        });
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.restore();

        // 2. Action Pins
        acts.forEach((act) => {
          const pt = statsBombToPixel(act.location[0], act.location[1]);
          const isHovered = hoveredActionPin && hoveredActionPin.minute === act.minute;
          const pinColor = act.color || '#f59e0b';

          ctx.save();

          // Outer Glow
          ctx.fillStyle = isHovered ? 'rgba(251, 191, 36, 0.45)' : 'rgba(251, 191, 36, 0.18)';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, isHovered ? 18 : 14, 0, Math.PI * 2);
          ctx.fill();

          // Pin Circle Body
          ctx.fillStyle = isHovered ? '#1e293b' : '#0f172a';
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, isHovered ? 13 : 11, 0, Math.PI * 2);
          ctx.fill();

          // Border Ring
          ctx.strokeStyle = isHovered ? '#fbbf24' : pinColor;
          ctx.lineWidth = isHovered ? 2.5 : 1.8;
          ctx.stroke();

          // Icon or minute inside pin
          ctx.font = isHovered ? 'bold 11px sans-serif' : 'bold 9px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = '#ffffff';
          ctx.fillText(act.icon || '📍', pt.x, pt.y);

          // Minute Pill below pin
          const minText = `${act.minute}'`;
          ctx.font = 'bold 9px sans-serif';
          const tw = ctx.measureText(minText).width;
          const badgeW = tw + 8;
          const badgeH = 14;
          const badgeX = pt.x - badgeW / 2;
          const badgeY = pt.y + (isHovered ? 16 : 14);

          ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
          ctx.beginPath();
          if (ctx.roundRect) ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 4);
          else ctx.rect(badgeX, badgeY, badgeW, badgeH);
          ctx.fill();

          ctx.strokeStyle = isHovered ? '#fbbf24' : 'rgba(255,255,255,0.2)';
          ctx.lineWidth = 1;
          ctx.stroke();

          ctx.fillStyle = isHovered ? '#fde047' : '#94a3b8';
          ctx.fillText(minText, pt.x, badgeY + badgeH / 2);

          ctx.restore();
        });
      }

      // Draw Players
      tacticsPlayers.forEach(p => {
        const isSelected = p.id === tacticsSelectedPlayerId;
        const isHome = p.team === 'home';

        // 1. Vision Cone (FOV Overlay)
        if (tacticsOverlays.fov) {
          const fovAngle = Math.PI / 3; // 60 degrees
          const fovDist = isSelected ? 85 : 55;
          const startAngle = p.angle - fovAngle / 2;
          const endAngle = p.angle + fovAngle / 2;

          ctx.fillStyle = isSelected
            ? 'rgba(251, 191, 36, 0.15)'
            : (isHome ? 'rgba(59, 130, 246, 0.08)' : 'rgba(239, 68, 68, 0.08)');

          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.arc(p.x, p.y, fovDist, startAngle, endAngle);
          ctx.closePath();
          ctx.fill();
        }

        // 2. Spotlight Ring (if selected or is_target)
        const isTarget = p.is_target === true;
        if ((isSelected || isTarget) && tacticsOverlays.spotlight) {
          ctx.strokeStyle = isTarget ? '#f59e0b' : '#fbbf24';
          ctx.lineWidth = isTarget ? 3.0 : 2.5;
          ctx.setLineDash([4, 3]);
          ctx.beginPath();
          ctx.arc(p.x, p.y, isTarget ? 24 : 22, 0, Math.PI * 2);
          ctx.stroke();
          ctx.setLineDash([]);
        }

        // 3. Stamina Ring
        ctx.strokeStyle = p.stamina > 50 ? '#10b981' : '#ef4444';
        ctx.lineWidth = 2;
        ctx.beginPath();
        const staminaArc = (p.stamina / 100) * Math.PI * 2;
        ctx.arc(p.x, p.y, 14, -Math.PI / 2, -Math.PI / 2 + staminaArc);
        ctx.stroke();

        // 4. Player Body Dot
        ctx.fillStyle = isTarget ? '#f59e0b' : (isHome ? '#2563eb' : '#dc2626');
        ctx.beginPath();
        ctx.arc(p.x, p.y, isTarget ? 13 : 11, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = isTarget ? 2.2 : 1.5;
        ctx.stroke();

        // 5. Jersey Number
        ctx.fillStyle = '#ffffff';
        ctx.font = isTarget ? 'bold 10px sans-serif' : 'bold 9px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.num.toString(), p.x, p.y);

        // 6. Name Label
        ctx.fillStyle = isTarget ? '#fde047' : (isSelected ? '#fef08a' : '#e2e8f0');
        ctx.font = isTarget ? 'bold 12px sans-serif' : (isSelected ? 'bold 11px sans-serif' : '10px sans-serif');
        ctx.fillText((isTarget ? '★ ' : '') + p.name, p.x, p.y + (isTarget ? 21 : 19));

        ctx.textAlign = 'start';
        ctx.textBaseline = 'alphabetic';
      });

      // Draw Ball
      ctx.fillStyle = 'rgba(0,0,0,0.4)';
      ctx.beginPath();
      ctx.arc(tacticsBall.x + 2, tacticsBall.y + 3, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(tacticsBall.x, tacticsBall.y, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#111827';
      ctx.lineWidth = 1.2;
      ctx.stroke();

      // Floating Tactical Ability Pill Badge above target player
      if (activeHighlightAnim && activeHighlightAnim.targetPlayer && activeHighlightAnim.tacticalTag) {
        const tp = activeHighlightAnim.targetPlayer;
        const tagText = activeHighlightAnim.tacticalTag;
        const tagColor = activeHighlightAnim.tagColor || '#10b981';
        ctx.save();
        ctx.font = 'bold 11px sans-serif';
        const textWidth = ctx.measureText(tagText).width;
        const pillW = textWidth + 20;
        const pillH = 22;
        let pillX = tp.x - pillW / 2;
        let pillY = tp.y - 34;

        if (pillY < TACTICS_PITCH_MARGIN + 4) pillY = tp.y + 28;
        if (pillX < TACTICS_PITCH_MARGIN + 4) pillX = TACTICS_PITCH_MARGIN + 4;
        if (pillX + pillW > TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 4) {
          pillX = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 4 - pillW;
        }

        ctx.shadowColor = 'rgba(0,0,0,0.85)';
        ctx.shadowBlur = 8;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.94)';
        ctx.beginPath();
        if (ctx.roundRect) {
          ctx.roundRect(pillX, pillY, pillW, pillH, 11);
        } else {
          ctx.rect(pillX, pillY, pillW, pillH);
        }
        ctx.fill();

        ctx.strokeStyle = tagColor;
        ctx.lineWidth = 1.6;
        ctx.stroke();

        ctx.shadowBlur = 0;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(tagText, pillX + pillW / 2, pillY + pillH / 2);
        ctx.restore();
      }

      // Interactive Tooltip for Hovered Action Map Pin
      if (tacticsOverlays.actionMap && hoveredActionPin) {
        const act = hoveredActionPin;
        const pt = statsBombToPixel(act.location[0], act.location[1]);
        ctx.save();

        const cardW = 220;
        const cardH = 76;
        let cardX = pt.x + 16;
        let cardY = pt.y - cardH / 2;

        if (cardX + cardW > margin + pw - 8) cardX = pt.x - cardW - 16;
        if (cardY < margin + 8) cardY = margin + 8;
        if (cardY + cardH > margin + ph - 8) cardY = margin + ph - 8 - cardH;

        // Card Shadow & Background Glassmorphism
        ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
        ctx.shadowBlur = 12;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.96)';
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(cardX, cardY, cardW, cardH, 8);
        else ctx.rect(cardX, cardY, cardW, cardH);
        ctx.fill();

        ctx.strokeStyle = act.color || '#38bdf8';
        ctx.lineWidth = 1.8;
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Header: [icon] display_time | zone
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.font = 'bold 11px sans-serif';
        ctx.fillStyle = '#fde047';
        ctx.fillText(`${act.icon} ${act.display_time} • ${act.zone}`, cardX + 10, cardY + 8);

        // Title
        ctx.font = 'bold 10px sans-serif';
        ctx.fillStyle = '#ffffff';
        let displayTitle = act.title;
        if (displayTitle.length > 25) displayTitle = displayTitle.substring(0, 24) + '...';
        ctx.fillText(displayTitle, cardX + 10, cardY + 26);

        // Description
        ctx.font = '9px sans-serif';
        ctx.fillStyle = '#94a3b8';
        let descText = act.desc;
        if (descText.length > 32) descText = descText.substring(0, 31) + '...';
        ctx.fillText(descText, cardX + 10, cardY + 43);

        // Footer action hint
        ctx.font = 'bold 9px sans-serif';
        ctx.fillStyle = act.highlight_idx !== undefined && act.highlight_idx !== null ? '#10b981' : '#a855f7';
        const hintText = act.highlight_idx !== undefined && act.highlight_idx !== null ? '▶️ 클릭 시 전술 하이라이트 리플레이' : '📍 90분 전술 히트맵 핵심 활약 구역';
        ctx.fillText(hintText, cardX + 10, cardY + 59);

        ctx.restore();
      }

      // FM Match Performance Rating & Tactical Summary Top Badge (when in player scouting mode)
      if (currentPlayerTacticsData && currentPlayerTacticsData.match_summary) {
        const ms = currentPlayerTacticsData.match_summary;
        const pInfo = currentPlayerTacticsData.player_info;
        const pName = pInfo.name_ko || pInfo.name;

        ctx.save();
        const badgeX = margin + 12;
        const badgeY = margin + 12;
        const badgeW = 290;
        const badgeH = 42;

        ctx.shadowColor = 'rgba(0,0,0,0.6)';
        ctx.shadowBlur = 8;
        ctx.fillStyle = 'rgba(10, 15, 29, 0.88)';
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 8);
        else ctx.rect(badgeX, badgeY, badgeW, badgeH);
        ctx.fill();

        ctx.strokeStyle = 'rgba(251, 191, 36, 0.4)';
        ctx.lineWidth = 1.2;
        ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';

        // Line 1: Star Rating & MoM
        ctx.font = 'bold 11px sans-serif';
        ctx.fillStyle = '#fbbf24';
        const momBadge = ms.mom ? ' ★ MoM' : '';
        ctx.fillText(`⭐ FM 평점 ${ms.rating || '8.7'}${momBadge} | #${pInfo.num || '10'} ${pName} (${pInfo.position})`, badgeX + 10, badgeY + 7);

        // Line 2: Opta Metric Summary
        ctx.font = '10px sans-serif';
        ctx.fillStyle = '#cbd5e1';
        ctx.fillText(`볼터치 ${ms.touches || 74}회 • 키패스 ${ms.key_passes || 4}회 • 패스 ${ms.pass_accuracy || '89%'} • ${ms.distance_km || 11.4}km`, badgeX + 10, badgeY + 23);

        ctx.restore();
      }

      // Goal Banner Timer
      if (tacticsGoalBannerTimer > 0) {
        tacticsGoalBannerTimer -= tacticsSpeed;
        if (tacticsGoalBannerTimer <= 0) {
          const banner = document.getElementById('tactics-goal-banner');
          if (banner) banner.classList.add('hidden');
        }
      }
    }

    // Autonomous FM Simulation Living Match Flow (Continuous Flow for All Modes)
    function updateLivingMatchFlow() {
      livingMatchTimer += tacticsSpeed;
      if (!tacticsPlayers || tacticsPlayers.length === 0) return;

      const pitchLeft = TACTICS_PITCH_MARGIN + 12;
      const pitchRight = TACTICS_PITCH_MARGIN + TACTICS_PITCH_W - 12;
      const pitchTop = TACTICS_PITCH_MARGIN + 12;
      const pitchBottom = TACTICS_PITCH_MARGIN + TACTICS_PITCH_H - 12;

      // 1. Resolve Ball Possession / Owner
      let owner = tacticsPlayers.find(p => p.id === livingBallOwnerId);
      if (!owner) {
        const target = tacticsPlayers.find(p => p.is_target);
        if (target) {
          owner = target;
          livingBallOwnerId = target.id;
        } else {
          owner = tacticsPlayers.find(p => p.pos !== 'GK' && p.team === 'home') || tacticsPlayers[8];
          livingBallOwnerId = owner ? owner.id : null;
        }
      }

      // 2. Ball Motion & Pass Circulation
      if (tacticsBall.inFlight) {
        const dx = (tacticsBall.tx || tacticsBall.x) - tacticsBall.x;
        const dy = (tacticsBall.ty || tacticsBall.y) - tacticsBall.y;
        const dist = Math.hypot(dx, dy);

        if (dist < 8) {
          tacticsBall.x = tacticsBall.tx;
          tacticsBall.y = tacticsBall.ty;
          tacticsBall.inFlight = false;
          livingPassCooldown = 35 + Math.floor(Math.random() * 25);
        } else {
          const stepSpeed = Math.min(dist, 10 * tacticsSpeed);
          tacticsBall.x += (dx / dist) * stepSpeed;
          tacticsBall.y += (dy / dist) * stepSpeed;
        }
      } else if (owner) {
        // Owner dribbles / carries ball
        tacticsBall.x += (owner.x + Math.cos(owner.angle) * 8 - tacticsBall.x) * 0.25;
        tacticsBall.y += (owner.y + Math.sin(owner.angle) * 8 - tacticsBall.y) * 0.25;

        // Gentle forward movement for owner
        owner.x += Math.cos(owner.angle) * 0.5 * tacticsSpeed;
        owner.y += Math.sin(owner.angle) * 0.3 * tacticsSpeed;

        // Decrement pass cooldown
        livingPassCooldown -= tacticsSpeed;
        if (livingPassCooldown <= 0) {
          // Teammates eligible for pass
          const teammates = tacticsPlayers.filter(p => p.team === owner.team && p.id !== owner.id && p.pos !== 'GK');
          const targetPlayer = tacticsPlayers.find(p => p.is_target);

          let receiver = null;
          // In player scouting mode, pass to target star player ~65% of the time if owner is someone else
          if (targetPlayer && owner.id !== targetPlayer.id && Math.random() < 0.65) {
            receiver = targetPlayer;
          } else if (teammates.length > 0) {
            // Pick teammate with good forward position
            const forwardTeammates = teammates.filter(p => (owner.team === 'home' ? p.x > owner.x - 20 : p.x < owner.x + 20));
            const pool = forwardTeammates.length > 0 ? forwardTeammates : teammates;
            receiver = pool[Math.floor(Math.random() * pool.length)];
          }

          if (receiver) {
            tacticsBall.tx = receiver.x;
            tacticsBall.ty = receiver.y;
            tacticsBall.inFlight = true;
            livingBallOwnerId = receiver.id;

            tacticsTrajectories.push({
              x1: owner.x,
              y1: owner.y,
              x2: receiver.x,
              y2: receiver.y,
              color: '#38bdf8',
              dashed: true,
              alpha: 0.85,
              fade: true,
              label: `${owner.name} ➔ ${receiver.name}`
            });

            updateCommentary('PASS', `[실시간 빌드업] #${owner.num} ${owner.name} ➔ #${receiver.num} ${receiver.name} 패스 연결 (${Math.round(Math.hypot(receiver.x - owner.x, receiver.y - owner.y) * 0.12)}m)`);
          } else {
            livingPassCooldown = 30;
          }
        }
      }

      // 3. Natural Tactical Shift & Breathing for All 22 Players
      tacticsPlayers.forEach(p => {
        const basePt = tacticsGridToPixel(p.baseCol, p.baseRow);

        // Corridor shift toward ball
        const ballShiftX = (tacticsBall.x - (TACTICS_PITCH_MARGIN + TACTICS_PITCH_W * 0.5)) * 0.08;
        const ballShiftY = (tacticsBall.y - (TACTICS_PITCH_MARGIN + TACTICS_PITCH_H * 0.5)) * 0.05;

        // Sinusoidal movement jitter
        const jitterX = Math.sin(Date.now() * 0.0022 + p.num * 1.4) * 12;
        const jitterY = Math.cos(Date.now() * 0.002 + p.num * 1.8) * 8;

        const targetX = Math.max(pitchLeft, Math.min(pitchRight, basePt.x + ballShiftX + jitterX));
        const targetY = Math.max(pitchTop, Math.min(pitchBottom, basePt.y + ballShiftY + jitterY));

        p.x += (targetX - p.x) * 0.04 * tacticsSpeed;
        p.y += (targetY - p.y) * 0.04 * tacticsSpeed;

        // Orient toward ball
        p.angle = Math.atan2(tacticsBall.y - p.y, tacticsBall.x - p.x);
      });
    }

    // Master Tactics Simulation Physics Loop
    function updateTacticsSimulation() {
      if (!isTacticsRunning) return;

      // 1. Decay fading trajectory trails
      for (let i = tacticsTrajectories.length - 1; i >= 0; i--) {
        const tr = tacticsTrajectories[i];
        if (tr.fade) {
          tr.alpha = (tr.alpha || 1.0) - 0.012 * tacticsSpeed;
          if (tr.alpha <= 0) {
            tacticsTrajectories.splice(i, 1);
          }
        }
      }

      // 2. Run Highlight Multi-Step Animation if active
      if (activeHighlightAnim) {
        updateHighlightAnimation();
        return;
      }

      // 3. Fall through to Living Match Flow (Continuous FM 2D Simulation)
      if (tacticsMode === 'sim') {
        updateLivingMatchFlow();
      }
    }

    // Main Animation Loop
    function tacticsLoop() {
      updateTacticsSimulation();
      drawTacticsPitch();
      tacticsAnimId = requestAnimationFrame(tacticsLoop);
    }

    // Hash change event listener
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.replace('#', '');
      if (hash && `page-${hash}` !== activePageId) {
        showPage(`page-${hash}`);
      }
    });


    // =========================================================================
    // STATE FOR PORTFOLIO, WATCHLIST & AUTHENTICATION
    // =========================================================================
    let cachedPortfolioData = null;
    let cachedRecruitmentData = null;
    let portfolioFilter = 'ALL';
    let portfolioSearchQuery = '';
    let currentRecCategory = 'ALL';
    let recruitmentSearchQuery = '';
    let currentAuthUser = null;
    let currentPitchMarkdown = '';
    let currentPitchTarget = '';

    // =========================================================================
    // AUTHENTICATION & ADMIN CONSOLE CONTROLLER
    // =========================================================================
    function initAuth() {
      const saved = localStorage.getItem('fc_agency_auth_user');
      if (saved) {
        try {
          currentAuthUser = JSON.parse(saved);
          updateAuthBadgeUI();
        } catch (e) {
          localStorage.removeItem('fc_agency_auth_user');
        }
      }
      if (!currentAuthUser) {
        // Default to admin for seamless experience
        currentAuthUser = {
          email: 'admin@agent.com',
          full_name: '김대표 Agent (대표 관리자)',
          department: '에이전시 대표실',
          role: 'ADMIN',
          is_admin: true
        };
        updateAuthBadgeUI();
      }
    }

    function updateAuthBadgeUI() {
      const textEl = document.getElementById('nav-auth-text');
      const badgeEl = document.getElementById('nav-auth-badge');
      if (!textEl || !badgeEl) return;

      if (currentAuthUser) {
        textEl.textContent = `인증: ${currentAuthUser.email}`;
        badgeEl.className = 'cursor-pointer text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:border-emerald-400 transition flex items-center gap-1.5';
      } else {
        textEl.textContent = '에이전시 로그인';
        badgeEl.className = 'cursor-pointer text-xs px-2.5 py-1 rounded-lg border border-white/[0.08] bg-[#12151c] text-zinc-400 hover:text-white transition flex items-center gap-1.5';
      }
    }

    function openAuthModal(defaultTab) {
      const modal = document.getElementById('modal-auth');
      if (!modal) return;
      modal.classList.remove('hidden');
      if (defaultTab) switchAuthTab(defaultTab);
    }

    function closeAuthModal() {
      const modal = document.getElementById('modal-auth');
      if (modal) modal.classList.add('hidden');
    }

    function switchAuthTab(tab) {
      const btnLogin = document.getElementById('auth-tab-btn-login');
      const btnSignup = document.getElementById('auth-tab-btn-signup');
      const formLogin = document.getElementById('form-auth-login');
      const formSignup = document.getElementById('form-auth-signup');
      const alertBox = document.getElementById('auth-alert-box');
      if (alertBox) alertBox.classList.add('hidden');

      if (tab === 'login') {
        btnLogin.className = 'flex-1 pb-2 text-xs font-bold text-emerald-400 border-b-2 border-emerald-400 transition text-center';
        btnSignup.className = 'flex-1 pb-2 text-xs font-medium text-zinc-400 hover:text-zinc-200 transition text-center';
        formLogin.classList.remove('hidden');
        formSignup.classList.add('hidden');
      } else {
        btnSignup.className = 'flex-1 pb-2 text-xs font-bold text-sky-400 border-b-2 border-sky-400 transition text-center';
        btnLogin.className = 'flex-1 pb-2 text-xs font-medium text-zinc-400 hover:text-zinc-200 transition text-center';
        formSignup.classList.remove('hidden');
        formLogin.classList.add('hidden');
      }
    }

    function fillAdminCredentials() {
      const emailInput = document.getElementById('login-email');
      const pwInput = document.getElementById('login-password');
      if (emailInput) emailInput.value = 'admin@agent.com';
      if (pwInput) pwInput.value = 'password1234';
      switchAuthTab('login');
    }

    async function submitLoginForm(e) {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const pw = document.getElementById('login-password').value;
      const alertBox = document.getElementById('auth-alert-box');

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, password: pw })
        });
        const data = await res.json();

        if (!res.ok) {
          alertBox.className = 'mb-3 p-2.5 rounded-lg text-xs bg-rose-500/10 text-rose-300 border border-rose-500/20';
          alertBox.textContent = data.detail || '로그인에 실패했습니다.';
          alertBox.classList.remove('hidden');
          return;
        }

        currentAuthUser = data.user;
        localStorage.setItem('fc_agency_auth_user', JSON.stringify(currentAuthUser));
        updateAuthBadgeUI();
        closeAuthModal();
        alert(`환영합니다, ${currentAuthUser.full_name || currentAuthUser.email} 님!`);
      } catch (err) {
        alert('로그인 통신 오류: ' + err.message);
      }
    }

    async function submitSignupForm(e) {
      e.preventDefault();
      const name = document.getElementById('signup-name').value.trim();
      const email = document.getElementById('signup-email').value.trim();
      const dept = document.getElementById('signup-department').value;
      const pw = document.getElementById('signup-password').value;
      const alertBox = document.getElementById('auth-alert-box');

      try {
        const res = await fetch('/api/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ full_name: name, email: email, department: dept, password: pw })
        });
        const data = await res.json();

        if (!res.ok) {
          alertBox.className = 'mb-3 p-2.5 rounded-lg text-xs bg-rose-500/10 text-rose-300 border border-rose-500/20';
          alertBox.textContent = data.detail || '가입 신청에 실패했습니다.';
          alertBox.classList.remove('hidden');
          return;
        }

        alertBox.className = 'mb-3 p-2.5 rounded-lg text-xs bg-emerald-500/10 text-emerald-300 border border-emerald-500/20';
        alertBox.textContent = data.message || '가입 신청이 완료되었습니다. 관리자 승인 후 로그인 가능합니다.';
        alertBox.classList.remove('hidden');
      } catch (err) {
        alert('가입 신청 통신 오류: ' + err.message);
      }
    }

    async function loadAdminDashboard() {
      try {
        const res = await fetch('/api/admin/users');
        if (!res.ok) throw new Error('관리자 데이터 조회 권한이 없습니다.');
        const data = await res.json();

        const pendingList = document.getElementById('admin-pending-users-list');
        const approvedList = document.getElementById('admin-approved-users-list');
        const pendingCount = document.getElementById('admin-pending-count');
        const approvedCount = document.getElementById('admin-approved-count');

        const pending = data.pending_users || [];
        const approved = data.approved_users || [];

        if (pendingCount) pendingCount.textContent = `${pending.length}명`;
        if (approvedCount) approvedCount.textContent = `${approved.length}명`;

        if (pendingList) {
          if (pending.length === 0) {
            pendingList.innerHTML = `<div class="p-4 text-center text-zinc-500 text-xs">현재 승인 대기 중인 직원이 없습니다.</div>`;
          } else {
            pendingList.innerHTML = pending.map(u => `
              <div class="p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-white">${u.full_name || u.email}</div>
                  <div class="text-[10px] text-zinc-400 font-mono">${u.email} · ${u.department || '미배치'}</div>
                </div>
                <button onclick="approvePendingUser(${u.id}, '${u.email}')"
                  class="px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition shadow-sm">
                  승인 처리
                </button>
              </div>
            `).join('');
          }
        }

        if (approvedList) {
          if (approved.length === 0) {
            approvedList.innerHTML = `<div class="p-4 text-center text-zinc-500 text-xs">등록된 임직원이 없습니다.</div>`;
          } else {
            approvedList.innerHTML = approved.map(u => `
              <div class="p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] flex items-center justify-between">
                <div>
                  <div class="text-xs font-bold text-white flex items-center gap-2">
                    <span>${u.full_name || u.email}</span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] ${u.role === 'ADMIN' ? 'bg-amber-500/10 text-amber-300' : 'bg-emerald-500/10 text-emerald-400'}">${u.role || 'AGENT'}</span>
                  </div>
                  <div class="text-[10px] text-zinc-400 font-mono">${u.email} · ${u.department || '일반직'}</div>
                </div>
                <span class="text-[10px] text-emerald-400 font-medium">활동중 (ACTIVE)</span>
              </div>
            `).join('');
          }
        }
      } catch (err) {
        console.error('loadAdminDashboard error:', err);
      }
    }

    async function approvePendingUser(userId, email) {
      if (!confirm(`[${email}] 직원의 가입을 승인하시겠습니까?`)) return;
      try {
        const res = await fetch('/api/admin/approve-user', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, role: 'AGENT' })
        });
        const data = await res.json();
        alert(data.message || '승인이 완료되었습니다.');
        loadAdminDashboard();
      } catch (err) {
        alert('승인 처리 통신 오류: ' + err.message);
      }
    }

    // =========================================================================
    // WATCHLIST CONTROLLER (스카우팅 -> 영입 관심 리스트 연동)
    // =========================================================================
    async function updateScoutingWatchlistButton(targetId, targetType) {
      const btn = document.getElementById('btn-scouting-watchlist');
      const icon = document.getElementById('scouting-watchlist-icon');
      const label = document.getElementById('scouting-watchlist-label');
      if (!btn || !icon || !label) return;

      try {
        const res = await fetch(`/api/agency/watchlist/check?target_id=${targetId}&target_type=${targetType}`);
        const data = await res.json();
        if (data.in_watchlist) {
          icon.textContent = '★';
          label.textContent = '영입 관심 해제 (Watchlist 등록됨)';
          btn.className = 'w-full py-2 px-3 rounded-lg bg-amber-500 text-black border border-amber-400 font-bold text-xs transition flex items-center justify-center gap-1.5 shadow-md shadow-amber-950/30';
        } else {
          icon.textContent = '⭐';
          label.textContent = '영입 관심 타깃 등록 (Watchlist)';
          btn.className = 'w-full py-2 px-3 rounded-lg bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-sm';
        }
      } catch (err) {
        console.error('check_watchlist error:', err);
      }
    }

    async function toggleCurrentPlayerWatchlist() {
      if (!selectedPlayer) {
        alert('먼저 스카우팅 로스터에서 선수 또는 감독을 선택해주세요.');
        return;
      }

      const targetId = selectedPlayer.player_id;
      const targetType = (selectedPlayer.position === 'MGR') ? 'MANAGER' : 'PLAYER';
      const targetName = selectedPlayer.name_ko || selectedPlayer.name;

      try {
        const res = await fetch('/api/agency/watchlist/toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_id: targetId, target_type: targetType })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('영입 관심 타깃 변경 실패: ' + (data.detail || '오류'));
          return;
        }

        // Update button state
        await updateScoutingWatchlistButton(targetId, targetType);

        // Reload recruitment targets and update counters
        loadAgencyRecruitmentTargets();

        alert(data.message || (data.in_watchlist ? `'${targetName}' 님이 영입 관심 리스트에 등록되었습니다!` : `'${targetName}' 님이 영입 관심 리스트에서 제외되었습니다.`));
      } catch (err) {
        alert('영입 관심 등록 통신 오류: ' + err.message);
      }
    }

    async function removeTargetFromWatchlist(targetId, targetType, targetName) {
      if (!confirm(`'${targetName}' 님을 영입 관심 리스트에서 제외하시겠습니까?`)) return;

      try {
        const res = await fetch('/api/agency/watchlist/toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_id: targetId, target_type: targetType })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('관심 제외 실패: ' + (data.detail || '오류'));
          return;
        }

        // Refresh targets
        loadAgencyRecruitmentTargets();
        if (selectedPlayer && selectedPlayer.player_id === targetId) {
          updateScoutingWatchlistButton(targetId, targetType);
        }
      } catch (err) {
        alert('관심 제외 통신 오류: ' + err.message);
      }
    }

    // =========================================================================
    // TALENT & MANAGER RECRUITMENT WATCHLIST CONTROLLER (PILLAR 2)
    // =========================================================================
    async function loadAgencyRecruitmentTargets() {
      try {
        const res = await fetch('/api/agency/recruitment-targets');
        if (!res.ok) throw new Error('Failed to fetch recruitment targets');
        cachedRecruitmentData = await res.json();

        const targets = cachedRecruitmentData.targets || [];
        const virtualCount = targets.filter(t => t.is_virtual).length;
        const scoutedCount = targets.filter(t => !t.is_virtual || t.category === 'SCOUTED_TARGET').length;
        const playerCount = targets.filter(t => t.target_type === 'PLAYER').length;
        const managerCount = targets.filter(t => t.target_type === 'MANAGER').length;

        // Update counters on page & header badges
        const countAllEl = document.getElementById('rec-count-all');
        const countPlayerEl = document.getElementById('rec-count-player');
        const countMgrEl = document.getElementById('rec-count-manager');
        const countVirtEl = document.getElementById('rec-count-virtual');
        const countScoutEl = document.getElementById('rec-count-scouted');

        if (countAllEl) countAllEl.textContent = targets.length;
        if (countPlayerEl) countPlayerEl.textContent = playerCount;
        if (countMgrEl) countMgrEl.textContent = managerCount;
        if (countVirtEl) countVirtEl.textContent = virtualCount;
        if (countScoutEl) countScoutEl.textContent = scoutedCount;

        const navWatchlistBadge = document.getElementById('nav-watchlist-count');
        if (navWatchlistBadge) navWatchlistBadge.textContent = targets.length;

        const bannerWatchlistBadge = document.getElementById('scouting-banner-watchlist-count');
        if (bannerWatchlistBadge) bannerWatchlistBadge.textContent = targets.length;

        const pfRecBadge = document.getElementById('portfolio-header-rec-count');
        if (pfRecBadge) pfRecBadge.textContent = targets.length;

        renderRecruitmentCards();
      } catch (err) {
        console.error('loadAgencyRecruitmentTargets error:', err);
      }
    }

    function filterRecruitmentTargets(cat) {
      currentRecCategory = cat;
      ['ALL', 'PLAYER', 'MANAGER', 'VIRTUAL', 'SCOUTED', 'UNREPRESENTED', 'EXPIRING_D6', 'TIER2_STEPUP', 'ELITE_MANAGER'].forEach(c => {
        const tab = document.getElementById(`rec-tab-${c}`);
        if (tab) {
          if (c === cat) {
            tab.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-500 text-black transition shadow-sm';
          } else {
            tab.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition';
          }
        }
      });
      renderRecruitmentCards();
    }

    function handleRecruitmentSearch(q) {
      recruitmentSearchQuery = (q || '').toLowerCase();
      renderRecruitmentCards();
    }

    function renderRecruitmentCards() {
      const grid = document.getElementById('recruitment-cards-grid');
      if (!grid || !cachedRecruitmentData) return;

      let targets = cachedRecruitmentData.targets || [];

      // Filter by Category Tab
      if (currentRecCategory === 'PLAYER') {
        targets = targets.filter(t => t.target_type === 'PLAYER');
      } else if (currentRecCategory === 'MANAGER') {
        targets = targets.filter(t => t.target_type === 'MANAGER');
      } else if (currentRecCategory === 'VIRTUAL') {
        targets = targets.filter(t => t.is_virtual);
      } else if (currentRecCategory === 'SCOUTED') {
        targets = targets.filter(t => !t.is_virtual || t.category === 'SCOUTED_TARGET');
      } else if (['UNREPRESENTED', 'EXPIRING_D6', 'TIER2_STEPUP', 'ELITE_MANAGER'].includes(currentRecCategory)) {
        targets = targets.filter(t => t.category === currentRecCategory);
      }

      // Filter by Search Query
      if (recruitmentSearchQuery) {
        targets = targets.filter(t => {
          const matchName = (t.name || '').toLowerCase().includes(recruitmentSearchQuery);
          const matchKo = (t.name_ko || '').toLowerCase().includes(recruitmentSearchQuery);
          const matchClub = (t.current_club || '').toLowerCase().includes(recruitmentSearchQuery);
          const matchNat = (t.player_nat || '').toLowerCase().includes(recruitmentSearchQuery);
          return matchName || matchKo || matchClub || matchNat;
        });
      }

      if (targets.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-zinc-500 text-sm ui-card bg-[#11141a]">
            선택한 조건의 영입 관심 타깃이 없습니다. 스카우팅 로스터에서 선수·감독을 발굴해 <strong>[⭐ 영입 관심 타깃 등록]</strong>을 눌러보세요.
          </div>
        `;
        return;
      }

      const catBadges = {
        'UNREPRESENTED': { label: '💎 무소속 원석', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
        'EXPIRING_D6': { label: '⏳ 대리계약 만료 임박 D-6', style: 'bg-amber-500/10 text-amber-300 border-amber-500/20' },
        'TIER2_STEPUP': { label: '🚀 메가에이전시 희망', style: 'bg-sky-500/10 text-sky-400 border-sky-500/20' },
        'ELITE_MANAGER': { label: '👔 차세대 명장 타깃', style: 'bg-purple-500/10 text-purple-400 border-purple-500/20' },
        'SCOUTED_TARGET': { label: '⭐ 스카우팅 발굴 관심', style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' }
      };

      grid.innerHTML = targets.map(target => {
        const catInfo = catBadges[target.category] || { label: target.category, style: 'bg-zinc-800 text-zinc-300 border-zinc-700' };
        const isPlayer = target.target_type === 'PLAYER';
        const isVirtual = target.is_virtual;
        const marketValStr = target.market_value_eur ? `€${(target.market_value_eur/1000000).toFixed(0)}M` : '-';
        const projValStr = target.projected_5yr_valuation_eur ? `€${(target.projected_5yr_valuation_eur/1000000).toFixed(0)}M` : '-';
        const roiStr = target.projected_agency_roi_eur ? `€${(target.projected_agency_roi_eur/1000000).toFixed(1)}M` : '-';
        const roleLabel = isPlayer ? (target.position || 'FW') : `감독 (${target.preferred_formation || '4-3-3'})`;

        return `
          <div class="ui-card p-5 border-white/[0.08] hover:border-amber-500/40 transition flex flex-col justify-between space-y-4 bg-[#11141a]">
            <div>
              <!-- Category Pill & Virtual Pool Badge -->
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${catInfo.style}">
                    ${catInfo.label}
                  </span>
                  ${isVirtual ? '<span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🧪 가상 풀</span>' : '<span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">⭐ 실제 발굴</span>'}
                </div>
                <button onclick="removeTargetFromWatchlist(${target.target_id}, '${target.target_type}', '${target.name_ko}')"
                  class="text-zinc-500 hover:text-rose-400 text-xs px-1.5 py-0.5 rounded hover:bg-zinc-800 transition" title="관심 리스트에서 제외">
                  ✕ 관심 해제
                </button>
              </div>

              <!-- Header Info -->
              <div class="flex items-start justify-between gap-3 mt-3">
                <div>
                  <h4 class="text-base font-bold text-white tracking-tight flex items-center gap-1.5">
                    <span>${target.name_ko}</span>
                    <span class="text-xs font-normal text-zinc-400 font-mono">${target.name}</span>
                  </h4>
                  <p class="text-xs text-zinc-400 mt-0.5">
                    <span class="text-zinc-200 font-medium">${target.current_club || '무소속 (FA)'}</span>
                    <span class="text-zinc-600">·</span>
                    <span>${target.league || '가상 리그'}</span>
                    <span class="text-zinc-600">·</span>
                    <span class="text-amber-400 font-mono font-medium">${roleLabel}</span>
                  </p>
                </div>
                <div class="text-right">
                  <div class="text-[10px] text-zinc-500 uppercase font-semibold">현재 시장가치</div>
                  <div class="text-sm font-bold text-white font-mono">${marketValStr}</div>
                </div>
              </div>
            </div>

            <!-- 4D Potential & Stardom Score Board -->
            <div class="grid grid-cols-3 gap-2 p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] text-center">
              <div>
                <div class="text-[10px] text-zinc-500">잠재력 포텐셜</div>
                <div class="text-base font-bold text-emerald-400 font-mono mt-0.5">${target.potential_ceiling_score || 95}점</div>
              </div>
              <div>
                <div class="text-[10px] text-zinc-500">스타성·마케팅</div>
                <div class="text-base font-bold text-amber-300 font-mono mt-0.5">${target.stardom_commercial_score || 90}점</div>
              </div>
              <div>
                <div class="text-[10px] text-zinc-500">에이전시 적합도</div>
                <div class="text-base font-bold text-sky-400 font-mono mt-0.5">${target.agency_fit_score || 90}점</div>
              </div>
            </div>

            <!-- Valuation & Agency Projected ROI -->
            <div class="flex items-center justify-between text-xs px-3 py-2 rounded-lg bg-amber-950/20 border border-amber-500/20">
              <div>
                <span class="text-zinc-400 text-[11px]">5개년 예상 가치: </span>
                <span class="font-bold text-white font-mono">${projValStr}</span>
              </div>
              <div>
                <span class="text-amber-300 text-[11px]">에이전시 기대수익: </span>
                <span class="font-bold text-amber-400 font-mono">${roiStr}</span>
              </div>
            </div>

            <!-- Scouting Rationale Preview -->
            <p class="text-xs text-zinc-400 leading-relaxed line-clamp-3 bg-[#0e1117] p-2.5 rounded-lg border border-white/[0.04]">
              ${target.recruitment_pitch_rationale || '글로벌 브랜드 및 스폰서십 연계와 빅클럽 이적 프로젝트를 대행합니다.'}
            </p>

            <!-- Actions -->
            <div class="grid grid-cols-2 gap-2 pt-1">
              <button onclick="generateRecruitmentPitch(${target.target_id}, '${target.target_type}', '${target.name_ko}')"
                class="px-3 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-md shadow-sky-950/30">
                <span>📊 1-Page 제안서 생성</span>
              </button>
              <button onclick="enrollRecruitmentTarget(${target.target_id}, '${target.target_type}', '${target.name_ko}')"
                class="px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-md shadow-emerald-950/30">
                <span>✍️ 전속 계약 체결</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    async function generateRecruitmentPitch(targetId, targetType, targetName) {
      try {
        const titleEl = document.getElementById('pitch-modal-title');
        const bodyEl = document.getElementById('pitch-modal-body');
        const enrollBtn = document.getElementById('btn-pitch-enroll-action');
        const modal = document.getElementById('modal-pitch-viewer');

        if (titleEl) titleEl.textContent = `[${targetName}] 1-Page Client Acquisition Pitch Deck`;
        if (bodyEl) bodyEl.innerHTML = `<div class="py-16 text-center text-zinc-400 text-sm">🔄 AI 에이전트가 4D 잠재력 지표 및 FIFA FFAR 맞춤 피치덱을 합성 중입니다...</div>`;
        if (enrollBtn) enrollBtn.onclick = () => enrollRecruitmentTarget(targetId, targetType, targetName);
        if (modal) modal.classList.remove('hidden');

        const res = await fetch('/api/agency/recruitment-pitch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_id: targetId, target_type: targetType })
        });
        const data = await res.json();

        if (!res.ok) {
          if (bodyEl) bodyEl.innerHTML = `<div class="p-4 bg-rose-500/10 text-rose-400 rounded-lg">피치덱 생성 실패: ${data.detail || '오류'}</div>`;
          return;
        }

        currentPitchMarkdown = data.pitch_deck_markdown || data.markdown_content || '';
        currentPitchTarget = targetName;
        if (bodyEl && typeof marked !== 'undefined') {
          bodyEl.innerHTML = marked.parse(currentPitchMarkdown);
        } else if (bodyEl) {
          bodyEl.innerHTML = `<pre class="whitespace-pre-wrap text-xs text-zinc-300 font-mono">${currentPitchMarkdown}</pre>`;
        }
      } catch (err) {
        alert('피치덱 생성 통신 오류: ' + err.message);
      }
    }

    function closePitchModal() {
      const modal = document.getElementById('modal-pitch-viewer');
      if (modal) modal.classList.add('hidden');
    }

    function downloadPitchMarkdown() {
      if (!currentPitchMarkdown) return;
      const blob = new Blob([currentPitchMarkdown], { type: 'text/markdown;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `Pitch_Deck_${currentPitchTarget || 'Client'}.md`;
      link.click();
      URL.revokeObjectURL(url);
    }

    async function enrollRecruitmentTarget(targetId, targetType, targetName) {
      const agentName = prompt(`[${targetName}] 전속 대리 계약을 체결하시겠습니까?
담당 리드 에이전트 성함을 입력해주세요:`, currentAuthUser?.full_name || '김대표 Agent');
      if (!agentName) return;

      const commRateStr = prompt('계약 수수료율(%)을 입력해주세요 (FIFA FFAR 표준: 5~10%):', '5.0');
      const commissionPct = parseFloat(commRateStr) || 5.0;

      try {
        const res = await fetch('/api/agency/enroll-client', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            target_id: targetId,
            target_type: targetType,
            lead_agent: agentName,
            commission_pct: commissionPct
          })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('소속 계약 체결 실패: ' + (data.detail || '오류'));
          return;
        }

        alert(data.message || `축하합니다! ${targetName} 님이 Antigravity Sports 전속 고객으로 등록되었습니다.`);
        closePitchModal();
        showPage('page-portfolio');
        loadAgencyPortfolio();
        loadAgencyRecruitmentTargets();
      } catch (err) {
        alert('계약 등록 통신 오류: ' + err.message);
      }
    }

    // =========================================================================
    // ACTIVE PORTFOLIO CONTROLLER & AGENCY BUSINESS LIFECYCLE (PILLAR 1)
    // =========================================================================
    async function loadAgencyPortfolio() {
      try {
        const res = await fetch('/api/agency/portfolio');
        if (!res.ok) throw new Error('Failed to fetch agency portfolio');
        cachedPortfolioData = await res.json();

        // Update KPI counters
        const summary = cachedPortfolioData.summary || {};
        const totalValEl = document.getElementById('portfolio-total-val');
        const totalCountEl = document.getElementById('portfolio-total-count');
        const wagesValEl = document.getElementById('portfolio-wages-val');
        const feeValEl = document.getElementById('portfolio-fee-val');
        const navPortCount = document.getElementById('nav-portfolio-count');

        const totalClients = summary.total_clients || 0;
        if (totalValEl) totalValEl.textContent = `€${((summary.total_portfolio_value_eur || 0) / 1000000).toFixed(1)}M`;
        if (totalCountEl) totalCountEl.textContent = `${totalClients}인`;
        if (wagesValEl) wagesValEl.textContent = `€${((summary.total_weekly_wages_eur || 0) / 1000).toFixed(0)}K / 주`;
        if (feeValEl) feeValEl.textContent = `€${((summary.annual_commission_potential_eur || 0) / 1000000).toFixed(2)}M / 년`;

        if (navPortCount) {
          navPortCount.textContent = totalClients;
          if (totalClients > 0) navPortCount.classList.remove('hidden');
          else navPortCount.classList.add('hidden');
        }

        renderPortfolioCards();
      } catch (err) {
        console.error('loadAgencyPortfolio error:', err);
      }
    }

    function filterPortfolio(filter) {
      portfolioFilter = filter;
      ['ALL', 'PLAYER', 'MANAGER', 'VIRTUAL', 'REAL'].forEach(f => {
        const btn = document.getElementById(`pf-btn-${f.toLowerCase()}`);
        if (btn) {
          if (f === filter) {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition';
          } else {
            btn.className = 'px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition';
          }
        }
      });
      renderPortfolioCards();
    }

    function handlePortfolioSearch(q) {
      portfolioSearchQuery = (q || '').toLowerCase();
      renderPortfolioCards();
    }

    function renderPortfolioCards() {
      const grid = document.getElementById('portfolio-cards-grid');
      if (!grid || !cachedPortfolioData) return;

      const players = (cachedPortfolioData.players || []).map(p => ({ ...p, type: 'PLAYER' }));
      const managers = (cachedPortfolioData.managers || []).map(m => ({ ...m, type: 'MANAGER' }));
      let all = [...players, ...managers];

      // Apply Filter
      if (portfolioFilter === 'PLAYER') all = all.filter(c => c.type === 'PLAYER');
      if (portfolioFilter === 'MANAGER') all = all.filter(c => c.type === 'MANAGER');
      if (portfolioFilter === 'VIRTUAL') all = all.filter(c => (c.client_id >= 90000) || (c.player_id >= 90000) || (c.manager_id >= 90000));
      if (portfolioFilter === 'REAL') all = all.filter(c => !((c.client_id >= 90000) || (c.player_id >= 90000) || (c.manager_id >= 90000)));

      // Apply Search Query
      if (portfolioSearchQuery) {
        all = all.filter(c => {
          const matchName = (c.client_name || '').toLowerCase().includes(portfolioSearchQuery);
          const matchKo = (c.client_name_ko || '').toLowerCase().includes(portfolioSearchQuery);
          const matchClub = (c.current_club || '').toLowerCase().includes(portfolioSearchQuery);
          return matchName || matchKo || matchClub;
        });
      }

      if (all.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full py-16 text-center text-zinc-500 text-sm ui-card bg-[#11141a]">
            현재 등록된 소속 전속 고객이 없습니다. <br>
            <button onclick="showPage('page-recruitment')" class="mt-3 px-3.5 py-2 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 font-semibold text-xs transition">
              ⭐ 영입 관심 리스트에서 신규 고객 계약 체결하기 →
            </button>
          </div>
        `;
        return;
      }

      grid.innerHTML = all.map(client => {
        const isPlayer = client.type === 'PLAYER';
        const clientId = client.client_id || (isPlayer ? client.player_id : client.manager_id);
        const nameKo = client.client_name_ko || client.client_name;
        const nameEn = client.client_name;
        const currentClub = client.current_club || '무소속 (FA)';
        const isFA = !currentClub || currentClub.includes('무직') || currentClub.includes('무소속') || currentClub.includes('자유계약') || currentClub === 'FA';
        const isVirtual = Boolean((clientId >= 90000) || (client.player_id >= 90000) || (client.manager_id >= 90000));

        const marketVal = client.market_value_eur ? `€${(client.market_value_eur / 1000000).toFixed(1)}M` : (client.estimated_buyout_eur ? `바이아웃 €${(client.estimated_buyout_eur/1000000).toFixed(0)}M` : 'N/A');
        const wage = client.weekly_wage_eur ? `€${Math.round(client.weekly_wage_eur / 1000)}K/주` : '-';
        const dDayStr = client.contract_expires ? `${client.contract_expires} 만료` : '2026.06.30 만료 (D-597)';

        return `
          <div class="ui-card p-5 border-white/[0.08] hover:border-emerald-500/40 transition flex flex-col justify-between space-y-4 bg-[#11141a]">
            <!-- Top Row: Badge & Type -->
            <div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold ${isPlayer ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'}">
                    ${isPlayer ? `선수 (${client.position || 'FW'})` : '감독 (Manager)'}
                  </span>
                  ${isVirtual ? '<span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">🧪 가상 인물</span>' : '<span class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">⭐ 실제 고객</span>'}
                </div>
                <button onclick="terminateClientContract(${clientId}, '${client.type}', '${nameKo}')"
                  class="text-[10px] text-zinc-500 hover:text-rose-400 px-1.5 py-0.5 rounded hover:bg-zinc-800 transition" title="전속 대리 계약 해지">
                  ✕ 전속해지
                </button>
              </div>

              <!-- Client Header -->
              <div class="flex items-start justify-between gap-3 mt-3">
                <div>
                  <h4 class="text-base font-bold text-white tracking-tight flex items-center gap-1.5">
                    <span>${nameKo}</span>
                    <span class="text-xs font-normal text-zinc-400 font-mono">${nameEn}</span>
                  </h4>
                  <p class="text-xs text-zinc-400 mt-0.5 flex items-center gap-1">
                    <span class="text-zinc-200 font-medium">${currentClub}</span>
                    <span class="text-zinc-600">·</span>
                    <span>${client.league || '글로벌 리그'}</span>
                  </p>
                </div>
                <div class="text-right">
                  <div class="text-xs font-bold text-emerald-400 font-mono">${marketVal}</div>
                  <div class="text-[10px] text-zinc-400 font-mono">${wage}</div>
                </div>
              </div>
            </div>

            <!-- Representation Agreement Status Box -->
            <div class="p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] space-y-1.5 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-zinc-400 text-[11px]">계약 상태 / 만료</span>
                <span class="font-mono text-amber-300 text-[11px] font-semibold">${dDayStr}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-zinc-400 text-[11px]">담당 리드 에이전트</span>
                <span class="text-zinc-200 text-[11px] font-medium">${client.lead_agent_name || '김대표 Agent'}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-zinc-400 text-[11px]">법정 수수료율</span>
                <span class="font-mono text-emerald-400 text-[11px] font-semibold">${client.commission_rate_pct || 5.0}% (FFAR Cap)</span>
              </div>
            </div>

            <!-- Agency Core Business Lifecycle Actions -->
            <div class="space-y-1.5 pt-1">
              ${isFA ? `
                <button onclick="openClientSignClubModal(${clientId}, '${client.type}', '${nameKo}')"
                  class="w-full py-2 px-3 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs transition flex items-center justify-center gap-1.5 shadow-md shadow-amber-950/30">
                  <span>🟡 새 구단 입단 계약 체결 (FA)</span>
                </button>
              ` : `
                <div class="grid grid-cols-2 gap-2">
                  <button onclick="openClientRenewalModal(${clientId}, '${client.type}', '${nameKo}', '${currentClub}', ${client.weekly_wage_eur || 50000})"
                    class="py-2 px-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1 shadow-md shadow-emerald-950/30">
                    <span>🔄 소속팀 재계약</span>
                  </button>
                  <button onclick="openClientTransferModal(${clientId}, '${client.type}', '${nameKo}', '${currentClub}', ${client.market_value_eur || 30000000}, ${client.weekly_wage_eur || 50000})"
                    class="py-2 px-2.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1 shadow-md shadow-sky-950/30">
                    <span>🚀 5대 리그 이적</span>
                  </button>
                </div>
              `}
              <div class="grid grid-cols-2 gap-2 pt-0.5">
                <button onclick="selectClientForStrategy('${nameKo}')"
                  class="px-2 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-medium transition text-center">
                  ⚡ 협상 전략
                </button>
                <button onclick="selectClientForDocs('${nameKo}')"
                  class="px-2 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-medium transition text-center">
                  📄 공식 문서
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function selectClientForStrategy(name) {
      if (typeof selectPlayer === 'function') {
        const found = (allPlayers || []).find(p => (p.name_ko === name || p.name === name));
        if (found) selectPlayer(found);
      }
      showPage('page-strategy');
    }

    function selectClientForDocs(name) {
      if (typeof selectPlayer === 'function') {
        const found = (allPlayers || []).find(p => (p.name_ko === name || p.name === name));
        if (found) selectPlayer(found);
      }
      showPage('page-documents');
    }

    // =========================================================================
    // MODAL HANDLERS FOR RENEWAL, TRANSFER, FA SIGNING & TERMINATION
    // =========================================================================
    function openClientRenewalModal(clientId, clientType, clientName, currentClub, currentWage) {
      const modal = document.getElementById('modal-client-renewal');
      if (!modal) return;

      document.getElementById('renewal-client-id').value = clientId;
      document.getElementById('renewal-client-type').value = clientType;
      document.getElementById('renewal-modal-title').textContent = `[${clientName}] 소속팀 재계약 협상`;
      document.getElementById('renewal-current-club').textContent = currentClub;
      document.getElementById('renewal-current-wage').textContent = `€${Math.round((currentWage || 50000)/1000)}K / 주`;
      document.getElementById('renewal-wage-input').value = Math.round((currentWage || 50000) * 1.2);

      modal.classList.remove('hidden');
    }

    function closeClientRenewalModal() {
      const modal = document.getElementById('modal-client-renewal');
      if (modal) modal.classList.add('hidden');
    }

    async function submitClientRenewal(e) {
      e.preventDefault();
      const clientId = parseInt(document.getElementById('renewal-client-id').value, 10);
      const clientType = document.getElementById('renewal-client-type').value;
      const newWage = parseFloat(document.getElementById('renewal-wage-input').value);
      const years = parseInt(document.getElementById('renewal-years-select').value, 10);
      const buyout = parseFloat(document.getElementById('renewal-buyout-input').value) || null;
      const bonus = parseFloat(document.getElementById('renewal-bonus-input').value) || null;

      try {
        const res = await fetch('/api/agency/client/renew', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            new_weekly_wage_eur: newWage,
            contract_years: years,
            new_buyout_eur: buyout,
            signing_bonus_eur: bonus
          })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('재계약 체결 실패: ' + (data.detail || '오류'));
          return;
        }

        alert(data.message || '재계약이 성공적으로 체결되었습니다!');
        closeClientRenewalModal();
        loadAgencyPortfolio();
      } catch (err) {
        alert('재계약 통신 오류: ' + err.message);
      }
    }

    function openClientTransferModal(clientId, clientType, clientName, currentClub, currentVal, currentWage) {
      const modal = document.getElementById('modal-client-transfer');
      if (!modal) return;

      document.getElementById('transfer-client-id').value = clientId;
      document.getElementById('transfer-client-type').value = clientType;
      document.getElementById('transfer-modal-title').textContent = `[${clientName}] 구단 이적 협상`;
      document.getElementById('transfer-current-club').textContent = currentClub;
      document.getElementById('transfer-current-val').textContent = `€${((currentVal || 30000000)/1000000).toFixed(1)}M`;
      document.getElementById('transfer-fee-input').value = Math.round((currentVal || 30000000) * 1.1);
      document.getElementById('transfer-wage-input').value = Math.round((currentWage || 60000) * 1.3);

      modal.classList.remove('hidden');
    }

    function closeClientTransferModal() {
      const modal = document.getElementById('modal-client-transfer');
      if (modal) modal.classList.add('hidden');
    }

    async function submitClientTransfer(e) {
      e.preventDefault();
      const clientId = parseInt(document.getElementById('transfer-client-id').value, 10);
      const clientType = document.getElementById('transfer-client-type').value;
      const club = document.getElementById('transfer-club-input').value.trim();
      const league = document.getElementById('transfer-league-select').value;
      const fee = parseFloat(document.getElementById('transfer-fee-input').value);
      const wage = parseFloat(document.getElementById('transfer-wage-input').value);
      const years = parseInt(document.getElementById('transfer-years-select').value, 10);

      try {
        const res = await fetch('/api/agency/client/transfer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            destination_club: club,
            destination_league: league,
            transfer_fee_eur: fee,
            new_weekly_wage_eur: wage,
            contract_years: years
          })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('이적 협상 실패: ' + (data.detail || '오류'));
          return;
        }

        alert(data.message || '이적이 성공적으로 완료되었습니다!');
        closeClientTransferModal();
        loadAgencyPortfolio();
      } catch (err) {
        alert('이적 통신 오류: ' + err.message);
      }
    }

    function openClientSignClubModal(clientId, clientType, clientName) {
      const modal = document.getElementById('modal-client-sign-club');
      if (!modal) return;

      document.getElementById('fa-client-id').value = clientId;
      document.getElementById('fa-client-type').value = clientType;
      document.getElementById('sign-club-modal-title').textContent = `[${clientName}] 새 구단 입단 계약 (FA)`;
      document.getElementById('fa-wage-input').value = 45000;

      modal.classList.remove('hidden');
    }

    function closeClientSignClubModal() {
      const modal = document.getElementById('modal-client-sign-club');
      if (modal) modal.classList.add('hidden');
    }

    async function submitClientSignClub(e) {
      e.preventDefault();
      const clientId = parseInt(document.getElementById('fa-client-id').value, 10);
      const clientType = document.getElementById('fa-client-type').value;
      const club = document.getElementById('fa-club-input').value.trim();
      const league = document.getElementById('fa-league-select').value;
      const wage = parseFloat(document.getElementById('fa-wage-input').value);
      const years = parseInt(document.getElementById('fa-years-select').value, 10);

      try {
        const res = await fetch('/api/agency/client/sign-club', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            destination_club: club,
            destination_league: league,
            weekly_wage_eur: wage,
            contract_years: years
          })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('입단 계약 실패: ' + (data.detail || '오류'));
          return;
        }

        alert(data.message || '입단 계약이 체결되었습니다!');
        closeClientSignClubModal();
        loadAgencyPortfolio();
      } catch (err) {
        alert('입단 계약 통신 오류: ' + err.message);
      }
    }

    async function terminateClientContract(clientId, clientType, clientName) {
      const reason = prompt(`[${clientName}] 전속 계약을 해지하시겠습니까?
해지 사유를 입력해주세요 (예: 선수 요청, 계약 만료, 상호 합의):`, '상호 합의 계약 해지');
      if (!reason) return;

      try {
        const res = await fetch('/api/agency/terminate-contract', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            reason: reason
          })
        });
        const data = await res.json();

        if (!res.ok) {
          alert('계약 해지 실패: ' + (data.detail || '오류'));
          return;
        }

        alert(data.message || `'${clientName}' 전속 계약이 해지되었으며, 영입 관심 풀로 복귀되었습니다.`);
        loadAgencyPortfolio();
        loadAgencyRecruitmentTargets();
      } catch (err) {
        alert('계약 해지 통신 오류: ' + err.message);
      }
    }


    window.addEventListener('DOMContentLoaded', initDashboard);
  