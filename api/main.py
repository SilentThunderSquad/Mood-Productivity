"""
main.py - FastAPI application entry point
Run with:  uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import pathlib
import sys

# ── Locate directories ────────────────────────────────────────────────────────
BASE_DIR     = pathlib.Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "static"

print(f"\n{'='*55}")
print(f"  App Base  : {BASE_DIR}")
print(f"  Static UI : {FRONTEND_DIR}")
print(f"  UI Assets Exist: {FRONTEND_DIR.is_dir()}")
print(f"{'='*55}\n")

# ── Import routers ────────────────────────────────────────────────────────────
from routes.auth_routes      import router as auth_router
from routes.task_routes      import router as task_router
from routes.mood_routes      import router as mood_router
from routes.analytics_routes import router as analytics_router

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="MoodFlow API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API routes ────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(mood_router)
app.include_router(analytics_router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Mood Productivity API is running ✓", "docs": "/api/docs"}

# ── Static assets (css + js) ──────────────────────────────────────────────────
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js",  StaticFiles(directory=str(FRONTEND_DIR / "js")),  name="js")

# ── HTML page routes ──────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "login.html"))

@app.get("/login")
@app.get("/login.html")
async def page_login():
    return FileResponse(str(FRONTEND_DIR / "login.html"))

@app.get("/register")
@app.get("/register.html")
async def page_register():
    return FileResponse(str(FRONTEND_DIR / "register.html"))

@app.get("/dashboard")
@app.get("/dashboard.html")
async def page_dashboard():
    return FileResponse(str(FRONTEND_DIR / "dashboard.html"))

@app.get("/tasks")
@app.get("/tasks.html")
async def page_tasks():
    return FileResponse(str(FRONTEND_DIR / "tasks.html"))

@app.get("/mood-detection")
@app.get("/mood-detection.html")
async def page_mood():
    return FileResponse(str(FRONTEND_DIR / "mood-detection.html"))

@app.get("/focus-mode")
@app.get("/focus-mode.html")
async def page_focus():
    return FileResponse(str(FRONTEND_DIR / "focus-mode.html"))

# ── Launch ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
