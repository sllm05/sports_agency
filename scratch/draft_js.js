
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
