import { apiGet, isLoggedIn } from './api.js';
import { showAlert, escapeHtml } from './utils.js';

export function init() {
  document.getElementById('btn-load-leaderboard').addEventListener('click', () => {
    const tid = document.getElementById('lb-tournament').value;
    if (tid) load(tid);
  });
}

export async function load(tournamentId) {
  if (!isLoggedIn()) { showAlert('leaderboard-data', 'Inicia sesion para ver el leaderboard.', 'error'); return; }
  try {
    const lb = await apiGet('/tournaments/' + tournamentId + '/leaderboard');
    const container = document.getElementById('leaderboard-data');
    if (!lb) { showAlert('leaderboard-data', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    let html = '<div class="alert-info">Tu puesto: <b>' + (lb.my_rank ?? '-') + '</b> | Tus puntos: <b>' + (lb.my_points ?? '-') + '</b></div>';
    html += '<table class="lb-table"><thead><tr><th>#</th><th>Usuario</th><th>Puntos</th><th>Aciertos</th><th>Precision</th></tr></thead><tbody>';
    lb.entries.forEach((e, i) => {
      const isYou = (e.rank === lb.my_rank) ? ' (tu)' : '';
      html += '<tr><td>' + (i + 1) + '</td><td>' + escapeHtml(e.username) + isYou + '</td><td>' + e.total_points + '</td><td>' + e.predictions_count + '</td><td>' + e.accuracy + '%</td></tr>';
    });
    html += '</tbody></table>';
    container.innerHTML = html;
    showAlert('leaderboard-data', 'Leaderboard cargado: ' + lb.entries.length + ' participantes.', 'success');
  } catch (e) {
    showAlert('leaderboard-data', e.message, 'error');
  }
}

window.leaderboardModule = { init, load };
