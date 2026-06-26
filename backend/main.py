"""
NewsFeed AI — FastAPI Backend

Endpoints:
  GET /              Health check
  GET /generate      Manually trigger one article generation
  GET /api/news      All articles (newest first)
  GET /api/news/{id} Single article by ID
  GET /images/{path} Serve locally generated AI images
"""

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from workflows.news_workflow import run_news_workflow
from scheduler.scheduler import start_scheduler

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(title="NewsFeed AI API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
NEWS_FILE = OUTPUT_DIR / "news.json"
IMAGES_DIR = OUTPUT_DIR / "images"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Serve AI-generated images at /images/*
app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    start_scheduler()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_news() -> list:
    if not NEWS_FILE.exists():
        return []
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def health():
    return {"status": "ok", "message": "NewsFeed AI Running"}


@app.get("/generate")
def generate_news():
    """Manually trigger one article generation cycle."""
    result = run_news_workflow()
    if result:
        return {"status": "success", "article": result}
    return {"status": "no_new_article"}


# ─── /api/news ───────────────────────────────────────────────────────────────

@app.get("/api/news")
def get_all_news():
    """Return all saved articles (newest first)."""
    return _load_news()


@app.get("/api/news/{article_id}")
def get_news_by_id(article_id: int):
    """Return a single article by its ID."""
    news = _load_news()
    for item in news:
        if item.get("id") == article_id:
            return item
    raise HTTPException(status_code=404, detail="Article not found")


# ─── Legacy routes (backward compat) ─────────────────────────────────────────

@app.get("/news")
def get_all_news_legacy():
    return _load_news()


@app.get("/news/latest")
def latest_news():
    news = _load_news()
    return news[:4]