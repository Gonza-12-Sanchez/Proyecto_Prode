export function formatDate(isoString) {
  if (!isoString) return '-';
  return new Date(isoString).toLocaleString();
}

export function formatCurrency(n) {
  if (n === null || n === undefined) return '-';
  return '$' + Number(n).toLocaleString();
}

export function showAlert(containerId, message, type = 'info') {
  const el = document.getElementById(containerId);
  if (el) {
    el.innerHTML = '<div class="alert alert-' + type + '">' + message + '</div>';
  }
}

export function showTable(tableId, headers, rows) {
  const t = document.getElementById(tableId);
  if (!t) return;
  const thead = t.querySelector('thead');
  const tbody = t.querySelector('tbody');
  if (thead) {
    thead.innerHTML = '<tr>' + headers.map(h => '<th>' + h + '</th>').join('') + '</tr>';
  }
  if (tbody) {
    tbody.innerHTML = rows;
  }
  t.classList.remove('hidden');
}

export function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(String(str)));
  return div.innerHTML;
}
