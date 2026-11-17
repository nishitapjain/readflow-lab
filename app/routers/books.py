"""Book creation, listing, and update endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book, ReadingLog, User
from app.schemas import BookCreate, BookOut, BookUpdate
from app.time_utils import today_local

router = APIRouter(tags=["Books"])


@router.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    book = Book(
        user_id=payload.user_id,
        title=payload.title.strip(),
        author=payload.author.strip() if payload.author else None,
        total_pages=payload.total_pages,
        started_on=payload.started_on or today_local(),
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("/users/{user_id}/books", response_model=list[BookOut])
def list_user_books(user_id: int, db: Session = Depends(get_db)):
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return (
        db.query(Book)
        .filter(Book.user_id == user_id)
        .order_by(Book.started_on.desc(), Book.id.desc())
        .all()
    )


@router.patch("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found.")

    updates = payload.model_dump(exclude_unset=True)
    if "total_pages" in updates and updates["total_pages"] is not None:
        logged_total = (
            db.query(func.coalesce(func.sum(ReadingLog.pages_read), 0))
            .filter(ReadingLog.book_id == book.id)
            .scalar()
        )
        if updates["total_pages"] < int(logged_total or 0):
            raise HTTPException(
                status_code=400,
                detail="total_pages cannot be less than the pages already logged.",
            )

    for field, value in updates.items():
        if value is None and field != "author":
            continue
        if field == "title":
            value = value.strip()
        elif field == "author" and value is not None:
            value = value.strip()
        setattr(book, field, value)

    logged_total = (
        db.query(func.coalesce(func.sum(ReadingLog.pages_read), 0))
        .filter(ReadingLog.book_id == book.id)
        .scalar()
    )
    if book.status == "finished" or int(logged_total or 0) == book.total_pages:
        book.status = "finished"
        book.finished_on = book.finished_on or today_local()
    else:
        book.finished_on = None

    db.commit()
    db.refresh(book)
    return book
