/* charts.js - Dashboard data loading + Chart.js */

Chart.defaults.color = '#7b8ab0';
Chart.defaults.borderColor = 'rgba(99,120,200,0.12)';

const MOOD_COLORS = { motivated:'#22c55e', neutral:'#60a5fa', tired:'#f59e0b', stressed:'#f87171' };
const MOOD_ICONS  = { motivated:'🚀', neutral:'😐', tired:'😴', stressed:'😰' };

async function initDashboard() {
  const user = getUser();
  const av   = document.getElementById('navAvatar');
  if (av && user.name) av.textContent = user.name.charAt(0).toUpperCase();

  await Promise.all([loadMoodBanner(), loadScoreData(), loadTasksData(), loadAnalytics()]);
}

async function loadMoodBanner() {
  try {
    const res  = await apiFetch(`${API}/mood-history`);
    const data = await res.json();
    const moods = data.moods || [];
    if (moods.length) {
      const m = moods[0].detected_mood || 'neutral';
      document.getElementById('moodEmoji').textContent = MOOD_ICONS[m] || '😐';
      document.getElementById('moodLabel').textContent = 'Current Mood: ' + m.charAt(0).toUpperCase() + m.slice(1);
      document.getElementById('moodDesc').textContent  = `Last check-in: ${new Date(moods[0].timestamp).toLocaleString()}`;
    }
  } catch {}
}

async function loadScoreData() {
  try {
    const res  = await apiFetch(`${API}/productivity-score`);
    const data = await res.json();
    document.getElementById('scoreValue').textContent = data.score + '%';
    document.getElementById('scoreBase').textContent  = `Base: ${data.base}% + ${data.bonuses} bonus pts`;
    document.getElementById('ringScore').textContent  = Math.round(data.score);
    document.getElementById('ringDetail').textContent = `${data.completed} of ${data.total} tasks done`;
    const circ = 339.3;
    setTimeout(() => {
      document.getElementById('scoreArc').style.strokeDashoffset =
        circ - (Math.min(data.score, 100) / 100) * circ;
    }, 200);
  } catch {}
}

async function loadTasksData() {
  try {
    const res   = await apiFetch(`${API}/tasks`);
    const data  = await res.json();
    const tasks = data.tasks || [];
    const pending   = tasks.filter(t => t.status === 'pending');
    const completed = tasks.filter(t => t.status === 'completed');

    document.getElementById('totalTasks').textContent     = tasks.length;
    document.getElementById('completedTasks').textContent = `${completed.length} completed`;
    document.getElementById('pendingTasks').textContent   = pending.length;

    const recList = document.getElementById('recentTasksList');
    const recent  = [...tasks].sort((a,b) => new Date(b.created_at||0)-new Date(a.created_at||0)).slice(0,5);
    recList.innerHTML = recent.length
      ? recent.map(t => renderTaskItem(t)).join('')
      : '<div class="empty-state"><div class="es-icon">📋</div><p>No tasks yet. <a href="tasks.html" style="color:var(--accent)">Add one →</a></p></div>';

    buildTaskChart(completed.length, pending.length);

    const mood  = localStorage.getItem('mf_mood') || 'neutral';
    const prefs = ({motivated:['Hard','Medium'],neutral:['Medium','Easy'],tired:['Easy'],stressed:['Easy','Medium']})[mood] || ['Medium'];
    const rec   = pending.filter(t => prefs.includes(t.difficulty)).slice(0,4);

    document.getElementById('recBadge').textContent = (MOOD_ICONS[mood]||'') + ' ' + mood.charAt(0).toUpperCase()+mood.slice(1);
    document.getElementById('recTasksList').innerHTML = rec.length
      ? rec.map(t => renderTaskItem(t)).join('')
      : '<div class="empty-state"><div class="es-icon">💬</div><p><a href="mood-detection.html" style="color:var(--accent)">Do your daily check-in</a> for recommendations</p></div>';

    const tipEl = document.getElementById('recTip');
    if (tipEl && mood) tipEl.style.display = 'flex';
  } catch {}
}

async function loadAnalytics() {
  try {
    const res  = await apiFetch(`${API}/mood-analytics`);
    const data = await res.json();

    document.getElementById('moodDetections').textContent = data.total_detections || 0;
    document.getElementById('mostFreqMood').textContent   = `Most frequent: ${data.most_frequent_mood || '—'}`;

    const insightsList = document.getElementById('insightsList');
    const icons = ['🧠','💡','📊','⚡','🎯'];
    insightsList.innerHTML = (data.insights||[]).length
      ? data.insights.map((ins,i) => `<div class="insight-item"><span class="insight-icon">${icons[i%icons.length]}</span><span>${ins}</span></div>`).join('')
      : `<div class="insight-item"><span class="insight-icon">💬</span><span><a href="mood-detection.html" style="color:var(--accent)">Complete your daily check-in</a> to unlock AI insights!</span></div>`;

    if (data.daily_trend) buildMoodChart(data.daily_trend);
  } catch {}
}

function buildMoodChart(dailyTrend) {
  const labels   = Object.keys(dailyTrend).sort();
  const datasets = ['motivated','neutral','tired','stressed'].map(mood => ({
    label: mood.charAt(0).toUpperCase()+mood.slice(1),
    data:  labels.map(d => dailyTrend[d]?.[mood]||0),
    borderColor: MOOD_COLORS[mood], backgroundColor: MOOD_COLORS[mood]+'22',
    borderWidth:2, pointRadius:4, tension:0.4, fill:false,
  }));
  const ctx = document.getElementById('moodChart');
  if (!ctx) return;
  new Chart(ctx, {
    type:'line', data:{ labels: labels.map(d => new Date(d).toLocaleDateString('en-GB',{weekday:'short'})), datasets },
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ position:'bottom', labels:{ boxWidth:10, padding:12, font:{size:11} } } },
      scales:{ x:{grid:{color:'rgba(99,120,200,.08)'}}, y:{beginAtZero:true, ticks:{stepSize:1}, grid:{color:'rgba(99,120,200,.08)'}} } },
  });
}

function buildTaskChart(completed, pending) {
  const ctx = document.getElementById('taskChart');
  if (!ctx) return;
  new Chart(ctx, {
    type:'doughnut',
    data:{ labels:['Completed','Pending'],
      datasets:[{ data:[completed,pending], backgroundColor:['#22c55e33','#f59e0b33'], borderColor:['#22c55e','#f59e0b'], borderWidth:2, hoverOffset:8 }] },
    options:{ responsive:true, maintainAspectRatio:false, cutout:'68%',
      plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12, padding:14, font:{size:12} } } } },
  });
}
