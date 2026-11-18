export const API = 'http://localhost:8002/api/v1';
const TOKEN_KEY = 'prode_token';

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function isLoggedIn() {
  const t = getToken();
  return t !== null && !isTokenExpired(t);
}

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  } catch {
    return true;
  }
}

export function authHeaders() {
  const h = { 'Content-Type': 'application/json' };
  const t = getToken();
  if (t) {
    if (isTokenExpired(t)) {
      setToken(null);
    } else {
      h['Authorization'] = 'Bearer ' + t;
    }
  }
  return h;
}

async function request(method, endpoint, body) {
  const opts = {
    method,
    headers: authHeaders(),
  };
  if (body !== undefined) opts.body = JSON.stringify(body);
  try {
    const r = await fetch(API + endpoint, opts);
    if (r.status === 401) {
      setToken(null);
      return null;
    }
    if (r.status === 404) {
      return null;
    }
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Error');
    return d;
  } catch (e) {
    throw e;
  }
}

export function apiPost(endpoint, body) {
  return request('POST', endpoint, body);
}

export function apiGet(endpoint) {
  return request('GET', endpoint);
}
