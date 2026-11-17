"""Reading pace, streak, and heatmap endpoints."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book, ReadingLog, User
from app.schemas import HeatmapDay, PredictionOut, StreakOut
from app.services.pace import predict_book_finish
from app.services.streak import get_streak_summary
from app.time_utils import today_local

router = APIRouter(tags=["Reading analytics"])


@router.get("/books/{book_id}/prediction", response_model=PredictionOut)
def get_book_prediction(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    return predict_book_finish(db, book)


@router.get("/users/{user_id}/streak", response_model=StreakOut)
def get_user_streak(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return get_streak_summary(db, user)


@router.get("/users/{user_id}/heatmap", response_model=list[HeatmapDay])
def get_user_heatmap(
    user_id: int,
    days: int = Query(default=90, ge=1, le=365),
    db: Session = Depends(get_db),
):
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found.")

    today = today_local()
    start_date = today - timedelta(days=days - 1)
    rows = (
        db.query(ReadingLog.log_date, func.sum(ReadingLog.pages_read))
        .filter(
            ReadingLog.user_id == user_id,
            ReadingLog.log_date >= start_date,
            ReadingLog.log_date <= today,
        )
        .group_by(ReadingLog.log_date)
        .all()
    )
    totals = {day: int(total) for day, total in rows}

    # Return every date, including dates with zero pages, to simplify the UI.
    return [
        {"date": start_date + timedelta(days=offset),
         "pages_read": totals.get(start_date + timedelta(days=offset), 0)}
        for offset in range(days)
    ]
