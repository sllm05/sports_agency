import re

def update_index_html():
    with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Header Navigation
    nav_old = '''        <button id="nav-btn-recruitment" onclick="showPage('page-recruitment')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span>신규 영입</span>
        </button>
        <button id="nav-btn-scouting" onclick="showPage('page-scouting')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span>스카우팅</span>
        </button>'''

    nav_new = '''        <button id="nav-btn-scouting" onclick="showPage('page-scouting')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>스카우팅 & 영입</span>
        </button>'''

    if nav_old in html:
        html = html.replace(nav_old, nav_new, 1)
        print("1. Header Nav replaced successfully")
    else:
        print("1. ERROR: Header Nav pattern not found")

    # 2. Extract content of existing page-recruitment
    rec_pattern = re.compile(r'(<!-- =+ -->\s*<!-- PAGE: RECRUITMENT TARGETS.*?-->\s*<div id="page-recruitment".*?</div>\s*</div>)', re.DOTALL)
    rec_match = rec_pattern.search(html)
    if not rec_match:
        print("2. ERROR: page-recruitment block not found")
        return
    
    rec_block = rec_match.group(1)
    # Remove the page-recruitment block from its current location
    html = html.replace(rec_block, "<!-- [Merged into page-scouting sub-tab 1] -->", 1)
    print("2. Extracted and removed original page-recruitment block")

    # Extract the inner contents of page-recruitment to put into subtab-virtual
    inner_rec_match = re.search(r'<div id="page-recruitment"[^>]*>(.*?)</div>\s*$', rec_block, re.DOTALL)
    if inner_rec_match:
        inner_rec_content = inner_rec_match.group(1).strip()
    else:
        # fallback
        inner_rec_content = rec_block

    # 3. Restructure page-scouting
    scout_start_old = '''    <!-- ======================================================================= -->
    <!-- PAGE 2: SCOUTING & PROSPECT DESK -->
    <!-- ======================================================================= -->
    <div id="page-scouting" class="page-view hidden space-y-5">

      <!-- Breadcrumb Header -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.06] pb-3">
        <div class="flex items-center gap-3">
          <button onclick="showPage('page-home')"
            class="px-2.5 py-1 rounded-lg bg-[#12151c] hover:bg-zinc-800 border border-white/[0.08] text-xs font-medium text-zinc-300 transition">
            ← 대시보드
          </button>
          <div>
            <h2 class="text-base font-bold text-white">선수 스카우팅 및 분석</h2>
            <p class="text-xs text-zinc-400">2,758명 선수·감독 로스터 검색 및 데이터 분석</p>
          </div>
        </div>

        <button onclick="showPage('page-strategy')"
          class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition">
          선택한 선수로 협상 전략 수립 →
        </button>
      </div>

      <!-- Main Scouting Workspace Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">'''

    scout_start_new = f'''    <!-- ======================================================================= -->
    <!-- PAGE 2: SCOUTING & RECRUITMENT DESK (통합 스카우팅 & 영입 센터) -->
    <!-- ======================================================================= -->
    <div id="page-scouting" class="page-view hidden space-y-5">

      <!-- Breadcrumb Header -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.06] pb-3">
        <div class="flex items-center gap-3">
          <button onclick="showPage('page-home')"
            class="px-2.5 py-1 rounded-lg bg-[#12151c] hover:bg-zinc-800 border border-white/[0.08] text-xs font-medium text-zinc-300 transition">
            ← 대시보드
          </button>
          <div>
            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <span>스카우팅 & 영입 센터</span>
              <span class="text-xs font-normal text-zinc-400 font-mono">(Talent Scouting & Acquisition Radar)</span>
            </h2>
            <p class="text-xs text-zinc-400">가상 인물 영입 테스트 풀 및 글로벌 5대 리그 스카우팅 통합 레이더</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="showPage('page-portfolio')"
            class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>소속 고객 관리실 보기</span>
          </button>
          <button onclick="showPage('page-strategy')"
            class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition">
            협상 전략실 바로가기 →
          </button>
        </div>
      </div>

      <!-- Sub-Tab Switcher: Virtual Test Pool vs Real Big 5 DB -->
      <div class="flex flex-wrap items-center justify-between gap-3 bg-[#11141a] p-2 rounded-xl border border-white/[0.08]">
        <div class="flex items-center gap-2">
          <button id="scouting-tab-virtual-btn" onclick="switchScoutingSubTab('virtual')"
            class="px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-emerald-600 text-white shadow-md shadow-emerald-950/30">
            <span>🧪 가상 인물 영입 테스트 풀 (선수 10인 · 감독 3인)</span>
            <span class="px-1.5 py-0.5 rounded text-[10px] bg-white/20">신규 에이전시 테스트</span>
          </button>
          <button id="scouting-tab-real-btn" onclick="switchScoutingSubTab('real')"
            class="px-3.5 py-2 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition flex items-center gap-2">
            <span>🌍 글로벌 5대 리그 스카우팅 DB (2,758명 · 96개 구단)</span>
            <span class="px-1.5 py-0.5 rounded text-[10px] bg-zinc-800 text-zinc-400 border border-white/[0.04]">실존 벤치마크</span>
          </button>
        </div>
        <div class="text-[11px] text-zinc-400 hidden md:block">
          <span id="scouting-tab-desc" class="text-zinc-300">신규 에이전시 테스트 전용: 가상 선수·감독 전속 계약 유치</span>
        </div>
      </div>

      <!-- SUB-TAB 1: VIRTUAL RECRUITMENT TARGETS TEST POOL -->
      <div id="scouting-subtab-virtual" class="space-y-5">
{inner_rec_content}
      </div>

      <!-- SUB-TAB 2: GLOBAL BIG 5 LEAGUES OBJECTIVE SCOUTING DB -->
      <div id="scouting-subtab-real" class="space-y-5 hidden">
        <!-- Main Scouting Workspace Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">'''

    if scout_start_old in html:
        html = html.replace(scout_start_old, scout_start_new, 1)
        print("3. Restructured page-scouting with Sub-tabs successfully")
    else:
        print("3. ERROR: scout_start_old not found")

    # Close scouting-subtab-real before closing page-scouting
    scout_end_old = '''          <div class="flex justify-end pt-1">
            <button onclick="registerCustomClient()"
              class="py-1.5 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition">
              선수 등록 및 선택
            </button>
          </div>
        </div>
      </div>

    </div>'''

    scout_end_new = '''          <div class="flex justify-end pt-1">
            <button onclick="registerCustomClient()"
              class="py-1.5 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition">
              선수 등록 및 선택
            </button>
          </div>
        </div>
      </div>

      </div> <!-- End of scouting-subtab-real -->

    </div>'''

    if scout_end_old in html:
        html = html.replace(scout_end_old, scout_end_new, 1)
        print("4. Closed scouting-subtab-real successfully")
    else:
        print("4. ERROR: scout_end_old not found")

    # 5. Routing controller update in showPage / updateNavState
    showpage_old = '''    function showPage(pageId) {
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

      // Lazy load page-specific data
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
        { id: 'nav-btn-admin', key: 'admin' },
      ];'''

    showpage_new = '''    let currentScoutingSubTab = 'virtual';

    function switchScoutingSubTab(tab) {
      currentScoutingSubTab = tab;
      const virtualTab = document.getElementById('scouting-subtab-virtual');
      const realTab = document.getElementById('scouting-subtab-real');
      const virtualBtn = document.getElementById('scouting-tab-virtual-btn');
      const realBtn = document.getElementById('scouting-tab-real-btn');
      const descEl = document.getElementById('scouting-tab-desc');

      if (tab === 'virtual') {
        if (virtualTab) virtualTab.classList.remove('hidden');
        if (realTab) realTab.classList.add('hidden');
        if (virtualBtn) {
          virtualBtn.className = 'px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-emerald-600 text-white shadow-md shadow-emerald-950/30';
        }
        if (realBtn) {
          realBtn.className = 'px-3.5 py-2 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition flex items-center gap-2';
        }
        if (descEl) descEl.textContent = '신규 에이전시 테스트 전용: 가상 선수·감독 전속 계약 유치';
        loadAgencyRecruitmentTargets();
      } else {
        if (virtualTab) virtualTab.classList.add('hidden');
        if (realTab) realTab.classList.remove('hidden');
        if (virtualBtn) {
          virtualBtn.className = 'px-3.5 py-2 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition flex items-center gap-2';
        }
        if (realBtn) {
          realBtn.className = 'px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-sky-600 text-white shadow-md shadow-sky-950/30';
        }
        if (descEl) descEl.textContent = '글로벌 5대 리그 실존 데이터베이스: 2,758명 선수·감독 로스터 및 스탯 분석';
        if (selectedPlayer) updateRadarChart(selectedPlayer);
      }
    }

    function showPage(pageId) {
      if (pageId === 'page-recruitment') {
        showPage('page-scouting');
        switchScoutingSubTab('virtual');
        return;
      }

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

      // Lazy load page-specific data
      if (pageId === 'page-portfolio') loadAgencyPortfolio();
      if (pageId === 'page-scouting') {
        loadAgencyRecruitmentTargets();
        if (currentScoutingSubTab === 'real' && selectedPlayer) {
          updateRadarChart(selectedPlayer);
        }
      }
      if (pageId === 'page-admin') loadAdminDashboard();

      if (pageId === 'page-tactics') {
        initTacticsDesk();
      } else if (pageId === 'page-documents' && currentWorkflowState) {
        switchDocTab(activeDocTab || 'career');
      } else if (pageId === 'page-finance') {
        runStandalonePsrCalc();
      }

      window.location.hash = pageId.replace('page-', '');
    }

    function updateNavState(pageId) {
      let navKey = pageId.replace('page-', '');
      if (navKey === 'recruitment') navKey = 'scouting';
      const buttons = [
        { id: 'nav-btn-home', key: 'home' },
        { id: 'nav-btn-portfolio', key: 'portfolio' },
        { id: 'nav-btn-scouting', key: 'scouting' },
        { id: 'nav-btn-strategy', key: 'strategy' },
        { id: 'nav-btn-tactics', key: 'tactics' },
        { id: 'nav-btn-documents', key: 'documents' },
        { id: 'nav-btn-finance', key: 'finance' },
        { id: 'nav-btn-regulations', key: 'regulations' },
        { id: 'nav-btn-admin', key: 'admin' },
      ];'''

    if showpage_old in html:
        html = html.replace(showpage_old, showpage_new, 1)
        print("5. showPage and switchScoutingSubTab updated successfully")
    else:
        print("5. ERROR: showpage_old not found")

    # 6. Update Portfolio Action Buttons in renderPortfolioCards()
    port_actions_old = '''            <!-- Quick Action Buttons -->
            <div class="grid grid-cols-4 gap-1.5 pt-1">
              <button onclick="selectClientForStrategy('${nameKo}')"
                class="px-1.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-[11px] font-medium transition text-center"
                title="이적 및 계약 협상 전략실 이동">
                ⚡ 협상
              </button>
              <button onclick="selectClientForDocs('${nameKo}')"
                class="px-1.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-[11px] font-medium transition text-center"
                title="공식 실무 문서 센터 발급">
                📄 공문
              </button>
              <button onclick="selectClientForTactics('${nameKo}')"
                class="px-1.5 py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white text-[11px] font-semibold transition text-center"
                title="전술 하이라이트 및 시뮬레이션">
                🎯 전술
              </button>
              <button onclick="terminateClientContract(${client.client_id}, '${client.type}', '${nameKo}')"
                class="px-1.5 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/25 text-rose-400 hover:text-rose-300 border border-rose-500/20 text-[11px] font-medium transition text-center"
                title="전속 계약 해지 (영입 대상 리스트로 반환)">
                ✕ 해지
              </button>
            </div>'''

    port_actions_new = '''            <!-- Client Actions (Renewal / Transfer / Sign Club / Release) -->
            <div class="space-y-1.5 pt-1 border-t border-white/[0.04]">
              ${isUnemployed ? `
                <button onclick="openClientSignClubModal(${client.client_id}, '${client.type}', '${nameKo}')"
                  class="w-full py-2 px-3 rounded-lg bg-amber-500 hover:bg-amber-400 text-black text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-md shadow-amber-950/20">
                  <span>🟡 새 구단 입단 계약 교섭 (FA)</span>
                </button>
              ` : `
                <div class="grid grid-cols-2 gap-1.5">
                  <button onclick="openClientRenewalModal(${client.client_id}, '${client.type}', '${nameKo}', '${client.current_club || ''}', ${client.weekly_wage_eur || 50000})"
                    class="py-1.5 px-2 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/30 text-xs font-bold transition flex items-center justify-center gap-1"
                    title="소속팀과의 재계약 및 주급 인상 협상">
                    <span>🔄 소속팀 재계약</span>
                  </button>
                  <button onclick="openClientTransferModal(${client.client_id}, '${client.type}', '${nameKo}', '${client.current_club || ''}', ${client.weekly_wage_eur || 50000}, ${client.market_value_eur || 20000000})"
                    class="py-1.5 px-2 rounded-lg bg-sky-600/20 hover:bg-sky-600 text-sky-300 hover:text-white border border-sky-500/30 text-xs font-bold transition flex items-center justify-center gap-1"
                    title="유럽 5대 리그 또는 상위 구단으로의 이적 타진">
                    <span>🚀 5대 리그 이적</span>
                  </button>
                </div>
              `}
              
              <div class="grid grid-cols-3 gap-1.5 pt-0.5">
                <button onclick="selectClientForStrategy('${nameKo}')"
                  class="py-1 px-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-medium transition text-center"
                  title="이적 및 계약 협상 전략실로 이동">
                  ⚡ 협상전략
                </button>
                <button onclick="selectClientForDocs('${nameKo}')"
                  class="py-1 px-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-medium transition text-center"
                  title="공식 실무 공문서 생성">
                  📄 실무문서
                </button>
                <button onclick="terminateClientContract(${client.client_id}, '${client.type}', '${nameKo}')"
                  class="py-1 px-1 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 hover:text-rose-300 border border-rose-500/20 text-[11px] font-medium transition text-center"
                  title="전속 계약 해지 (영입 테스트 풀로 반환)">
                  ✕ 전속해지
                </button>
              </div>
            </div>'''

    if port_actions_old in html:
        html = html.replace(port_actions_old, port_actions_new, 1)
        print("6. Portfolio Actions updated successfully")
    else:
        print("6. ERROR: port_actions_old not found")

    # 7. Add Renewal, Transfer, Sign Club Modals before modal-pitch-viewer
    modals_code = '''  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT CONTRACT RENEWAL (소속팀 재계약 협상) -->
  <!-- ========================================================================= -->
  <div id="modal-client-renewal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
    <div class="ui-card w-full max-w-lg border-emerald-500/30 bg-[#11141a] shadow-2xl p-6 rounded-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-white/[0.08] pb-3">
        <div class="flex items-center gap-2">
          <span class="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 text-lg">🔄</span>
          <div>
            <h3 class="text-base font-bold text-white tracking-tight">소속팀 재계약 및 조건 개선 협상</h3>
            <p id="renewal-modal-subtitle" class="text-xs text-zinc-400">선수·소속팀 간 계약 연장 및 주급 인상 협상 데스크</p>
          </div>
        </div>
        <button onclick="closeModal('modal-client-renewal')" class="text-zinc-400 hover:text-white p-1 text-xl leading-none">&times;</button>
      </div>

      <input type="hidden" id="renewal-client-id" />
      <input type="hidden" id="renewal-client-type" />

      <div class="space-y-3.5 text-xs">
        <div class="p-3 rounded-xl bg-[#0e1117] border border-white/[0.06] flex items-center justify-between">
          <div>
            <span class="text-zinc-400">협상 대상 고객</span>
            <div id="renewal-client-name" class="text-sm font-bold text-white mt-0.5">-</div>
          </div>
          <div class="text-right">
            <span class="text-zinc-400">현재 소속팀</span>
            <div id="renewal-client-club" class="text-sm font-bold text-emerald-400 mt-0.5">-</div>
          </div>
        </div>

        <div>
          <label class="block text-zinc-300 font-semibold mb-1">인상 제안 주급 (Weekly Wage, EUR)</label>
          <div class="flex items-center gap-2">
            <input type="number" id="renewal-wage-input" class="flex-1 bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-emerald-500" placeholder="100000" />
            <span class="text-zinc-400 font-mono">EUR / 주</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">연장 계약 기간</label>
            <select id="renewal-years-select" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-2.5 py-2 text-white text-xs focus:outline-none focus:border-emerald-500">
              <option value="1">+1년 연장 (단기)</option>
              <option value="2">+2년 연장 (표준)</option>
              <option value="3" selected>+3년 연장 (중장기 코어)</option>
              <option value="4">+4년 연장 (장기 프랜차이즈)</option>
              <option value="5">+5년 연장 (최대 장기 계약)</option>
            </select>
          </div>
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">신설 바이아웃 (EUR, 선택)</label>
            <input type="number" id="renewal-buyout-input" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-emerald-500" placeholder="예: 30000000" />
          </div>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/[0.08]">
        <button onclick="closeModal('modal-client-renewal')" class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
          취소
        </button>
        <button onclick="submitClientRenewal()" id="btn-submit-renewal" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition shadow-md shadow-emerald-950/30 flex items-center gap-1.5">
          <span>✍️ 재계약 공식 합의 체결</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT CLUB TRANSFER (타 구단 / 5대 리그 이적) -->
  <!-- ========================================================================= -->
  <div id="modal-client-transfer" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
    <div class="ui-card w-full max-w-lg border-sky-500/30 bg-[#11141a] shadow-2xl p-6 rounded-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-white/[0.08] pb-3">
        <div class="flex items-center gap-2">
          <span class="p-1.5 rounded-lg bg-sky-500/20 text-sky-400 text-lg">🚀</span>
          <div>
            <h3 class="text-base font-bold text-white tracking-tight">상위 리그 / 타 구단 이적 타진 협상</h3>
            <p class="text-xs text-zinc-400">유럽 5대 리그 및 빅클럽 스텝업 이적 교섭 데스크</p>
          </div>
        </div>
        <button onclick="closeModal('modal-client-transfer')" class="text-zinc-400 hover:text-white p-1 text-xl leading-none">&times;</button>
      </div>

      <input type="hidden" id="transfer-client-id" />
      <input type="hidden" id="transfer-client-type" />

      <div class="space-y-3.5 text-xs">
        <div class="p-3 rounded-xl bg-[#0e1117] border border-white/[0.06] flex items-center justify-between">
          <div>
            <span class="text-zinc-400">이적 대상 고객</span>
            <div id="transfer-client-name" class="text-sm font-bold text-white mt-0.5">-</div>
          </div>
          <div class="text-right">
            <span class="text-zinc-400">현재 원소속팀</span>
            <div id="transfer-client-prev-club" class="text-sm font-bold text-zinc-300 mt-0.5">-</div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">이적 대상 리그</label>
            <select id="transfer-league-select" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-2.5 py-2 text-white text-xs focus:outline-none focus:border-sky-500">
              <option value="Premier League" selected>Premier League (잉글랜드)</option>
              <option value="La Liga">La Liga (스페인)</option>
              <option value="Bundesliga">Bundesliga (독일)</option>
              <option value="Serie A">Serie A (이탈리아)</option>
              <option value="Ligue 1">Ligue 1 (프랑스)</option>
              <option value="가상 슈퍼리그">가상 슈퍼리그 (Virtual Tier 1)</option>
            </select>
          </div>
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">행선지 구단명</label>
            <input type="text" id="transfer-club-input" list="transfer-club-datalist" value="토트넘 홋스퍼 FC" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white text-xs focus:outline-none focus:border-sky-500" placeholder="예: 토트넘 홋스퍼 FC" />
            <datalist id="transfer-club-datalist">
              <option value="토트넘 홋스퍼 FC"></option>
              <option value="아스널 FC"></option>
              <option value="맨체스터 시티 FC"></option>
              <option value="레알 마드리드"></option>
              <option value="FC 바르셀로나"></option>
              <option value="바이에른 뮌헨"></option>
              <option value="보루시아 도르트문트"></option>
              <option value="파리 생제르맹 FC"></option>
              <option value="유벤투스 FC"></option>
              <option value="FC 메트로폴리스"></option>
              <option value="발할라 FC"></option>
            </datalist>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">합의 이적료 (Transfer Fee, EUR)</label>
            <input type="number" id="transfer-fee-input" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-sky-500" placeholder="35000000" />
          </div>
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">신규 합의 주급 (EUR / 주)</label>
            <input type="number" id="transfer-wage-input" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-sky-500" placeholder="150000" />
          </div>
        </div>

        <div>
          <label class="block text-zinc-300 font-semibold mb-1">신규 계약 기간</label>
          <select id="transfer-years-select" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-2.5 py-2 text-white text-xs focus:outline-none focus:border-sky-500">
            <option value="3">3년 계약</option>
            <option value="4" selected>4년 계약 (장기 스텝업 권장)</option>
            <option value="5">5년 계약 (빅클럽 표준)</option>
          </select>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/[0.08]">
        <button onclick="closeModal('modal-client-transfer')" class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
          취소
        </button>
        <button onclick="submitClientTransfer()" id="btn-submit-transfer" class="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs transition shadow-md shadow-sky-950/30 flex items-center gap-1.5">
          <span>🚀 공식 이적 계약 타결 및 등록</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT SIGN CLUB (무직/FA 신규 구단 입단 계약) -->
  <!-- ========================================================================= -->
  <div id="modal-client-sign-club" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
    <div class="ui-card w-full max-w-lg border-amber-500/30 bg-[#11141a] shadow-2xl p-6 rounded-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-white/[0.08] pb-3">
        <div class="flex items-center gap-2">
          <span class="p-1.5 rounded-lg bg-amber-500/20 text-amber-400 text-lg">🟡</span>
          <div>
            <h3 class="text-base font-bold text-white tracking-tight">자유계약(FA) 신규 구단 공식 입단</h3>
            <p class="text-xs text-zinc-400">무직 상태 고객의 신규 구단 입단 계약 협상 및 전속 지원</p>
          </div>
        </div>
        <button onclick="closeModal('modal-client-sign-club')" class="text-zinc-400 hover:text-white p-1 text-xl leading-none">&times;</button>
      </div>

      <input type="hidden" id="signclub-client-id" />
      <input type="hidden" id="signclub-client-type" />

      <div class="space-y-3.5 text-xs">
        <div class="p-3 rounded-xl bg-[#0e1117] border border-white/[0.06] flex items-center justify-between">
          <div>
            <span class="text-zinc-400">입단 대상 고객</span>
            <div id="signclub-client-name" class="text-sm font-bold text-white mt-0.5">-</div>
          </div>
          <div class="text-right">
            <span class="text-zinc-400">현재 상태</span>
            <div class="text-xs font-bold text-amber-300 mt-0.5 px-2 py-0.5 bg-amber-500/10 border border-amber-500/20 rounded">무직 (FA 자유계약)</div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">입단 대상 구단</label>
            <select id="signclub-club-select" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-2.5 py-2 text-white text-xs focus:outline-none focus:border-amber-500">
              <option value="FC 메트로폴리스">FC 메트로폴리스 (가상 리그 강호)</option>
              <option value="발할라 FC">발할라 FC (가상 북유럽 리그)</option>
              <option value="아틀란티스 SC">아틀란티스 SC (가상 남부 리그)</option>
              <option value="네오 도쿄 FC">네오 도쿄 FC (가상 아시아 리그)</option>
              <option value="스타라이트 로버스">스타라이트 로버스 (가상 리그)</option>
            </select>
          </div>
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">소속 리그</label>
            <input type="text" id="signclub-league-input" value="가상 슈퍼리그" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white text-xs focus:outline-none focus:border-amber-500" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">합의 주급 (Weekly Wage, EUR)</label>
            <input type="number" id="signclub-wage-input" value="80000" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-amber-500" />
          </div>
          <div>
            <label class="block text-zinc-300 font-semibold mb-1">계약 기간</label>
            <select id="signclub-years-select" class="w-full bg-[#0e1117] border border-white/[0.1] rounded-lg px-2.5 py-2 text-white text-xs focus:outline-none focus:border-amber-500">
              <option value="1">1년 단기 계약</option>
              <option value="2" selected>2년 표준 계약</option>
              <option value="3">3년 장기 계약</option>
            </select>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-white/[0.08]">
        <button onclick="closeModal('modal-client-sign-club')" class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
          취소
        </button>
        <button onclick="submitClientSignClub()" id="btn-submit-signclub" class="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs transition shadow-md shadow-amber-950/30 flex items-center gap-1.5">
          <span>✍️ 공식 입단 계약 체결 확정</span>
        </button>
      </div>
    </div>
  </div>\n\n'''

    modal_target = '  <!-- ========================================================================= -->\n  <!-- MODAL: RECRUITMENT PITCH DECK VIEWER -->'
    if modal_target in html:
        html = html.replace(modal_target, modals_code + modal_target, 1)
        print("7. Added Renewal, Transfer, Sign Club Modals successfully")
    else:
        print("7. ERROR: modal_target not found")

    # 8. Add JavaScript Functions for the Modals
    js_funcs = '''
    // -------------------------------------------------------------------------
    // Portfolio Client Negotiation Desk (Renewal, Transfer, FA Sign Club)
    // -------------------------------------------------------------------------
    function closeModal(modalId) {
      const el = document.getElementById(modalId);
      if (el) el.classList.add('hidden');
    }

    function openClientRenewalModal(clientId, clientType, clientName, currentClub, currentWage) {
      document.getElementById('renewal-client-id').value = clientId;
      document.getElementById('renewal-client-type').value = clientType;
      document.getElementById('renewal-client-name').textContent = clientName;
      document.getElementById('renewal-client-club').textContent = currentClub || '가상팀';
      
      const suggestedWage = Math.round((currentWage || 50000) * 1.35);
      document.getElementById('renewal-wage-input').value = suggestedWage;
      document.getElementById('renewal-years-select').value = '3';
      document.getElementById('renewal-buyout-input').value = '';
      
      const modal = document.getElementById('modal-client-renewal');
      if (modal) modal.classList.remove('hidden');
    }

    async function submitClientRenewal() {
      const clientId = parseInt(document.getElementById('renewal-client-id').value);
      const clientType = document.getElementById('renewal-client-type').value;
      const clientName = document.getElementById('renewal-client-name').textContent;
      const newWage = parseInt(document.getElementById('renewal-wage-input').value) || 100000;
      const years = parseInt(document.getElementById('renewal-years-select').value) || 3;
      const buyoutVal = document.getElementById('renewal-buyout-input').value;
      const buyout = buyoutVal ? parseInt(buyoutVal) : null;
      
      const btn = document.getElementById('btn-submit-renewal');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳ 재계약 협상 및 서명 중...</span>';
      }

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
            signing_bonus_eur: 0
          })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '재계약 처리 중 오류가 발생했습니다.');

        alert(`🎉 [재계약 합의 성공]\\n${data.message}`);
        closeModal('modal-client-renewal');
        await loadAgencyPortfolio();
      } catch (err) {
        alert('❌ 재계약 실패: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<span>✍️ 재계약 공식 합의 체결</span>';
        }
      }
    }

    function openClientTransferModal(clientId, clientType, clientName, currentClub, currentWage, marketVal) {
      document.getElementById('transfer-client-id').value = clientId;
      document.getElementById('transfer-client-type').value = clientType;
      document.getElementById('transfer-client-name').textContent = clientName;
      document.getElementById('transfer-client-prev-club').textContent = currentClub || '원소속팀';
      
      const fee = marketVal > 0 ? Math.round(marketVal * 1.15) : 30000000;
      const wage = Math.round((currentWage || 50000) * 1.5);
      
      document.getElementById('transfer-fee-input').value = fee;
      document.getElementById('transfer-wage-input').value = wage;
      document.getElementById('transfer-years-select').value = '4';
      
      const modal = document.getElementById('modal-client-transfer');
      if (modal) modal.classList.remove('hidden');
    }

    async function submitClientTransfer() {
      const clientId = parseInt(document.getElementById('transfer-client-id').value);
      const clientType = document.getElementById('transfer-client-type').value;
      const destClub = document.getElementById('transfer-club-input').value.trim() || '토트넘 홋스퍼 FC';
      const destLeague = document.getElementById('transfer-league-select').value;
      const fee = parseInt(document.getElementById('transfer-fee-input').value) || 30000000;
      const wage = parseInt(document.getElementById('transfer-wage-input').value) || 120000;
      const years = parseInt(document.getElementById('transfer-years-select').value) || 4;

      const btn = document.getElementById('btn-submit-transfer');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳ 구단 간 이적 협상 및 메디컬 테스트 중...</span>';
      }

      try {
        const res = await fetch('/api/agency/client/transfer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            destination_club: destClub,
            destination_league: destLeague,
            transfer_fee_eur: fee,
            new_weekly_wage_eur: wage,
            contract_years: years
          })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '이적 처리 중 오류가 발생했습니다.');

        alert(`🚀 [이적 계약 공식 타결]\\n${data.message}`);
        closeModal('modal-client-transfer');
        await loadAgencyPortfolio();
      } catch (err) {
        alert('❌ 이적 협상 실패: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<span>🚀 공식 이적 계약 타결 및 등록</span>';
        }
      }
    }

    function openClientSignClubModal(clientId, clientType, clientName) {
      document.getElementById('signclub-client-id').value = clientId;
      document.getElementById('signclub-client-type').value = clientType;
      document.getElementById('signclub-client-name').textContent = clientName;
      document.getElementById('signclub-wage-input').value = '80000';
      document.getElementById('signclub-years-select').value = '2';

      const modal = document.getElementById('modal-client-sign-club');
      if (modal) modal.classList.remove('hidden');
    }

    async function submitClientSignClub() {
      const clientId = parseInt(document.getElementById('signclub-client-id').value);
      const clientType = document.getElementById('signclub-client-type').value;
      const destClub = document.getElementById('signclub-club-select').value;
      const destLeague = document.getElementById('signclub-league-input').value.trim() || '가상 슈퍼리그';
      const wage = parseInt(document.getElementById('signclub-wage-input').value) || 80000;
      const years = parseInt(document.getElementById('signclub-years-select').value) || 2;

      const btn = document.getElementById('btn-submit-signclub');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span>⏳ 구단 공식 입단 계약서 서명 중...</span>';
      }

      try {
        const res = await fetch('/api/agency/client/sign-club', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            client_id: clientId,
            client_type: clientType,
            destination_club: destClub,
            destination_league: destLeague,
            weekly_wage_eur: wage,
            contract_years: years
          })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || '입단 계약 처리 중 오류가 발생했습니다.');

        alert(`🎉 [공식 입단 축하]\\n${data.message}`);
        closeModal('modal-client-sign-club');
        await loadAgencyPortfolio();
      } catch (err) {
        alert('❌ 입단 계약 실패: ' + err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<span>✍️ 공식 입단 계약 체결 확정</span>';
        }
      }
    }
'''

    js_target = '    async function loadAgencyPortfolio() {'
    if js_target in html:
        html = html.replace(js_target, js_funcs + '\n' + js_target, 1)
        print("8. Added JavaScript Modal action functions successfully")
    else:
        print("8. ERROR: js_target not found")

    with open("src/sports_agency/api/static/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("ALL UPDATES APPLIED TO index.html!")

if __name__ == '__main__':
    update_index_html()
