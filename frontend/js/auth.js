/* auth.js - Authentication & shared utilities */

const API = 'http://localhost:8000/api';

/* ── Token helpers ─────────────────────────────────────────── */
function getToken()   { return localStorage.getItem('mf_token') || ''; }
function setToken(t)  { localStorage.setItem('mf_token', t); }
function clearAuth()  {
  localStorage.removeItem('mf_token');
  localStorage.removeItem('mf_user');
  localStorage.removeItem('mf_mood');
}
function getUser()    {
  try { return JSON.parse(localStorage.getItem('mf_user') || '{}'); }
  catch { return {}; }
}
function setUser(u)   { localStorage.setItem('mf_user', JSON.stringify(u)); }

/* ── Auth headers — ALWAYS include Bearer token ────────────── */
function authHeaders() {
  const token = getToken();
  return {
    'Content-Type':  'application/json',
    'Authorization': `Bearer ${token}`,
  };
}

/* ── Central fetch wrapper — auto-redirects on 401 ─────────── */
async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });

  // Auto logout on 401
  if (res.status === 401) {
    clearAuth();
    window.location.href = 'login.html';
    throw new Error('Session expired. Please log in again.');
  }
  return res;
}

/* ── Require auth guard ─────────────────────────────────────── */
function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = 'login.html';
    return;
  }
  // Set nav avatar
  const user = getUser();
  const av   = document.getElementById('navAvatar');
  if (av && user.name) av.textContent = user.name.charAt(0).toUpperCase();
}

/* ── Login ─────────────────────────────────────────────────── */
async function doLogin() {
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  if (!email || !password) { showAlert('Please fill in all fields.', 'error'); return; }

  const btn = document.getElementById('loginBtn');
  if (btn) { btn.textContent = 'Signing in...'; btn.disabled = true; }

  try {
    const res  = await fetch(`${API}/login`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');

    setToken(data.token);
    setUser(data.user);
    window.location.href = 'dashboard.html';
  } catch (e) {
    showAlert(e.message, 'error');
    if (btn) { btn.textContent = 'Sign In →'; btn.disabled = false; }
  }
}

/* ── Register ──────────────────────────────────────────────── */
async function doRegister() {
  const name     = document.getElementById('name').value.trim();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  if (!name || !email || !password) { showAlert('Please fill in all fields.', 'error'); return; }
  if (password.length < 6)          { showAlert('Password must be at least 6 characters.', 'error'); return; }

  const btn = document.querySelector('.btn-primary');
  if (btn) { btn.textContent = 'Creating account...'; btn.disabled = true; }

  try {
    const res  = await fetch(`${API}/register`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ name, email, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');

    setToken(data.token);
    setUser(data.user);
    showAlert('Account created! Redirecting...', 'success');
    setTimeout(() => { window.location.href = 'dashboard.html'; }, 700);
  } catch (e) {
    showAlert(e.message, 'error');
    if (btn) { btn.textContent = 'Create Account →'; btn.disabled = false; }
  }
}

/* ── Logout ────────────────────────────────────────────────── */
async function doLogout() {
  try {
    await fetch(`${API}/logout`, { method: 'POST', headers: authHeaders() });
  } catch {}
  clearAuth();
  window.location.href = 'login.html';
}

/* ── Alert (auth pages) ────────────────────────────────────── */
function showAlert(msg, type = 'error') {
  const box = document.getElementById('alertBox');
  if (!box) return;
  box.textContent  = msg;
  box.className    = `alert alert-${type}`;
  box.style.display = 'block';
  setTimeout(() => { box.style.display = 'none'; }, 5000);
}

/* ── Toast (app pages) ─────────────────────────────────────── */
function showToast(msg, type = 'success') {
  const c = document.getElementById('toastContainer');
  if (!c) return;
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.innerHTML = `<span>${type === 'success' ? '✅' : '❌'}</span><span>${msg}</span>`;
  c.appendChild(t);
  setTimeout(() => {
    t.style.transition = 'all .3s';
    t.style.opacity    = '0';
    t.style.transform  = 'translateX(110%)';
    setTimeout(() => t.remove(), 320);
  }, 3200);
}

/* ── Mobile menu ───────────────────────────────────────────── */
function toggleMobileMenu() {
  document.getElementById('mobileMenu')?.classList.toggle('open');
}

/* ── Shared task renderer ──────────────────────────────────── */
function renderTaskItem(task, opts = {}) {
  const { showComplete = true, showEdit = false, showDelete = false } = opts;
  const isDone   = task.status === 'completed';
  const deadline = task.deadline ? new Date(task.deadline) : null;
  const now      = new Date();
  const isUrgent = deadline && !isDone && (deadline - now) / 86400000 <= 2;
  const dlStr    = deadline
    ? deadline.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })
    : '';

  return `
  <div class="task-item ${isDone ? 'completed' : ''}" id="task-${task.id}">
    <div class="task-check ${isDone ? 'done' : ''}"
         onclick="${showComplete && !isDone ? `markTaskDone('${task.id}')` : ''}"></div>
    <div class="task-info">
      <div class="task-title">${escHtml(task.title)}</div>
      <div class="task-meta">
        <span class="badge-diff diff-${task.difficulty}">${task.difficulty}</span>
        <span class="badge-status status-${task.status}">${task.status}</span>
        ${dlStr ? `<span class="task-deadline ${isUrgent ? 'urgent' : ''}">📅 ${dlStr}${isUrgent ? ' ⚠️' : ''}</span>` : ''}
      </div>
    </div>
    <div class="task-actions">
      ${showEdit   ? `<button class="btn-icon"        onclick="editTask('${task.id}')"   title="Edit">✏️</button>` : ''}
      ${showDelete ? `<button class="btn-icon delete" onclick="deleteTask('${task.id}')" title="Delete">🗑️</button>` : ''}
    </div>
  </div>`;
}

function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

/* ── Enter key on login/register ───────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  const isLogin    = !!document.getElementById('loginBtn');
  const isRegister = !!document.getElementById('name');
  document.addEventListener('keydown', e => {
    if (e.key !== 'Enter') return;
    const tag = document.activeElement?.tagName;
    if (tag === 'TEXTAREA' || tag === 'SELECT' || tag === 'BUTTON') return;
    if (isLogin)    doLogin();
    if (isRegister) doRegister();
  });
});
