from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI()

DB_PATH = "reviews.db"

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

# --- Models ---
class ReviewIn(BaseModel):
    text: str

class ReviewOut(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str

# --- Sentiment analysis ---
def analyze_sentiment(text: str) -> str:
    text_lower = text.lower()
    if any(word in text_lower for word in ["хорош", "люблю"]):
        return "positive"
    if any(word in text_lower for word in ["плохо", "ненавиж"]):
        return "negative"
    return "neutral"

# --- Endpoints ---
@app.post("/reviews", response_model=ReviewOut)
def create_review(review: ReviewIn):
    sentiment = analyze_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
        (review.text, sentiment, created_at),
    )
    review_id = c.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": review_id,
        "text": review.text,
        "sentiment": sentiment,
        "created_at": created_at,
    }

@app.get("/reviews", response_model=List[ReviewOut])
def get_reviews(sentiment: Optional[str] = Query(None)):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if sentiment:
        c.execute(
            "SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ? ORDER BY id",
            (sentiment,),
        )
    else:
        c.execute(
            "SELECT id, text, sentiment, created_at FROM reviews ORDER BY id"
        )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "text": row[1],
            "sentiment": row[2],
            "created_at": row[3],
        }
        for row in rows
    ]