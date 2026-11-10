from pathlib import Path

file_path = Path("src/sports_agency/api/static/index.html")
content = file_path.read_text(encoding="utf-8")

# 1. Update top nav
nav_target = """        <button id="nav-btn-tactics" onclick="showPage('page-tactics')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>전술·하이라이트</span>
        </button>"""

nav_replacement = """        <button id="nav-btn-tactics" onclick="showPage('page-tactics')"
          class="nav-btn px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800/60 transition flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>전술·하이라이트</span>
        </button>
        <a href="/tactics" target="_blank"
          class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 hover:bg-emerald-500/20 transition flex items-center gap-1 shadow-sm"
          title="손흥민, 홀란드, 김민재, 이강인 등 유럽 5대 리그 76인 전술 재현 엔진을 새 창으로 엽니다">
          <span>⚽ 2D 전술 재현기 (76인)</span>
          <span class="text-[10px]">↗</span>
        </a>"""

assert nav_target in content, "nav_target not found"
content = content.replace(nav_target, nav_replacement, 1)

# 2. Update page-tactics header and embed iframe
page_tactics_target = """    <div id="page-tactics" class="page-view hidden space-y-5">

      <!-- Breadcrumb Header -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.06] pb-3">
        <div class="flex items-center gap-3">
          <button onclick="showPage('page-home')"
            class="px-2.5 py-1 rounded-lg bg-[#12151c] hover:bg-zinc-800 border border-white/[0.08] text-xs font-medium text-zinc-300 transition">
            ← 대시보드
          </button>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-base font-bold text-white">2D 전술 그리드 엔진 & 경기 하이라이트</h2>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono">StatsBomb 120×80m × Opta</span>
            </div>
            <p class="text-xs text-zinc-400 mt-0.5">실제 경기 공간 좌표 2D 피치 리플레이 · 시야각(FOV) 전술 분석 · 타임스탬프 영상 동기화</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="showPage('page-scouting')"
            class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
            선수 스카우팅으로 이동 →
          </button>
        </div>
      </div>"""

page_tactics_replacement = """    <div id="page-tactics" class="page-view hidden space-y-5">

      <!-- Breadcrumb Header -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-white/[0.06] pb-3">
        <div class="flex items-center gap-3">
          <button onclick="showPage('page-home')"
            class="px-2.5 py-1 rounded-lg bg-[#12151c] hover:bg-zinc-800 border border-white/[0.08] text-xs font-medium text-zinc-300 transition">
            ← 대시보드
          </button>
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-base font-bold text-white">2D 전술 그리드 엔진 & 경기 하이라이트</h2>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono">StatsBomb 120×80m × Opta</span>
            </div>
            <p class="text-xs text-zinc-400 mt-0.5">실제 경기 공간 좌표 2D 피치 리플레이 · 시야각(FOV) 전술 분석 · 타임스탬프 영상 동기화</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a href="/tactics" target="_blank"
            class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 transition shadow-lg shadow-emerald-600/30">
            <span>⚡ 손흥민·홀란드 76인 전술 엔진 새창 열기 ↗</span>
          </a>
          <button onclick="showPage('page-scouting')"
            class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
            선수 스카우팅으로 이동 →
          </button>
        </div>
      </div>

      <!-- 76 Elite Players 2D FM Grid Replayer Embedded Frame -->
      <div class="ui-card p-3 space-y-2 border border-emerald-500/30 bg-[#0b101a]">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="text-xs font-bold text-white">⚡ 유럽 5대 리그 정예 76인 시그니처 전술 재현 엔진 (손흥민 감아차기 · 홀란드 대포알 레이저 · 김민재 스토퍼 · 이강인 라파우사)</span>
          </div>
          <a href="/tactics" target="_blank" class="text-xs text-emerald-400 hover:underline flex items-center gap-1">
            <span>풀스크린 전체화면으로 열기</span>
            <span>↗</span>
          </a>
        </div>
        <div class="w-full h-[760px] rounded-xl overflow-hidden border border-white/[0.08] shadow-2xl bg-[#090d16]">
          <iframe src="/tactics" class="w-full h-full border-0" title="2D Tactical Match Engine"></iframe>
        </div>
      </div>"""

assert page_tactics_target in content, "page_tactics_target not found"
content = content.replace(page_tactics_target, page_tactics_replacement, 1)

file_path.write_text(content, encoding="utf-8")
print("Integrated tactics links and iframe into index.html successfully!")
