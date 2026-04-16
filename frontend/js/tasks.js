/* tasks.js - Task management */

let allTasks  = [];
let curFilter = 'all';
let editingId = null;

async function loadTasks() {
  try {
    const res  = await apiFetch(`${API}/tasks`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to load tasks');
    allTasks = data.tasks || [];
    renderTasks();
  } catch (e) {
    if (e.message.includes('Session expired')) return;
    const el = document.getElementById('tasksList');
    if (el) el.innerHTML = `<div class="empty-state"><div class="es-icon">⚠️</div><p>${e.message}</p></div>`;
  }
}

function renderTasks() {
  const list = document.getElementById('tasksList');
  if (!list) return;

  let filtered = allTasks;
  if (curFilter === 'pending')   filtered = allTasks.filter(t => t.status === 'pending');
  else if (curFilter === 'completed') filtered = allTasks.filter(t => t.status === 'completed');
  else if (['Easy','Medium','Hard'].includes(curFilter))
    filtered = allTasks.filter(t => t.difficulty === curFilter);

  if (!filtered.length) {
    list.innerHTML = `<div class="empty-state"><div class="es-icon">📋</div><p>No tasks found. Add one to get started!</p></div>`;
    return;
  }

  list.innerHTML = [...filtered]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .map(t => renderTaskItem(t, { showComplete: true, showEdit: true, showDelete: true }))
    .join('');
}

function setFilter(f, btn) {
  curFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderTasks();
}

/* ── Modal ─────────────────────────────────────────────────── */
function openModal(task = null) {
  editingId = task ? task.id : null;
  document.getElementById('modalTitle').textContent    = task ? 'Edit Task' : 'Add New Task';
  document.getElementById('taskTitle').value           = task?.title       || '';
  document.getElementById('taskDesc').value            = task?.description || '';
  document.getElementById('taskDiff').value            = task?.difficulty  || 'Medium';
  document.getElementById('taskDeadline').value        = task?.deadline
    ? task.deadline.split('T')[0] : '';
  document.getElementById('taskModal').classList.add('open');
  document.getElementById('taskTitle').focus();
}

function closeModal() {
  document.getElementById('taskModal').classList.remove('open');
  editingId = null;
}

// Close modal on overlay click
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('taskModal');
  if (overlay) {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) closeModal();
    });
  }
});

async function saveTask() {
  const title    = document.getElementById('taskTitle').value.trim();
  const desc     = document.getElementById('taskDesc').value.trim();
  const diff     = document.getElementById('taskDiff').value;
  const deadline = document.getElementById('taskDeadline').value;

  if (!title) { showToast('Task title is required', 'error'); return; }

  const body = { title, description: desc, difficulty: diff, deadline: deadline || null };

  try {
    let res;
    if (editingId) {
      res = await apiFetch(`${API}/task/${editingId}`, {
        method: 'PUT', body: JSON.stringify(body),
      });
    } else {
      res = await apiFetch(`${API}/task`, {
        method: 'POST', body: JSON.stringify(body),
      });
    }
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Save failed');

    showToast(editingId ? '✏️ Task updated!' : '✅ Task created!', 'success');
    closeModal();
    loadTasks();
  } catch (e) {
    if (!e.message.includes('Session expired')) showToast(e.message, 'error');
  }
}

function editTask(id) {
  const task = allTasks.find(t => t.id === id);
  if (task) openModal(task);
}

async function deleteTask(id) {
  if (!confirm('Delete this task?')) return;
  try {
    const res  = await apiFetch(`${API}/task/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Delete failed');
    allTasks = allTasks.filter(t => t.id !== id);
    renderTasks();
    showToast('🗑️ Task deleted', 'success');
  } catch (e) {
    if (!e.message.includes('Session expired')) showToast(e.message, 'error');
  }
}

async function markTaskDone(id) {
  try {
    const res  = await apiFetch(`${API}/task/complete/${id}`, { method: 'PUT' });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to complete task');
    const task = allTasks.find(t => t.id === id);
    if (task) task.status = 'completed';
    renderTasks();
    showToast('🎉 Task completed!', 'success');
  } catch (e) {
    if (!e.message.includes('Session expired')) showToast(e.message, 'error');
  }
}
