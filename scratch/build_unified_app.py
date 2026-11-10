import re
from pathlib import Path

INDEX_PATH = Path("src/sports_agency/api/static/index.html")
html = INDEX_PATH.read_text(encoding="utf-8")
print(f"Original index.html lines: {len(html.splitlines())}")

# ==============================================================================
# 1. Update Navigation Tabs in Header
# ==============================================================================
old_nav = """      <!-- Navigation Tabs -->
      <nav class="flex items-center gap-1 bg-[#12151c] border border-white/[0.06] p-1 rounded-xl">
        <button id="nav-btn-home" onclick="showPage('page-home')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-zinc-800 transition flex items-center gap-1.5 shadow-sm">
          <span>대시보드</span>
        </button>
        <button id="nav-btn-scouting" onclick="showPage('page-scouting')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span>스카우팅</span>
        </button>"""

new_nav = """      <!-- Navigation Tabs -->
      <nav class="flex items-center gap-1 bg-[#12151c] border border-white/[0.06] p-1 rounded-xl">
        <button id="nav-btn-home" onclick="showPage('page-home')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-zinc-800 transition flex items-center gap-1.5 shadow-sm">
          <span>대시보드</span>
        </button>
        <button id="nav-btn-portfolio" onclick="showPage('page-portfolio')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>소속 고객</span>
          <span id="nav-portfolio-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-emerald-500/20 text-emerald-400 font-mono hidden">0</span>
        </button>
        <button id="nav-btn-scouting" onclick="showPage('page-scouting')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span>스카우팅</span>
        </button>
        <button id="nav-btn-recruitment" onclick="showPage('page-recruitment')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
          <span>영입 관심 리스트</span>
          <span id="nav-watchlist-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-500/20 text-amber-300 font-mono">13</span>
        </button>"""

if old_nav in html:
    html = html.replace(old_nav, new_nav, 1)
    print("1. Navigation tabs updated")
else:
    print("1. ERROR: old_nav not found")

# ==============================================================================
# 2. Update Header Right Actions (Auth & Admin Console badges)
# ==============================================================================
old_header_right = """        <div id="adc-badge" class="text-xs px-2.5 py-1 rounded-lg border border-white/[0.08] bg-[#12151c] text-zinc-400 flex items-center gap-1.5">
          <span id="adc-dot" class="w-1.5 h-1.5 rounded-full bg-zinc-500"></span>
          <span id="adc-text" class="text-[11px]">시스템 준비</span>
        </div>
      </div>"""

new_header_right = """        <div id="adc-badge" class="text-xs px-2.5 py-1 rounded-lg border border-white/[0.08] bg-[#12151c] text-zinc-400 flex items-center gap-1.5">
          <span id="adc-dot" class="w-1.5 h-1.5 rounded-full bg-zinc-500"></span>
          <span id="adc-text" class="text-[11px]">시스템 준비</span>
        </div>
        <div id="nav-auth-badge" onclick="openAuthModal()" title="에이전시 인증 및 관리자 로그인"
          class="cursor-pointer text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:border-emerald-400 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="nav-auth-text" class="font-medium text-[11px]">인증: admin@agent.com</span>
        </div>
        <button id="nav-btn-admin-console" onclick="showPage('page-admin')" title="관리자 콘솔 (가입 승인 & 당일 감사)"
          class="text-xs px-2.5 py-1 rounded-lg border border-purple-500/30 bg-purple-500/10 text-purple-300 hover:border-purple-400 transition flex items-center gap-1.5">
          <span>🛡️</span>
          <span class="font-medium text-[11px]">관리자 콘솔</span>
        </button>
      </div>"""

if old_header_right in html:
    html = html.replace(old_header_right, new_header_right, 1)
    print("2. Header right actions updated with Auth & Admin Console")
else:
    print("2. ERROR: old_header_right not found")

# ==============================================================================
# 3. Add Watchlist Banner and Button in page-scouting
# ==============================================================================
scouting_target_banner = """    <div id="page-scouting" class="page-view hidden space-y-6">

      <!-- Executive Header & Global Roster Filters -->"""

scouting_replacement_banner = """    <div id="page-scouting" class="page-view hidden space-y-6">

      <!-- Watchlist Quick Access Banner -->
      <div class="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl bg-amber-500/5 border border-amber-500/20 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-amber-400 font-bold">⭐ 에이전시 영입 관심 리스트 (Watchlist)</span>
          <span class="text-zinc-400">| 관심 있는 선수·감독을 <strong>[⭐ 영입 관심 타깃 등록]</strong>하면 영입 관심 리스트에서 1-Page 제안서 생성 및 전속 계약을 진행할 수 있습니다.</span>
        </div>
        <button onclick="showPage('page-recruitment')"
          class="px-3 py-1.5 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 font-semibold transition flex items-center gap-1.5">
          <span>영입 관심 리스트 열기</span>
          <span id="scouting-banner-watchlist-count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-500/30 text-amber-200 font-mono">13</span>
          <span>→</span>
        </button>
      </div>

      <!-- Executive Header & Global Roster Filters -->"""

if scouting_target_banner in html:
    html = html.replace(scouting_target_banner, scouting_replacement_banner, 1)
    print("3. Watchlist quick banner added to page-scouting")
else:
    print("3. ERROR: scouting_target_banner not found")

# Add Watchlist Button in player action bar
old_player_action = """                <div class="space-y-1.5 pt-1">
                  <button onclick="showPage('page-strategy')"
                    class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5">
                    <span>이 선수로 협상 전략 수립하기 →</span>
                  </button>"""

new_player_action = """                <div class="space-y-1.5 pt-1">
                  <button id="btn-scouting-watchlist" onclick="toggleCurrentPlayerWatchlist()"
                    class="w-full py-2 px-3 rounded-lg bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-sm">
                    <span id="scouting-watchlist-icon">⭐</span>
                    <span id="scouting-watchlist-label">영입 관심 타깃 등록 (Watchlist)</span>
                  </button>
                  <button onclick="showPage('page-strategy')"
                    class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5">
                    <span>이 선수로 협상 전략 수립하기 →</span>
                  </button>"""

if old_player_action in html:
    html = html.replace(old_player_action, new_player_action, 1)
    print("4. Watchlist button added to scouting player action bar")
else:
    print("4. ERROR: old_player_action not found")

INDEX_PATH.write_text(html, encoding="utf-8")
print(f"Step 1-4 completed. Current lines: {len(html.splitlines())}")
