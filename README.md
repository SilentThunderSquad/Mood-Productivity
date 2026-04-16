# 💬 MoodFlow — Mood-Based Productivity App

A productivity application that assesses your emotional state through a short daily check-in quiz and recommends tasks aligned with your mood.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 💬 **Daily Mood Check-In** | Quiz-based mood assessment (no camera required) |
| 🎯 **Smart Recommendations** | Tasks filtered by mood + difficulty + urgency |
| ✅ **Task Management** | Full CRUD with difficulty levels and deadlines |
| 📊 **Productivity Score** | Formula-based scoring with bonuses |
| 📈 **Charts & Analytics** | Chart.js visualisations for mood and tasks |
| 🎯 **Focus Mode** | Mood-adaptive Pomodoro-style timer |
| 🔐 **Auth** | JWT + bcrypt secure authentication |

---

## 🏗️ Architecture

```
Client (Browser)
    ↕  HTTP / REST
FastAPI Backend
    ↕
MongoDB Database
```

---

## 📁 Project Structure

```
mood-productivity-app/
│
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── database.py                # MongoDB connection
│   ├── auth.py                    # JWT + bcrypt auth
│   ├── mood_quiz_engine.py        # Quiz-based mood derivation
│   ├── recommendation_engine.py   # Mood-based task suggestions
│   ├── analytics_engine.py        # Productivity scoring + insights
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── routes/
│   │   ├── auth_routes.py         # /register /login /logout
│   │   ├── task_routes.py         # CRUD tasks
│   │   ├── mood_routes.py         # /mood-questions /assess-mood /mood-history
│   │   └── analytics_routes.py   # /productivity-score /mood-analytics /weekly-report
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── task_model.py
│   │   └── mood_model.py
│   │
│   └── utils/
│       ├── productivity_score.py
│       └── mood_analysis.py
│
└── frontend/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── tasks.html
    ├── mood-detection.html
    ├── focus-mode.html
    │
    ├── css/
    │   └── style.css              # Fully responsive dark UI
    │
    └── js/
        ├── auth.js                # Login/register/logout + shared utils
        ├── tasks.js               # Task CRUD operations
        ├── mood_detection.js      # Mood check-in helpers
        └── charts.js              # Dashboard + Chart.js
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.9+
- MongoDB (Community Edition)
- Modern browser (Chrome / Firefox recommended)

---

### 2. Install MongoDB

**macOS (Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Ubuntu/Debian:**
```bash
sudo apt install mongodb
sudo systemctl start mongodb
```

**Windows:**
Download from https://www.mongodb.com/try/download/community

---

### 3. Backend Setup

```bash
# Navigate to backend directory
cd mood-productivity-app/backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env if needed (MongoDB URI, SECRET_KEY)

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

The API will be available at: **http://localhost:8000**
API documentation (Swagger UI): **http://localhost:8000/docs**

---

### 4. Frontend Setup

The frontend is pure HTML/CSS/JS — no build step required.

**Option A: Serve via FastAPI (recommended)**
FastAPI automatically serves the frontend at **http://localhost:8000**

**Option B: Use VS Code Live Server extension**
Right-click login.html -> Open with Live Server

---

### 5. First Run

1. Open **http://localhost:8000**
2. Click **"Create one"** to register an account
3. Login to reach the dashboard
4. Go to **Check-In** -> Answer the short quiz -> Submit
5. View recommendations on the dashboard!

---

## 🔌 API Reference

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/register | Register new user |
| POST | /api/login | Login and receive JWT |
| POST | /api/logout | Clear auth cookie |
| GET | /api/me | Get current user |

### Mood Check-In
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/mood-questions | Get quiz questions |
| POST | /api/assess-mood | Submit answers and get mood result |
| GET | /api/mood-history | Get past mood records |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/task | Create task |
| GET | /api/tasks | Get all user tasks |
| PUT | /api/task/{id} | Update task |
| DELETE | /api/task/{id} | Delete task |
| PUT | /api/task/complete/{id} | Mark task as completed |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/productivity-score | Calculate score |
| GET | /api/mood-analytics | Mood distribution + insights |
| GET | /api/weekly-report | 7-day summary |

---

## 😊 Mood to Task Mapping

| Mood | Recommended Tasks |
|---|---|
| motivated 🚀 | Hard -> Medium |
| neutral 😐 | Medium -> Easy |
| tired 😴 | Easy only |
| stressed 😰 | Easy -> Medium |

---

## 📊 Productivity Score Formula

```
Base Score = (completed_tasks / total_tasks) x 100

Bonuses:
  +10 for each completed Hard task
  +5  for each task completed while in stressed mood

Final Score = Base Score + Total Bonuses  (capped at 150%)
```

---

## 🎨 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js 4.x |
| Backend | Python + FastAPI + Uvicorn |
| Database | MongoDB + PyMongo |
| Auth | JWT (python-jose) + bcrypt (passlib) |

---

## 🛠️ Troubleshooting

**MongoDB connection refused:**
```bash
# Check if MongoDB is running
mongosh --eval "db.runCommand({ connectionStatus: 1 })"
# Start it
sudo systemctl start mongod   # Linux
brew services start mongodb-community  # macOS
```

**CORS errors in browser:**
Make sure you're accessing the frontend through http://localhost:8000 (served by FastAPI), not a different port.

---

## 👥 Contributors

Built as an academic project demonstrating:
- Quiz-Based Mood Assessment
- Full-Stack Web Development (FastAPI + Vanilla JS)
- Data Analytics (Productivity Scoring + Mood Trends)
