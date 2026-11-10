import re
from pathlib import Path

# ==============================================================================
# 1. HTML Views (page-portfolio, page-recruitment, page-admin)
# ==============================================================================

HTML_PORTFOLIO = """
    <!-- ======================================================================= -->
    <!-- PAGE: AGENCY PORTFOLIO (소속 선수 및 감독 포트폴리오) -->
    <!-- ======================================================================= -->
    <div id="page-portfolio" class="page-view hidden space-y-6">

      <!-- Header & FIFA FFAR Compliance Banner -->
      <div class="ui-card p-6 border-white/[0.08] relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-72 h-72 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                FIFA Football Agent #FIFA-2024-KOR-8821
              </span>
              <span class="text-xs text-zinc-400">FFAR 규정 24개월 전속 대리 계약 및 이적·재계약 라이프사이클 관리</span>
            </div>
            <h2 class="text-2xl font-bold text-white tracking-tight mt-1.5 flex items-center gap-2">
              <span>Antigravity Sports 포트폴리오</span>
              <span class="text-xs font-normal text-zinc-400 font-mono">(Active Roster)</span>
            </h2>
            <p class="text-xs text-zinc-400 mt-1">
              에이전시와 전속 계약 체결된 고객들의 구단 재계약, 5대 리그 이적, 무소속(FA) 입단 및 전속 해지를 원클릭으로 실행합니다.
            </p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="showPage('page-recruitment')"
              class="px-3.5 py-2 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-semibold transition flex items-center gap-1.5 border border-amber-500/30 shadow-lg shadow-amber-950/20">
              <span>⭐ 영입 관심 리스트 (Watchlist) 보기</span>
              <span id="portfolio-header-rec-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-500/30 text-amber-200 font-mono">13</span>
            </button>
          </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 pt-5 mt-5 border-t border-white/[0.06]">
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.04]">
            <div class="text-[11px] text-zinc-500 uppercase font-semibold">총 포트폴리오 가치</div>
            <div id="portfolio-total-val" class="text-xl font-bold text-emerald-400 font-mono mt-1">€0.0M</div>
            <div class="text-[10px] text-zinc-400 mt-0.5">선수 이적료 시장가치 합산</div>
          </div>
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.04]">
            <div class="text-[11px] text-zinc-500 uppercase font-semibold">전속 대리 고객 수</div>
            <div id="portfolio-total-count" class="text-xl font-bold text-white font-mono mt-1">0인</div>
            <div class="text-[10px] text-zinc-400 mt-0.5">선수 및 감독 실시간 전속 계약 현황</div>
          </div>
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.04]">
            <div class="text-[11px] text-zinc-500 uppercase font-semibold">총 주급 / 연봉 규모</div>
            <div id="portfolio-wages-val" class="text-xl font-bold text-amber-300 font-mono mt-1">€0K / 주</div>
            <div class="text-[10px] text-zinc-400 mt-0.5">소속 고객 주급 총합계</div>
          </div>
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.04]">
            <div class="text-[11px] text-zinc-500 uppercase font-semibold">연간 에이전시 예상 수수료</div>
            <div id="portfolio-fee-val" class="text-xl font-bold text-sky-400 font-mono mt-1">€0.0M / 년</div>
            <div class="text-[10px] text-zinc-400 mt-0.5">FFAR Cap 5~10% 법정 요율</div>
          </div>
        </div>
      </div>

      <!-- Filter Controls & Client Search -->
      <div class="flex flex-wrap items-center justify-between gap-3 bg-[#11141a] p-3 rounded-xl border border-white/[0.06]">
        <div class="flex flex-wrap items-center gap-1.5" id="portfolio-filter-tabs">
          <button onclick="filterPortfolio('ALL')" id="pf-btn-all" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition">전체</button>
          <button onclick="filterPortfolio('PLAYER')" id="pf-btn-player" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">선수</button>
          <button onclick="filterPortfolio('MANAGER')" id="pf-btn-manager" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">감독</button>
          <button onclick="filterPortfolio('VIRTUAL')" id="pf-btn-virtual" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">🧪 가상 인물</button>
          <button onclick="filterPortfolio('REAL')" id="pf-btn-real" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">⭐ 실제 발굴 고객</button>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="portfolio-search-input" oninput="handlePortfolioSearch(this.value)" placeholder="고객명/구단/국적 검색..."
            class="bg-[#0e1117] text-xs px-3 py-1.5 rounded-lg border border-white/[0.08] text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50 w-52">
        </div>
      </div>

      <!-- Portfolio Grid Cards Container -->
      <div id="portfolio-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Rendered dynamically via renderPortfolioCards() -->
      </div>
    </div>
"""

HTML_RECRUITMENT = """
    <!-- ======================================================================= -->
    <!-- PAGE: RECRUITMENT WATCHLIST (영입 관심 리스트 및 피치덱 센터) -->
    <!-- ======================================================================= -->
    <div id="page-recruitment" class="page-view hidden space-y-6">

      <!-- Header Banner -->
      <div class="ui-card p-6 border-white/[0.08] relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-72 h-72 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/20">
                ⭐ Agency Recruitment Watchlist
              </span>
              <span class="text-xs text-zinc-400">잠재력 · 스타성 4D 입체 분석 & 대리권 전속 유치</span>
            </div>
            <h2 class="text-2xl font-bold text-white tracking-tight mt-1.5 flex items-center gap-2">
              <span>영입 관심 리스트</span>
              <span class="text-xs font-normal text-zinc-400 font-mono">(Watchlist Radar)</span>
            </h2>
            <p class="text-xs text-zinc-400 mt-1">
              스카우팅에서 관심 타깃으로 등록한 선수·감독 및 가상 테스트 풀을 관리하며, 1-Page 제안서 생성과 전속 계약 체결을 지원합니다.
            </p>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="showPage('page-scouting')"
              class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold transition flex items-center gap-1.5">
              <span>← 스카우팅 로스터로 이동</span>
            </button>
            <button onclick="showPage('page-portfolio')"
              class="px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition flex items-center gap-1.5 shadow-md shadow-emerald-950/30">
              <span>소속 포트폴리오 보기 →</span>
            </button>
          </div>
        </div>

        <!-- 4 Recruitment Categories Pills -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 pt-5 mt-5 border-t border-white/[0.06]">
          <div onclick="filterRecruitmentTargets('UNREPRESENTED')" id="rec-cat-UNREPRESENTED" class="cursor-pointer p-3 rounded-xl bg-[#0e1117] border border-white/[0.04] hover:border-emerald-500/30 transition">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-emerald-400">💎 무소속 / FA 원석</span>
              <span class="text-[10px] bg-emerald-500/10 text-emerald-400 px-1.5 py-0.5 rounded">즉시협상</span>
            </div>
            <p class="text-[11px] text-zinc-400 mt-1">가족 대리인 체제 탈피 및 전문 에이전시 론칭 타깃</p>
          </div>
          <div onclick="filterRecruitmentTargets('EXPIRING_D6')" id="rec-cat-EXPIRING_D6" class="cursor-pointer p-3 rounded-xl bg-[#0e1117] border border-white/[0.04] hover:border-amber-500/30 transition">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-300">⏳ 대리계약 만료 임박 (D-6)</span>
              <span class="text-[10px] bg-amber-500/10 text-amber-300 px-1.5 py-0.5 rounded">FFAR 합법 접촉</span>
            </div>
            <p class="text-[11px] text-zinc-400 mt-1">기존 대리 계약 2개월 미만 잔여 선수 선점 접촉</p>
          </div>
          <div onclick="filterRecruitmentTargets('TIER2_STEPUP')" id="rec-cat-TIER2_STEPUP" class="cursor-pointer p-3 rounded-xl bg-[#0e1117] border border-white/[0.04] hover:border-sky-500/30 transition">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-sky-400">🚀 메가에이전시 스텝업</span>
              <span class="text-[10px] bg-sky-500/10 text-sky-400 px-1.5 py-0.5 rounded">글로벌 확장</span>
            </div>
            <p class="text-[11px] text-zinc-400 mt-1">현 소속사 케어 한계 극복 및 빅클럽 이적 희망</p>
          </div>
          <div onclick="filterRecruitmentTargets('ELITE_MANAGER')" id="rec-cat-ELITE_MANAGER" class="cursor-pointer p-3 rounded-xl bg-[#0e1117] border border-white/[0.04] hover:border-purple-500/30 transition">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-purple-400">👔 차세대 명장 유치 타깃</span>
              <span class="text-[10px] bg-purple-500/10 text-purple-400 px-1.5 py-0.5 rounded">사령탑 확보</span>
            </div>
            <p class="text-[11px] text-zinc-400 mt-1">빅클럽 차기 감독 선임 및 바이아웃 협상 대행</p>
          </div>
        </div>
      </div>

      <!-- Filter Controls & Target Search -->
      <div class="flex flex-wrap items-center justify-between gap-3 bg-[#11141a] p-3 rounded-xl border border-white/[0.06]">
        <div class="flex flex-wrap items-center gap-1.5" id="recruitment-filter-tabs">
          <button onclick="filterRecruitmentTargets('ALL')" id="rec-tab-ALL" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition">
            <span>전체</span>
            <span id="rec-count-all" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-white/20 font-mono">13</span>
          </button>
          <button onclick="filterRecruitmentTargets('PLAYER')" id="rec-tab-PLAYER" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
            <span>선수</span>
            <span id="rec-count-player" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-zinc-800 font-mono">10</span>
          </button>
          <button onclick="filterRecruitmentTargets('MANAGER')" id="rec-tab-MANAGER" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
            <span>감독</span>
            <span id="rec-count-manager" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-zinc-800 font-mono">3</span>
          </button>
          <button onclick="filterRecruitmentTargets('VIRTUAL')" id="rec-tab-VIRTUAL" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
            <span>🧪 가상 테스트 풀</span>
            <span id="rec-count-virtual" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-zinc-800 font-mono">13</span>
          </button>
          <button onclick="filterRecruitmentTargets('SCOUTED')" id="rec-tab-SCOUTED" class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
            <span>⭐ 스카우팅 발굴 관심</span>
            <span id="rec-count-scouted" class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-zinc-800 font-mono">0</span>
          </button>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" id="recruitment-search-input" oninput="handleRecruitmentSearch(this.value)" placeholder="타깃명/구단/포지션 검색..."
            class="bg-[#0e1117] text-xs px-3 py-1.5 rounded-lg border border-white/[0.08] text-white placeholder-zinc-500 focus:outline-none focus:border-amber-500/50 w-52">
        </div>
      </div>

      <!-- Recruitment Target Cards Grid -->
      <div id="recruitment-cards-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Rendered dynamically via renderRecruitmentCards() -->
      </div>
    </div>
"""

HTML_ADMIN = """
    <!-- ======================================================================= -->
    <!-- PAGE: ADMIN CONSOLE (관리자 감사 및 가입 승인 콘솔) -->
    <!-- ======================================================================= -->
    <div id="page-admin" class="page-view hidden space-y-6">

      <!-- Header -->
      <div class="ui-card p-6 border-white/[0.08] bg-[#11141a]">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20">
                ADMIN ACCESS ONLY
              </span>
              <span class="text-xs text-zinc-400">에이전시 내부통제 & 보안 감사 콘솔</span>
            </div>
            <h2 class="text-2xl font-bold text-white tracking-tight mt-1.5">대표 관리자 전용 대시보드</h2>
            <p class="text-xs text-zinc-400 mt-1">
              신규 에이전트 직원 승인, 실시간 권한 감사, 전체 계약 건에 대한 시스템 감사 기록을 조회합니다.
            </p>
          </div>
          <button onclick="loadAdminDashboard()"
            class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold transition flex items-center gap-1.5">
            <span>🔄 새로고침</span>
          </button>
        </div>
      </div>

      <!-- Pending Staff Approvals -->
      <div class="ui-card p-5 border-white/[0.08] bg-[#11141a] space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-bold text-white flex items-center gap-2">
            <span>🛡️ 에이전시 직원 가입 승인 대기 목록</span>
            <span id="admin-pending-count" class="px-2 py-0.5 rounded-full text-xs font-mono bg-amber-500/20 text-amber-300">0명</span>
          </h3>
          <span class="text-[11px] text-zinc-400">승인 즉시 시스템 접근 권한이 활성화됩니다</span>
        </div>

        <div id="admin-pending-users-list" class="space-y-2">
          <!-- Rendered via loadAdminDashboard() -->
        </div>
      </div>

      <!-- Approved Staff Roster -->
      <div class="ui-card p-5 border-white/[0.08] bg-[#11141a] space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-bold text-white flex items-center gap-2">
            <span>👥 승인 완료된 에이전시 임직원 현황</span>
            <span id="admin-approved-count" class="px-2 py-0.5 rounded-full text-xs font-mono bg-emerald-500/20 text-emerald-400">0명</span>
          </h3>
        </div>

        <div id="admin-approved-users-list" class="space-y-2">
          <!-- Rendered via loadAdminDashboard() -->
        </div>
      </div>
    </div>
"""

HTML_VIEWS = f"{HTML_PORTFOLIO}\n{HTML_RECRUITMENT}\n{HTML_ADMIN}"
print("HTML Views defined successfully")
