"""Award one-time badges when a user's longest streak reaches a milestone."""

from sqlalchemy.orm import Session

from app.models import User, UserBadge
from app.services.streak import get_longest_streak
from app.time_utils import today_local

BADGE_MILESTONES = {
    "week_warrior": 7,
    "month_master": 30,
    "century_legend": 100,
}


def award_eligible_badges(db: Session, user: User) -> list[UserBadge]:
    longest = get_longest_streak(db, user)
    existing = {
        row.badge_code
        for row in db.query(UserBadge).filter(UserBadge.user_id == user.id).all()
    }
    newly_awarded = []
    for badge_code, milestone in BADGE_MILESTONES.items():
        if longest >= milestone and badge_code not in existing:
            badge = UserBadge(
                user_id=user.id,
                badge_code=badge_code,
                awarded_on=today_local(),
            )
            db.add(badge)
            newly_awarded.append(badge)
    return newly_awarded
