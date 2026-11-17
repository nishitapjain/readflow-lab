"""Book-specific reading pace prediction."""

from datetime import timedelta
from math import ceil

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Book, ReadingLog
from app.schemas import PredictionOut
from app.time_utils import today_local


def predict_book_finish(db: Session, book: Book) -> PredictionOut:
    today = today_local()
    logged_total = (
        db.query(func.coalesce(func.sum(ReadingLog.pages_read), 0))
        .filter(ReadingLog.book_id == book.id)
        .scalar()
    )
    pages_remaining = max(book.total_pages - int(logged_total or 0), 0)

    if book.status == "finished" or pages_remaining == 0:
        return PredictionOut(
            book_id=book.id,
            status="finished",
            pages_remaining=0,
            average_daily_pages=0.0,
            days_left=0,
            expected_finish_date=today,
            message="This book is marked as finished.",
        )

    start_date = today - timedelta(days=6)
    daily_rows = (
        db.query(ReadingLog.log_date, func.sum(ReadingLog.pages_read))
        .filter(
            ReadingLog.book_id == book.id,
            ReadingLog.log_date >= start_date,
            ReadingLog.log_date <= today,
        )
        .group_by(ReadingLog.log_date)
        .all()
    )

    # The seven-day denominator includes days with no reading (zero pages).
    pages_in_window = sum(int(row[1]) for row in daily_rows)
    average = pages_in_window / 7

    # Require logs on at least three distinct dates in the seven-day window.
    if len(daily_rows) < 3 or average <= 0:
        return PredictionOut(
            book_id=book.id,
            status="not_enough_data",
            pages_remaining=pages_remaining,
            average_daily_pages=round(average, 2),
            days_left=None,
            expected_finish_date=None,
            message="Not enough data. Log reading on at least three different days in the last seven days.",
        )

    days_left = ceil(pages_remaining / average)
    return PredictionOut(
        book_id=book.id,
        status="ready",
        pages_remaining=pages_remaining,
        average_daily_pages=round(average, 2),
        days_left=days_left,
        expected_finish_date=today + timedelta(days=days_left),
        message="Prediction calculated from the last seven calendar days.",
    )
