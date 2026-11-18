import { apiPost, apiGet, isLoggedIn } from './api.js';
import { showAlert, showTable, escapeHtml } from './utils.js';

export function init() {
  document.getElementById('btn-create-tournament').addEventListener('click', create);
  document.getElementById('btn-join-tournament').addEventListener('click', join);
  document.getElementById('btn-load-tournaments').addEventListener('click', load);
  if (isLoggedIn()) {
    populateSelects();
    loadLeaguesSelect();
  }
}

async function loadLeaguesSelect() {
  try {
    const leagues = await apiGet('/leagues');
    if (!leagues) return;
    const sel = document.getElementById('tourn-league-id');
    if (!sel) return;
    while (sel.options.length > 0) sel.remove(0);
    leagues.forEach(l => {
      const opt = document.createElement('option');
      opt.value = l.id;
      opt.textContent = l.name + (l.country ? ' (' + l.country + ')' : '');
      sel.appendChild(opt);
    });
  } catch (e) {
    console.warn('No se pudieron cargar las ligas:', e);
  }
}

export async function create() {
  const name = document.getElementById('tourn-name').value.trim();
  const league_id = parseInt(document.getElementById('tourn-league-id').value);
  const max_participants = parseInt(document.getElementById('tourn-max').value);
  if (!name || !league_id || !max_participants) {
    showAlert('auth-status', 'Completa todos los campos', 'error');
    return;
  }
  try {
    const d = await apiPost('/tournaments', { name, league_id, max_participants });
    if (!d) { showAlert('auth-status', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    showAlert('auth-status', 'Torneo creado: ' + escapeHtml(d.name) + ' | Codigo: ' + escapeHtml(d.invite_code), 'success');
    load();
    populateSelects();
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

export async function join() {
  const code = document.getElementById('join-code').value.trim();
  if (!code || code.length !== 8) {
    showAlert('auth-status', 'Codigo de 8 caracteres', 'error');
    return;
  }
  try {
    const d = await apiPost('/tournaments/join-by-code', { invite_code: code });
    if (!d) { showAlert('auth-status', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    showAlert('auth-status', 'Unido al torneo: ' + escapeHtml(d.name), 'success');
    load();
    populateSelects();
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

export async function load() {
  try {
    if (!isLoggedIn()) { showAlert('auth-status', 'Inicia sesion para ver torneos.', 'error'); return; }
    const tournaments = await apiGet('/tournaments');
    if (!tournaments) { showAlert('auth-status', 'Sesion expirada. Inicia sesion.', 'error'); return; }
    if (tournaments.length === 0) {
      showTable('tournaments-table', ['ID', 'Nombre', 'Liga', 'Estado', 'Invitacion', 'Accion'], '');
      showAlert('auth-status', 'No hay torneos creados aun.', 'info');
      return;
    }
    const headers = ['ID', 'Nombre', 'Liga', 'Estado', 'Invitacion', 'Accion'];
    const rows = tournaments.map(t => {
      const shortId = t.id.substring(0, 8) + '...';
      return '<tr><td>' + shortId + '</td><td>' + escapeHtml(t.name) + '</td><td>' + escapeHtml(String(t.league_id)) + '</td><td><span class="badge badge-blue">' + escapeHtml(t.status) + '</span></td><td>' + escapeHtml(t.invite_code) + '</td><td><button class="secondary" onclick="window.viewTournamentDetail(\'' + t.id + '\')">Ver</button></td></tr>';
    }).join('');
    showTable('tournaments-table', headers, rows);
    showAlert('auth-status', tournaments.length + ' torneo(s) cargado(s).', 'success');
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

export async function viewDetail(tournamentId) {
  try {
    if (!isLoggedIn()) { showAlert('auth-status', 'Inicia sesion.', 'error'); return; }
    const t = await apiGet('/tournaments/' + tournamentId);
    if (!t) { showAlert('auth-status', 'No se encontro el torneo.', 'error'); return; }
    let html = '<div class="card"><h3>' + escapeHtml(t.name) + '</h3><p>Liga: ' + escapeHtml(String(t.league_id)) + ' | Estado: <span class="badge badge-blue">' + escapeHtml(t.status) + '</span> | Invitacion: ' + escapeHtml(t.invite_code) + '</p></div>';

    const mr = await apiGet('/tournaments/' + tournamentId + '/matches?next_days=7');
    if (mr && mr.length > 0) {
      html += '<h4 style="color:#58a6ff;margin-top:12px;">Partidos</h4><table><thead><tr><th>Equipo Local</th><th>Equipo Visitante</th><th>Hora</th><th>Status</th></tr></thead><tbody>';
      mr.forEach(m => {
        html += '<tr><td>' + escapeHtml(m.home_team) + '</td><td>' + escapeHtml(m.away_team) + '</td><td>' + formatDate(m.start_time) + '</td><td><span class="badge ' + (m.status === 'FT' ? 'badge-red' : 'badge-green') + '">' + escapeHtml(m.status) + '</span></td></tr>';
      });
      html += '</tbody></table>';
    } else {
      html += '<p class="status-info">Sin partidos en los proximos 7 dias.</p>';
    }
    document.getElementById('profile-data').innerHTML = html;
    showAlert('auth-status', 'Detalle del torneo cargado: ' + escapeHtml(t.name), 'success');
  } catch (e) {
    showAlert('auth-status', e.message, 'error');
  }
}

export function populateSelects() {
  if (!isLoggedIn()) return;
  apiGet('/tournaments').then(tournaments => {
    if (!tournaments) return;
    ['predict-tournament', 'lb-tournament'].forEach(selId => {
      const sel = document.getElementById(selId);
      if (!sel) return;
      const current = sel.value;
      while (sel.options.length > 1) sel.remove(1);
      tournaments.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.id;
        opt.textContent = t.name + ' (' + t.league_id + ')';
        sel.appendChild(opt);
      });
      if (current) sel.value = current;
    });
  }).catch(() => {});
}

function formatDate(isoString) {
  if (!isoString) return '-';
  return new Date(isoString).toLocaleString();
}

window.viewTournamentDetail = viewDetail;
