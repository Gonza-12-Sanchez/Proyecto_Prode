import { apiGet, apiPost, isLoggedIn } from './api.js';
import { showAlert, escapeHtml } from './utils.js';

let predictTournamentId = null;

export function init() {
  document.getElementById('btn-load-matches').addEventListener('click', () => {
    const tid = document.getElementById('predict-tournament').value;
    if (tid) loadMatches(tid);
  });
}

export async function loadMatches(tournamentId) {
  if (!isLoggedIn()) { showAlert('auth-status', 'Inicia sesion para ver partidos.', 'error'); return; }
  predictTournamentId = tournamentId;
  try {
    const matches = await apiGet('/tournaments/' + tournamentId + '/matches?next_days=7');
    const container = document.getElementById('matches-list');
    if (!matches) { showAlert('auth-status', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    if (matches.length === 0) {
      container.innerHTML = '<div class="status-info">Sin partidos disponibles.</div>';
      showAlert('auth-status', 'No hay partidos disponibles para este torneo.', 'info');
      return;
    }
    let html = '';
    matches.forEach(m => {
      const homePred = m.my_prediction ? m.my_prediction.home_score : '';
      const awayPred = m.my_prediction ? m.my_prediction.away_score : '';
      const predLabel = m.my_prediction ? ' (tu: ' + m.my_prediction.home_score + '-' + m.my_prediction.away_score + ')' : '';
      html += '<div class="prediction-card">' +
        '<div class="match-header">' + escapeHtml(m.home_team) + ' vs ' + escapeHtml(m.away_team) + ' ' +
        '<span class="badge ' + (m.status === 'FT' ? 'badge-red' : 'badge-green') + '">' + escapeHtml(m.status) + '</span>' + predLabel + '</div>' +
        '<div class="score-inputs">' +
        '<input type="number" id="phome-' + m.id + '" placeholder="Local" min="0" max="50" value="' + homePred + '">' +
        '<span>-</span>' +
        '<input type="number" id="paway-' + m.id + '" placeholder="Visitante" min="0" max="50" value="' + awayPred + '">' +
        '</div>' +
        '<button class="secondary submit-btn" onclick="predictionsModule.makePrediction(\'' + m.id + '\',' + tournamentId + ')">Pronosticar</button>' +
        '</div>';
    });
    container.innerHTML = html;
    showAlert('auth-status', matches.length + ' partido(s) cargado(s).', 'success');
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

export async function makePrediction(matchId, tournamentId) {
  const home_score = parseInt(document.getElementById('phome-' + matchId).value) || 0;
  const away_score = parseInt(document.getElementById('paway-' + matchId).value) || 0;
  try {
    if (!isLoggedIn()) { showAlert('auth-status', 'Inicia sesion para pronosticar.', 'error'); return; }
    const d = await apiPost('/matches/' + matchId + '/predictions?tournament_id=' + tournamentId, { home_score, away_score });
    if (!d) { showAlert('auth-status', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    showAlert('auth-status', 'Pronostico guardado: ' + home_score + ' - ' + away_score + ' | Puntos: ' + (d.points_earned ?? '-'), 'success');
    loadMatches(tournamentId);
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

window.predictionsModule = { init, loadMatches, makePrediction };
