/**
 * AgencyOS Pro - Core Application Lifecycle & Router
 */

const AppState = {
  currentPage: 'page-scouting',
  selectedPlayer: null,
  agencyClients: [],
  tickerRumors: [],
  tickerInjuries: []
};

function showPage(pageId) {
  // Alias resolution
  const aliases = {
    'page-strategy': 'page-strategy',
    'strategy': 'page-strategy',
    'page-negotiation': 'page-strategy',
    'negotiation': 'page-strategy',
    'page-tactics': 'page-tactics',
    'tactics': 'page-tactics',
    'page-scouting': 'page-scouting',
    'scouting': 'page-scouting',
    'page-clients': 'page-clients',
    'clients': 'page-clients',
    'portfolio': 'page-clients',
    'page-documents': 'page-documents',
    'documents': 'page-documents',
    'page-finance': 'page-finance',
    'finance': 'page-finance',
    'page-regulations': 'page-regulations',
    'regulations': 'page-regulations'
  };

  const targetId = aliases[pageId] || pageId;
  const pages = document.querySelectorAll('.page-section');
  pages.forEach(p => p.classList.add('hidden'));

  const activePage = document.getElementById(targetId);
  if (activePage) {
    activePage.classList.remove('hidden');
    AppState.currentPage = targetId;
    window.location.hash = targetId.replace('page-', '');
  }
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  const colors = {
    info: 'bg-indigo-600 text-white border-indigo-500',
    success: 'bg-emerald-600 text-white border-emerald-500',
    warning: 'bg-amber-600 text-white border-amber-500',
    error: 'bg-rose-600 text-white border-rose-500'
  };
  toast.className = `px-4 py-2.5 rounded-lg shadow-lg border text-xs font-semibold flex items-center gap-2 transition-all transform duration-300 ${colors[type] || colors.info}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
