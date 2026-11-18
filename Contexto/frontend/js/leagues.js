import { apiGet } from './api.js';
import { showTable, escapeHtml, showAlert } from './utils.js';

export function init() {
  const btn = document.getElementById('btn-load-leagues');
  if (btn) btn.addEventListener('click', load);
}

export async function load() {
  try {
    const leagues = await apiGet('/leagues');
    if (!leagues || leagues.length === 0) {
      showAlert('auth-status', '⚠ No hay ligas disponibles.', 'info');
      return;
    }
    const headers = ['ID', 'Nombre', 'País'];
    const rows = leagues.map(l =>
      '<tr><td>' + l.id + '</td><td>' + escapeHtml(l.name) + '</td><td>' + escapeHtml(l.country || '-') + '</td></tr>'
    ).join('');
    showTable('leagues-table', headers, rows);
    showAlert('auth-status', '✅ Ligas cargadas: ' + leagues.length + ' disponibles', 'success');
  } catch (e) {
    showAlert('auth-status', '❌ ' + e.message, 'error');
  }
}
