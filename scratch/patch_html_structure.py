import re

html_path = 'src/sports_agency/api/static/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length of index.html:", len(content))

# -----------------------------------------------------------------------------
# Part 1: Remove external-prospect widget from Left Column to eliminate dead space
# -----------------------------------------------------------------------------
left_col_widget = """            <!-- External Prospect Onboarding Widget (API-Football 1,100+ Leagues) -->
            <div class="mt-3 pt-3 border-t border-white/[0.08]">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  5대 리그 외 유망주 등록 (API-Football)
                </span>
                <span class="text-[10px] text-zinc-500">K리그·J리그·남미</span>
              </div>
              <div class="flex gap-1.5">
                <input id="external-prospect-input" type="text"
                  placeholder="유망주 영문/한글 이름 (예: Seol, Yang Min-Hyeok)"
                  class="flex-1 bg-[#0e1117] border border-white/[0.08] rounded-lg px-2.5 py-1 text-[11px] text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500" />
                <button id="btn-onboard-prospect" onclick="onboardExternalProspectUI()"
                  class="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-[11px] font-semibold whitespace-nowrap transition">
                  등록
                </button>
              </div>
              <div id="onboard-result-box" class="hidden mt-2 p-2 rounded-lg border border-emerald-500/30 bg-emerald-950/20 text-xs text-zinc-200"></div>
            </div>"""

if left_col_widget in content:
    content = content.replace(left_col_widget, "<!-- External Prospect widget integrated into custom registration panel -->")
    print("Step 1: Removed redundant external prospect widget from left column.")
else:
    print("Warning: left_col_widget not found by exact string, checking regex...")

# -----------------------------------------------------------------------------
# Part 2: Upgrade 2D Position Scatter Plot HTML (5 Position Roles & Modern Badges)
# -----------------------------------------------------------------------------
old_scatter_tabs = """              <div class="flex items-center gap-1.5">
                <button id="scatter-tab-fw" onclick="switchScatterView('FW')"
                  class="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-600 text-white transition shadow-sm">
                  ⚽ 공격수/윙어 (xG vs 슈팅전환율)
                </button>
                <button id="scatter-tab-mf" onclick="switchScatterView('MF')"
                  class="px-2.5 py-1 rounded-lg text-xs font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  🎯 미드필더 (전진액션 vs Opta xT)
                </button>
              </div>"""

new_scatter_tabs = """              <div class="flex items-center gap-1 flex-wrap">
                <button id="scatter-tab-fw" onclick="switchScatterView('FW')"
                  class="px-2 py-1 rounded-lg text-[11px] font-bold bg-emerald-600 text-white transition shadow-sm">
                  ⚽ 공격수 (xG vs 결정력)
                </button>
                <button id="scatter-tab-mf" onclick="switchScatterView('MF')"
                  class="px-2 py-1 rounded-lg text-[11px] font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  🎯 미드필더 (전진액션 vs xT)
                </button>
                <button id="scatter-tab-df" onclick="switchScatterView('DF')"
                  class="px-2 py-1 rounded-lg text-[11px] font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  🛡️ 수비수 (경합성공 vs 태클)
                </button>
                <button id="scatter-tab-gk" onclick="switchScatterView('GK')"
                  class="px-2 py-1 rounded-lg text-[11px] font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  🧤 골키퍼 (선방률 vs PSxG)
                </button>
                <button id="scatter-tab-mgr" onclick="switchScatterView('MGR')"
                  class="px-2 py-1 rounded-lg text-[11px] font-medium text-zinc-400 hover:text-white hover:bg-zinc-800 transition">
                  👔 사령탑 (승점 PPG vs 득실)
                </button>
              </div>"""

if old_scatter_tabs in content:
    content = content.replace(old_scatter_tabs, new_scatter_tabs)
    print("Step 2: Upgraded scatter plot role tabs in HTML.")
else:
    print("Warning: old_scatter_tabs not found by exact string.")

# -----------------------------------------------------------------------------
# Part 3: Upgrade Bosman Radar sub-tab HTML (Clear Coach vs Player distinction)
# -----------------------------------------------------------------------------
old_bosman_panel = """        <!-- Sub-Tab 2: Bosman Radar -->
        <div id="scout-panel-bosman" class="hidden space-y-3 pt-1">
          <div class="flex flex-wrap items-center gap-2">
            <select id="bosman-pos-select" onchange="loadBosmanRadar()"
              class="bg-[#0e1117] border border-white/[0.08] rounded-lg px-2.5 py-1.5 text-xs text-white">
              <option value="ALL">전체 포지션</option>
              <option value="ST">ST</option><option value="LW">LW</option><option value="RW">RW</option>
              <option value="AM">AM</option><option value="CM">CM</option><option value="DM">DM</option>
              <option value="CB">CB</option><option value="RB">RB</option><option value="LB">LB</option>
            </select>
            <select id="bosman-league-select" onchange="loadBosmanRadar()"
              class="bg-[#0e1117] border border-white/[0.08] rounded-lg px-2.5 py-1.5 text-xs text-white">
              <option value="ALL">5대 리그 전체</option>
              <option value="Premier League">Premier League</option>
              <option value="La Liga">La Liga</option>
              <option value="Serie A">Serie A</option>
              <option value="Bundesliga">Bundesliga</option>
              <option value="Ligue 1">Ligue 1</option>
            </select>
            <span id="bosman-count-badge" class="text-xs text-zinc-400 ml-auto">스캔 중...</span>
          </div>
          <div id="bosman-radar-grid" class="grid grid-cols-1 md:grid-cols-3 gap-2.5 max-h-56 overflow-y-auto pr-1"></div>
        </div>"""

new_bosman_panel = """        <!-- Sub-Tab 2: Bosman Radar -->
        <div id="scout-panel-bosman" class="hidden space-y-3 pt-1">
          <!-- Clear Target Type Segmentation (선수 공백 vs 감독 공석) -->
          <div class="flex flex-wrap items-center justify-between gap-2 p-2 rounded-xl bg-[#0e1117] border border-white/[0.06]">
            <div class="flex items-center gap-1.5">
              <button id="bosman-filter-btn-all" onclick="setBosmanTargetType('ALL')"
                class="px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-600 text-white transition shadow-sm">
                전체 영입 기회
              </button>
              <button id="bosman-filter-btn-player" onclick="setBosmanTargetType('PLAYER')"
                class="px-2.5 py-1 rounded-lg text-xs font-medium text-zinc-400 bg-zinc-800 hover:text-white transition">
                ⚽ 선수 포지션 공백 구단
              </button>
              <button id="bosman-filter-btn-mgr" onclick="setBosmanTargetType('MGR')"
                class="px-2.5 py-1 rounded-lg text-xs font-medium text-zinc-400 bg-zinc-800 hover:text-white transition">
                👔 사령탑 공석/교체 구단
              </button>
            </div>
            <div class="flex items-center gap-2">
              <select id="bosman-pos-select" onchange="loadBosmanRadar()"
                class="bg-[#12151c] border border-white/[0.08] rounded-lg px-2.5 py-1 text-xs text-white">
                <option value="ALL">전체 포지션</option>
                <option value="ST">ST (스트라이커)</option><option value="LW">LW (좌측윙)</option><option value="RW">RW (우측윙)</option>
                <option value="AM">AM (공격형미드)</option><option value="CM">CM (중앙미드)</option><option value="DM">DM (수비형미드)</option>
                <option value="CB">CB (센터백)</option><option value="RB">RB (우측풀백)</option><option value="LB">LB (좌측풀백)</option>
              </select>
              <select id="bosman-league-select" onchange="loadBosmanRadar()"
                class="bg-[#12151c] border border-white/[0.08] rounded-lg px-2.5 py-1 text-xs text-white">
                <option value="ALL">5대 리그 전체</option>
                <option value="Premier League">Premier League</option>
                <option value="La Liga">La Liga</option>
                <option value="Serie A">Serie A</option>
                <option value="Bundesliga">Bundesliga</option>
                <option value="Ligue 1">Ligue 1</option>
              </select>
              <span id="bosman-count-badge" class="text-xs text-zinc-400 font-mono">스캔 중...</span>
            </div>
          </div>
          <div id="bosman-radar-grid" class="grid grid-cols-1 md:grid-cols-3 gap-2.5 max-h-64 overflow-y-auto pr-1"></div>
        </div>"""

if old_bosman_panel in content:
    content = content.replace(old_bosman_panel, new_bosman_panel)
    print("Step 3: Upgraded Bosman Radar HTML with distinct player/manager filters.")
else:
    print("Warning: old_bosman_panel not found by exact string.")

# -----------------------------------------------------------------------------
# Part 4: Integrate API-Football Prospect Registration into Sub-Tab 3 (No dead space)
# -----------------------------------------------------------------------------
old_custom_panel = """        <!-- Sub-Tab 3: Custom Player -->
        <div id="scout-panel-custom" class="hidden space-y-3 pt-1">
          <!-- Position Template Quick Selectors -->"""

new_custom_panel = """        <!-- Sub-Tab 3: External Prospect & Custom Player Registration -->
        <div id="scout-panel-custom" class="hidden space-y-4 pt-1">
          <!-- Unified Section 1: API-Football Prospect Auto-Search (K-League, J-League, South America, etc.) -->
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-emerald-500/25 space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                📡 5대 리그 외 글로벌 유망주 원클릭 등록 (API-Football 1,100+개 리그)
              </span>
              <span class="text-[10px] text-zinc-400">K리그·J리그·에레디비시·남미 유망주 실측 DB 즉시 연동</span>
            </div>
            <div class="flex gap-2">
              <input id="external-prospect-input" type="text"
                placeholder="유망주 영문 또는 한글 이름 (예: Seol, Yang Min-Hyeok, Endrick)"
                class="flex-1 bg-[#12151c] border border-white/[0.08] rounded-lg px-3 py-1.5 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-emerald-500" />
              <button id="btn-onboard-prospect" onclick="onboardExternalProspectUI()"
                class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold whitespace-nowrap transition shadow-sm flex items-center gap-1">
                <span>⚡ 실시간 스카우팅 등록</span>
              </button>
            </div>
            <div id="onboard-result-box" class="hidden p-2.5 rounded-lg border border-emerald-500/30 bg-emerald-950/20 text-xs text-zinc-200"></div>
          </div>

          <!-- Unified Section 2: Manual Position Stat Editor -->
          <div class="p-3.5 rounded-xl bg-[#0e1117] border border-white/[0.06] space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-semibold text-zinc-200 flex items-center gap-1.5">
                <span>✍️</span> 외부 선수 정밀 스탯 직접 입력 등록
              </span>
              <span class="text-[10px] text-zinc-500">Opta & DataMB 6대 세부 지표 수기 보정 등록</span>
            </div>
            <!-- Position Template Quick Selectors -->"""

if old_custom_panel in content:
    content = content.replace(old_custom_panel, new_custom_panel)
    # also close the extra div at the end of custom panel
    content = content.replace("""            <div>
              <label class="text-[10px] text-zinc-400 block mb-0.5">등록 실행</label>
              <button onclick="registerCustomClient()"
                class="w-full py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition">
                + 신규 등록
              </button>
            </div>
          </div>
        </div>""", """            <div>
              <label class="text-[10px] text-zinc-400 block mb-0.5">등록 실행</label>
              <button onclick="registerCustomClient()"
                class="w-full py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition">
                + 신규 등록
              </button>
            </div>
          </div>
          </div>
        </div>""")
    print("Step 4: Integrated API-Football Prospect Registration into Custom Sub-Tab.")
else:
    print("Warning: old_custom_panel not found by exact string.")

# -----------------------------------------------------------------------------
# Part 5: Upgrade modal-client-transfer HTML (Dropdown clubs, no min/max fee restrictions)
# -----------------------------------------------------------------------------
old_transfer_inputs = """          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">이적 목적지 구단명</label>
              <input type="text" id="transfer-club-input" required placeholder="예: Real Madrid, Arsenal, FC Bayern"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500">
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">소속 리그</label>
              <select id="transfer-league-select" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500">
                <option value="Premier League">Premier League (EPL)</option>
                <option value="La Liga">La Liga</option>
                <option value="Bundesliga">Bundesliga</option>
                <option value="Serie A">Serie A</option>
                <option value="Ligue 1">Ligue 1</option>
                <option value="기타 글로벌 리그">기타 글로벌 리그</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">제시 이적료 (€)</label>
              <input type="number" id="transfer-fee-input" required min="100000" step="500000"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">신규 주급 (€ / Week)</label>
              <input type="number" id="transfer-wage-input" required min="1000" step="1000"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
            </div>
          </div>"""

new_transfer_inputs = """          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">이적 목적지 리그</label>
              <select id="transfer-league-select" onchange="updateTransferClubsDropdown()" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500">
                <option value="Premier League" selected>Premier League (EPL)</option>
                <option value="La Liga">La Liga</option>
                <option value="Bundesliga">Bundesliga</option>
                <option value="Serie A">Serie A</option>
                <option value="Ligue 1">Ligue 1</option>
                <option value="기타 글로벌 리그">기타 글로벌 리그</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">이적 목적지 구단 선택</label>
              <select id="transfer-club-select" onchange="onTransferClubSelectChange()" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500">
                <!-- Dynamically populated based on chosen league -->
              </select>
              <input type="text" id="transfer-club-custom-input" placeholder="직접 구단명 입력 (예: AFC Ajax)"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 mt-1.5 hidden">
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">제시 이적료 (€ - 제한 없음)</label>
              <input type="number" id="transfer-fee-input" required min="0" step="any"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
            </div>
            <div>
              <label class="block text-xs font-medium text-zinc-300 mb-1">신규 주급 (€ / Week - 제한 없음)</label>
              <input type="number" id="transfer-wage-input" required min="0" step="any"
                class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
            </div>
          </div>"""

if old_transfer_inputs in content:
    content = content.replace(old_transfer_inputs, new_transfer_inputs)
    print("Step 5: Upgraded transfer modal inputs with dynamic club dropdown and removed fee/wage restrictions.")
else:
    print("Warning: old_transfer_inputs not found by exact string.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved HTML structure changes.")
