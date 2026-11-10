import sys
sys.path.append('.')
import re
from pathlib import Path

INDEX_PATH = Path("src/sports_agency/api/static/index.html")
html = INDEX_PATH.read_text(encoding="utf-8")
print(f"Initial lines: {len(html.splitlines())}")

# 1. Read Drafts
from scratch.draft_html_views import HTML_VIEWS
from scratch.draft_modals import MODALS_HTML
from scratch.draft_javascript import JAVASCRIPT_LOGIC

# 2. Inject HTML Views before </main>
if 'id="page-portfolio"' not in html:
    html = html.replace("  </main>", f"{HTML_VIEWS}\n  </main>", 1)
    print("1. HTML Views (page-portfolio, page-recruitment, page-admin) injected before </main>")
else:
    print("1. page-portfolio already exists in html")

# 3. Inject Modals before </body>
if 'id="modal-client-renewal"' not in html:
    html = html.replace("</body>", f"{MODALS_HTML}\n</body>", 1)
    print("2. Modals injected before </body>")
else:
    print("2. Modals already exist in html")

# 4. Inject JavaScript before window.addEventListener('DOMContentLoaded', initDashboard);
if 'function updateScoutingWatchlistButton(' not in html:
    target_listener = "    window.addEventListener('DOMContentLoaded', initDashboard);"
    html = html.replace(target_listener, f"{JAVASCRIPT_LOGIC}\n\n{target_listener}", 1)
    print("3. JavaScript logic injected before initDashboard listener")
else:
    print("3. JavaScript logic already exists in html")

# 5. Update showPage
old_show_page = """    function showPage(pageId) {
      activePageId = pageId;
      document.querySelectorAll('.page-view').forEach(p => p.classList.add('hidden'));

      const target = document.getElementById(pageId);
      if (target) {
        target.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }

      updateNavState(pageId);"""

new_show_page = """    function showPage(pageId) {
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
      if (pageId === 'page-admin') loadAdminDashboard();"""

if old_show_page in html:
    html = html.replace(old_show_page, new_show_page, 1)
    print("4. showPage updated")
else:
    print("4. Notice: old_show_page pattern not found, checking if already updated...")

# 6. Update updateNavState
old_nav_state = """      const buttons = [
        { id: 'nav-btn-home', key: 'home' },
        { id: 'nav-btn-scouting', key: 'scouting' },
        { id: 'nav-btn-strategy', key: 'strategy' },
        { id: 'nav-btn-tactics', key: 'tactics' },
        { id: 'nav-btn-documents', key: 'documents' },
        { id: 'nav-btn-finance', key: 'finance' },
        { id: 'nav-btn-regulations', key: 'regulations' },
      ];"""

new_nav_state = """      const buttons = [
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
      ];"""

if old_nav_state in html:
    html = html.replace(old_nav_state, new_nav_state, 1)
    print("5. updateNavState updated")
else:
    print("5. Notice: old_nav_state pattern not found")

# 7. Update selectPlayer to update watchlist button
old_select_p = """    function selectPlayer(p) {
      selectedPlayer = p;"""

new_select_p = """    function selectPlayer(p) {
      selectedPlayer = p;
      const targetType = (p.position === 'MGR') ? 'MANAGER' : 'PLAYER';
      if (typeof updateScoutingWatchlistButton === 'function') {
        updateScoutingWatchlistButton(p.player_id, targetType);
      }"""

if old_select_p in html:
    html = html.replace(old_select_p, new_select_p, 1)
    print("6. selectPlayer updated with updateScoutingWatchlistButton call")
else:
    print("6. Notice: old_select_p pattern not found")

# 8. Update initDashboard
old_init_db = """    async function initDashboard() {
      const hash = window.location.hash.replace('#', '');
      const initialPage = hash ? `page-${hash}` : 'page-home';

      await Promise.all([
        loadSystemStatus(),
        loadQuotaStatus(),
        loadPlayers(),
        loadBosmanRadar(),
        loadUndervaluedProspects(),
        runStandalonePsrCalc()
      ]);"""

new_init_db = """    async function initDashboard() {
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
      ]);"""

if old_init_db in html:
    html = html.replace(old_init_db, new_init_db, 1)
    print("7. initDashboard updated with initAuth, loadAgencyPortfolio, loadAgencyRecruitmentTargets")
else:
    print("7. Notice: old_init_db pattern not found")

INDEX_PATH.write_text(html, encoding="utf-8")
print(f"Completed! Final lines: {len(html.splitlines())}")
