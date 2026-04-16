# 💬 MoodFlow — Mood-Based Productivity App

A premium "Neural Dark" productivity application that assesses your emotional state through a short daily check-in quiz and recommends tasks aligned with your mood. Built for speed and visual excellence.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 💬 **Daily Mood Check-In** | AI-driven quiz assessment with instant mood derivation |
| 🎯 **Smart Recommendations** | Tasks filtered dynamically by mood, difficulty, and urgency |
| ✅ **Task Management** | Full CRUD with difficulty levels, deadlines, and glassmorphic UI |
| 📊 **Productivity Score** | Formula-based progressive scoring with mood bonuses |
| 📈 **Advanced Analytics** | Real-time Chart.js visualisations for mood trends and completion |
| 🎯 **Focus Mode** | Premium Pomodoro-style timer with mood-adaptive durations |
| 🔐 **Secure Auth** | Supabase-powered JWT + bcrypt authentication |

---

## 🏗️ Architecture

```
Client (Browser / Vanilla JS)
    ↕  HTTPS / REST
FastAPI Backend (Python)
    ↕
Supabase (PostgreSQL + Auth)
```

---

## 📁 Project Structure

```
mood-productivity-app/
│
├── backend/
│   ├── main.py                    # FastAPI entry point & Routing
│   ├── database.py                # Supabase Connection Manager
│   ├── routes/                    # API Route Handlers
│   ├── models/                    # Data Schemas
│   ├── requirements.txt           # Python Dependencies
│   └── .env                       # Cloud Credentials
│
├── frontend/                  # Static assets
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── tasks.html
│   ├── mood-detection.html
│   ├── focus-mode.html
│   ├── css/style.css              # Premium "Neural Dark" Design System
│   └── js/                        # Shared Logic (Auth, Charts, Tasks)
│
├── vercel.json                    # Vercel Deployment Config
└── DEPLOY.md                      # Cloud Hosting Guide
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- **Python 3.9+**
- **Supabase Account** (Free tier works perfectly)
- A modern browser

### 2. Database Setup (Supabase)
1. Create a new project on [Supabase](https://supabase.com).
2. Grab your **Project URL** and **API Key** from the Supabase Project Settings.
3. Add these to your `.env` file in the `backend/` folder.

### 3. Local Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (.env)
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-anon-key"
SECRET_KEY="your-jwt-secret"

# Start the server
uvicorn main:app --reload
```

The app will be available locally at: **http://localhost:8000**

---

## 🚀 Deployment (Vercel)

This project is optimized for **Vercel**. 
1. Push this project to GitHub.
2. Link the repository to Vercel.
3. Add your `.env` variables in the Vercel Dashboard.

See [DEPLOY.md](DEPLOY.md) for a detailed walkthrough.

---

## 🎨 Design Aesthetic
MoodFlow uses a custom **"Neural Dark"** design system featuring:
- **Glassmorphism**: Backdrop blur and soft glows on all major components.
- **Vibrant Gradients**: Luminous mood-based colors (Indigo, Emerald, Violet).
- **Responsive Simplicity**: Built with Vanilla CSS for maximum performance.

---

## 📊 Productivity Score Formula

```
Base Score = (completed_tasks / total_tasks) x 100

Bonuses:
  +10 for each completed Hard task
  +5  for each task completed while in a "Stressed" mood

Final Score = Base Score + Total Bonuses (Capped at 150%)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, Vanilla JavaScript, CSS3 (Custom Design System) |
| **Charts** | Chart.js 4.x |
| **Backend** | Python 3.x, FastAPI, Uvicorn |
| **Database** | Supabase (PostgreSQL) |
| **Deployment** | Vercel (Serverless Functions) |

---

## 👥 Contributors

Built with focus on AI-driven productivity and modern web aesthetics.
