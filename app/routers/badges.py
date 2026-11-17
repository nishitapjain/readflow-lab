"""Earned badge endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserBadge
from app.schemas import BadgeOut
from app.services.badges import award_eligible_badges

router = APIRouter(tags=["Badges"])


@router.get("/users/{user_id}/badges", response_model=list[BadgeOut])
def get_user_badges(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    newly_awarded = award_eligible_badges(db, user)
    if newly_awarded:
        db.commit()
    return (
        db.query(UserBadge)
        .filter(UserBadge.user_id == user_id)
        .order_by(UserBadge.awarded_on.asc(), UserBadge.id.asc())
        .all()
    )
