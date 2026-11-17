"""User creation and retrieval endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == str(payload.email).lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists.")

    user = User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        daily_goal_pages=payload.daily_goal_pages,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
