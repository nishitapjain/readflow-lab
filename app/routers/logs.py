"""Reading-session logging and per-book history endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book, ReadingLog, User
from app.schemas import ReadingLogCreate, ReadingLogOut
from app.services.badges import award_eligible_badges
from app.time_utils import today_local

router = APIRouter(tags=["Reading logs"])


@router.post("/logs", response_model=ReadingLogOut, status_code=status.HTTP_201_CREATED)
def create_reading_log(payload: ReadingLogCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    book = db.get(Book, payload.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    if book.user_id != user.id:
        raise HTTPException(status_code=400, detail="This book does not belong to the specified user.")

    log_date = payload.log_date or today_local()
    if log_date > today_local():
        raise HTTPException(status_code=400, detail="Reading logs cannot be dated in the future.")
    if book.status == "finished":
        raise HTTPException(status_code=400, detail="Cannot add a reading log to a finished book.")

    already_logged = (
        db.query(func.coalesce(func.sum(ReadingLog.pages_read), 0))
        .filter(ReadingLog.book_id == book.id)
        .scalar()
    )
    new_total = int(already_logged or 0) + payload.pages_read
    if new_total > book.total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"This log would exceed the book's total page count ({book.total_pages}).",
        )

    log = ReadingLog(
        user_id=user.id,
        book_id=book.id,
        pages_read=payload.pages_read,
        log_date=log_date,
    )
    db.add(log)
    db.flush()

    # Automatically mark a book finished when its complete page count is logged.
    if new_total == book.total_pages:
        book.status = "finished"
        book.finished_on = log_date

    # Badge eligibility is based on the user's longest historical streak.
    award_eligible_badges(db, user)
    db.commit()
    db.refresh(log)
    return log


@router.get("/books/{book_id}/logs", response_model=list[ReadingLogOut])
def get_book_logs(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")
    return (
        db.query(ReadingLog)
        .filter(ReadingLog.book_id == book_id)
        .order_by(ReadingLog.log_date.desc(), ReadingLog.id.desc())
        .all()
    )
