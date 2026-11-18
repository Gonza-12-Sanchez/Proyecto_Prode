import { apiPost, apiGet, setToken, getToken, isLoggedIn, authHeaders } from './api.js';
import { showAlert, escapeHtml } from './utils.js';

export function init() {
  document.getElementById('btn-register').addEventListener('click', register);
  document.getElementById('btn-login').addEventListener('click', login);
  document.getElementById('btn-load-profile').addEventListener('click', loadProfile);

  if (isLoggedIn()) {
    loadProfile();
  }
}

export async function loadProfile() {
  const d = await apiGet('/auth/me');
  if (!d) {
    setToken(null);
    showAlert('profile-data', '❌ Sesión expirada. Inicia sesión de nuevo.', 'error');
    window.App && window.App.updateAuthUI();
    return;
  }
  const el = document.getElementById('profile-data');
  if (el) {
    el.innerHTML = '<div class="profile-card">' +
      '<div class="stat-row"><span class="stat-label">Username:</span><span class="stat-value">' + escapeHtml(d.username) + '</span></div>' +
      '<div class="stat-row"><span class="stat-label">Email:</span><span class="stat-value">' + escapeHtml(d.email) + '</span></div>' +
      '<div class="stat-row"><span class="stat-label">Torneos jugados:</span><span class="stat-value">' + d.tournaments_played + '</span></div>' +
      '<div class="stat-row"><span class="stat-label">Predicciones totales:</span><span class="stat-value">' + d.total_predictions + '</span></div>' +
      '<div class="stat-row"><span class="stat-label">Precisión:</span><span class="stat-value">' + d.accuracy_percentage + '%</span></div>' +
      '<div class="stat-row"><span class="stat-label">Racha actual:</span><span class="stat-value">' + d.current_streak + '</span></div>' +
      '<div class="stat-row"><span class="stat-label">Mejor puesto:</span><span class="stat-value">' + (d.best_finish ?? '-') + '</span></div>' +
      '</div>';
  }
}

export async function register() {
  const email = document.getElementById('auth-email').value.trim();
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value;
  if (!email || !username || !password) {
    showAlert('auth-status', 'Completa todos los campos', 'error');
    return;
  }
  try {
    const d = await apiPost('/auth/register', { email, username, password });
    setToken(null);
    showAlert('auth-status', '✅ Registro exitoso: ' + escapeHtml(d.username) + ' (id: ' + d.id + '). Inicia sesión.', 'success');
    window.App && window.App.updateAuthUI();
  } catch (e) {
    showAlert('auth-status', '❌ ' + e.message, 'error');
  }
}

export async function login() {
  const email = document.getElementById('auth-email').value.trim();
  const password = document.getElementById('auth-password').value;
  if (!email || !password) {
    showAlert('auth-status', 'Completa email y password', 'error');
    return;
  }
  try {
    const d = await apiPost('/auth/login', { email, password });
    setToken(d.access_token);
    showAlert('auth-status', '✅ Logueado. Token guardado.', 'success');
    window.App && window.App.updateAuthUI();
    loadProfile();
  } catch (e) {
    showAlert('auth-status', '❌ ' + e.message, 'error');
  }
}

export function updateUI() {
  const profileCard = document.querySelector('#tab-auth .card:nth-child(2)');
  const btnProfile = document.getElementById('btn-load-profile');
  if (isLoggedIn()) {
    if (btnProfile) btnProfile.textContent = 'Recargar Perfil';
    loadProfile();
  } else {
    const el = document.getElementById('profile-data');
    if (el) el.innerHTML = '';
    if (btnProfile) btnProfile.textContent = 'Cargar Mi Perfil';
  }
}

window.authModule = { init, register, login, loadProfile, updateUI };
