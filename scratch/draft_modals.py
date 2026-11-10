MODALS_HTML = """
  <!-- ========================================================================= -->
  <!-- MODAL: AUTHENTICATION (Firebase / Agency Login & Signup) -->
  <!-- ========================================================================= -->
  <div id="modal-auth" class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm hidden">
    <div class="ui-card w-full max-w-md p-6 border-white/[0.12] bg-[#12151c] shadow-2xl relative">
      <!-- Close Button -->
      <button onclick="closeAuthModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>

      <!-- Modal Title -->
      <div class="flex items-center gap-2 mb-4">
        <div class="w-7 h-7 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-xs">
          FC
        </div>
        <div>
          <h3 class="text-base font-bold text-white tracking-tight">Antigravity Sports OS</h3>
          <p class="text-[11px] text-zinc-400">FIFA 공인 에이전시 업무 포털 인증</p>
        </div>
      </div>

      <!-- Quick Admin Auto-fill Button -->
      <div class="mb-4 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-between">
        <div>
          <div class="text-[11px] font-bold text-amber-300">👑 대표 관리자 1초 로그인</div>
          <div class="text-[10px] text-zinc-400 font-mono">admin@agent.com / password1234</div>
        </div>
        <button onclick="fillAdminCredentials()"
          class="px-2.5 py-1 rounded bg-amber-500 hover:bg-amber-400 text-black text-xs font-bold transition">
          자동입력
        </button>
      </div>

      <!-- Tabs: Login vs Signup -->
      <div class="flex border-b border-white/[0.08] mb-4">
        <button id="auth-tab-btn-login" onclick="switchAuthTab('login')"
          class="flex-1 pb-2 text-xs font-bold text-emerald-400 border-b-2 border-emerald-400 transition text-center">
          로그인
        </button>
        <button id="auth-tab-btn-signup" onclick="switchAuthTab('signup')"
          class="flex-1 pb-2 text-xs font-medium text-zinc-400 hover:text-zinc-200 transition text-center">
          직원 회원가입 신청
        </button>
      </div>

      <!-- Alert Box -->
      <div id="auth-alert-box" class="hidden mb-3 p-2.5 rounded-lg text-xs leading-relaxed"></div>

      <!-- Login Form -->
      <form id="form-auth-login" onsubmit="submitLoginForm(event)" class="space-y-3">
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">이메일 계정</label>
          <input type="email" id="login-email" required placeholder="admin@agent.com"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
        </div>
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">비밀번호</label>
          <input type="password" id="login-password" required placeholder="••••••••"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
        </div>
        <div class="pt-2">
          <button type="submit" id="btn-submit-login"
            class="w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition shadow-lg shadow-emerald-950/40">
            에이전시 시스템 로그인
          </button>
        </div>
      </form>

      <!-- Signup Form -->
      <form id="form-auth-signup" onsubmit="submitSignupForm(event)" class="space-y-3 hidden">
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">성명 (실명)</label>
          <input type="text" id="signup-name" required placeholder="홍길동 수석에이전트"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
        </div>
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">이메일 계정</label>
          <input type="email" id="signup-email" required placeholder="agent@agency.com"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
        </div>
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">소속 부서</label>
          <select id="signup-department" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
            <option value="선수영입1팀">선수영입1팀</option>
            <option value="선수영입2팀">선수영입2팀</option>
            <option value="법무계약팀">법무계약팀</option>
            <option value="전술데이터팀">전술데이터팀</option>
            <option value="재무전략팀">재무전략팀</option>
            <option value="글로벌마케팅팀">글로벌마케팅팀</option>
          </select>
        </div>
        <div>
          <label class="block text-[11px] font-medium text-zinc-400 mb-1">비밀번호 (6자 이상)</label>
          <input type="password" id="signup-password" minlength="6" required placeholder="••••••••"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
        </div>
        <p class="text-[10px] text-zinc-400 leading-tight">
          ※ 에이전시 보안 규정에 따라 가입 즉시 <strong class="text-amber-300">승인 대기(PENDING)</strong> 상태가 되며, 대표 관리자(admin@agent.com)의 승인 후 로그인이 활성화됩니다.
        </p>
        <div class="pt-2">
          <button type="submit" id="btn-submit-signup"
            class="w-full py-2.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition shadow-lg shadow-sky-950/40">
            회원가입 신청서 제출
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: RECRUITMENT PITCH DECK VIEWER -->
  <!-- ========================================================================= -->
  <div id="modal-pitch-viewer" class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md hidden p-4">
    <div class="ui-card w-full max-w-4xl max-h-[90vh] flex flex-col border-white/[0.12] bg-[#11141a] shadow-2xl relative overflow-hidden">
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-white/[0.08] flex items-center justify-between bg-[#161a22]">
        <div class="flex items-center gap-2.5">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            ⭐ 1-PAGE PITCH DECK
          </span>
          <h3 id="pitch-modal-title" class="text-base font-bold text-white tracking-tight">영입 제안서 뷰어</h3>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition flex items-center gap-1">
            <span>🖨️ 인쇄 / PDF</span>
          </button>
          <button onclick="downloadPitchMarkdown()" class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition flex items-center gap-1">
            <span>📥 마크다운</span>
          </button>
          <button onclick="closePitchModal()" class="text-zinc-400 hover:text-white p-1 ml-1 transition">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Pitch Deck Markdown Scrollable Content -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div id="pitch-modal-body" class="markdown-body">
          <!-- Rendered marked.js output with inline SVGs -->
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-3 border-t border-white/[0.08] flex items-center justify-between bg-[#161a22]">
        <div class="text-[11px] text-zinc-400">
          FIFA Football Agent Regulations (Article 12/13) 표준 전속 제안서
        </div>
        <div class="flex items-center gap-2">
          <button id="btn-pitch-enroll-action" onclick=""
            class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center gap-1.5 shadow-md">
            <span>✍️ 전속 대리 계약 체결 (소속 등록)</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT CONTRACT RENEWAL (소속팀 재계약) -->
  <!-- ========================================================================= -->
  <div id="modal-client-renewal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
    <div class="ui-card w-full max-w-lg p-6 border-white/[0.12] bg-[#12151c] shadow-2xl relative">
      <button onclick="closeClientRenewalModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>

      <div class="flex items-center gap-2 mb-4">
        <span class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm">🔄</span>
        <div>
          <h3 id="renewal-modal-title" class="text-base font-bold text-white tracking-tight">소속팀 재계약 협상</h3>
          <p id="renewal-modal-subtitle" class="text-xs text-zinc-400">현재 소속 구단과의 계약 연장 및 주급 인상 협상</p>
        </div>
      </div>

      <form onsubmit="submitClientRenewal(event)" class="space-y-4">
        <input type="hidden" id="renewal-client-id">
        <input type="hidden" id="renewal-client-type" value="PLAYER">

        <div class="grid grid-cols-2 gap-3 p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] text-xs">
          <div>
            <span class="text-zinc-500">현재 구단:</span>
            <span id="renewal-current-club" class="font-bold text-white ml-1">-</span>
          </div>
          <div>
            <span class="text-zinc-500">현재 주급:</span>
            <span id="renewal-current-wage" class="font-mono font-bold text-amber-300 ml-1">-</span>
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-zinc-300 mb-1">희망 주급 (€ / Week)</label>
          <input type="number" id="renewal-wage-input" required min="1000" step="1000"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500 font-mono">
          <p class="text-[10px] text-zinc-500 mt-1">※ 기본 권장: 현 주급 대비 15~25% 인상안</p>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">계약 연장 기간</label>
            <select id="renewal-years-select" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500">
              <option value="1">1년 연장</option>
              <option value="2">2년 연장</option>
              <option value="3" selected>3년 연장 (표준)</option>
              <option value="4">4년 연장</option>
              <option value="5">5년 장기계약</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">재계약 보너스 (€)</label>
            <input type="number" id="renewal-bonus-input" placeholder="선택사항 (예: 2000000)" min="0" step="50000"
              class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500 font-mono">
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-zinc-300 mb-1">신규 바이아웃 조항 (€ - 선택사항)</label>
          <input type="number" id="renewal-buyout-input" placeholder="미설정 시 구단 방침 준용" min="0" step="1000000"
            class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-emerald-500 font-mono">
        </div>

        <div class="pt-2 flex items-center justify-end gap-2">
          <button type="button" onclick="closeClientRenewalModal()"
            class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
            취소
          </button>
          <button type="submit"
            class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition shadow-md shadow-emerald-950/40">
            재계약 체결 실행
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT TRANSFER (5대 리그 구단 이적) -->
  <!-- ========================================================================= -->
  <div id="modal-client-transfer" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
    <div class="ui-card w-full max-w-lg p-6 border-white/[0.12] bg-[#12151c] shadow-2xl relative">
      <button onclick="closeClientTransferModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>

      <div class="flex items-center gap-2 mb-4">
        <span class="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-bold text-sm">🚀</span>
        <div>
          <h3 id="transfer-modal-title" class="text-base font-bold text-white tracking-tight">구단 이적 협상</h3>
          <p id="transfer-modal-subtitle" class="text-xs text-zinc-400">새로운 구단으로의 이적 계약 및 연봉 협상</p>
        </div>
      </div>

      <form onsubmit="submitClientTransfer(event)" class="space-y-4">
        <input type="hidden" id="transfer-client-id">
        <input type="hidden" id="transfer-client-type" value="PLAYER">

        <div class="grid grid-cols-2 gap-3 p-3 rounded-lg bg-[#0e1117] border border-white/[0.04] text-xs">
          <div>
            <span class="text-zinc-500">현재 구단:</span>
            <span id="transfer-current-club" class="font-bold text-white ml-1">-</span>
          </div>
          <div>
            <span class="text-zinc-500">현재 시장가치:</span>
            <span id="transfer-current-val" class="font-mono font-bold text-emerald-400 ml-1">-</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">이적 목적지 구단명</label>
            <input type="text" id="transfer-club-input" required placeholder="예: Real Madrid, Arsenal"
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
            <label class="block text-xs font-medium text-zinc-300 mb-1">최종 이적료 (€)</label>
            <input type="number" id="transfer-fee-input" required min="100000" step="500000"
              class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
          </div>
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">신규 주급 (€ / Week)</label>
            <input type="number" id="transfer-wage-input" required min="1000" step="1000"
              class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500 font-mono">
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-zinc-300 mb-1">계약 기간</label>
          <select id="transfer-years-select" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-sky-500">
            <option value="2">2년 계약</option>
            <option value="3">3년 계약</option>
            <option value="4" selected>4년 계약 (표준)</option>
            <option value="5">5년 계약</option>
          </select>
        </div>

        <div class="pt-2 flex items-center justify-end gap-2">
          <button type="button" onclick="closeClientTransferModal()"
            class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
            취소
          </button>
          <button type="submit"
            class="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition shadow-md shadow-sky-950/40">
            이적 계약 완료
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: CLIENT SIGN NEW CLUB (FA 입단 계약) -->
  <!-- ========================================================================= -->
  <div id="modal-client-sign-club" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
    <div class="ui-card w-full max-w-lg p-6 border-white/[0.12] bg-[#12151c] shadow-2xl relative">
      <button onclick="closeClientSignClubModal()" class="absolute top-4 right-4 text-zinc-400 hover:text-white transition">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>

      <div class="flex items-center gap-2 mb-4">
        <span class="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-300 font-bold text-sm">🟡</span>
        <div>
          <h3 id="sign-club-modal-title" class="text-base font-bold text-white tracking-tight">새 구단 입단 계약 (FA)</h3>
          <p id="sign-club-modal-subtitle" class="text-xs text-zinc-400">무소속(FA) 상태 고객의 신규 구단 입단 계약 체결</p>
        </div>
      </div>

      <form onsubmit="submitClientSignClub(event)" class="space-y-4">
        <input type="hidden" id="fa-client-id">
        <input type="hidden" id="fa-client-type" value="PLAYER">

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">입단 구단명</label>
            <input type="text" id="fa-club-input" required placeholder="예: Tottenham Hotspur, FC Seoul"
              class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-amber-500">
          </div>
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">소속 리그</label>
            <select id="fa-league-select" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-amber-500">
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
            <label class="block text-xs font-medium text-zinc-300 mb-1">주급 (€ / Week)</label>
            <input type="number" id="fa-wage-input" required min="1000" step="1000"
              class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-amber-500 font-mono">
          </div>
          <div>
            <label class="block text-xs font-medium text-zinc-300 mb-1">계약 기간</label>
            <select id="fa-years-select" class="w-full bg-[#0e1117] text-xs px-3 py-2 rounded-lg border border-white/[0.08] text-white focus:outline-none focus:border-amber-500">
              <option value="1">1년 계약</option>
              <option value="2">2년 계약</option>
              <option value="3" selected>3년 계약</option>
              <option value="4">4년 계약</option>
            </select>
          </div>
        </div>

        <div class="pt-2 flex items-center justify-end gap-2">
          <button type="button" onclick="closeClientSignClubModal()"
            class="px-3.5 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs font-medium transition">
            취소
          </button>
          <button type="submit"
            class="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs transition shadow-md shadow-amber-950/40">
            입단 계약 체결 완료
          </button>
        </div>
      </form>
    </div>
  </div>
"""
print("Modals HTML defined successfully")
