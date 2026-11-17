"""Streak and daily reading totals, calculated from reading logs."""

from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ReadingLog, User
from app.time_utils import today_local


def daily_page_totals(db: Session, user_id: int):
    rows = (
        db.query(ReadingLog.log_date, func.sum(ReadingLog.pages_read))
        .filter(ReadingLog.user_id == user_id)
        .group_by(ReadingLog.log_date)
        .all()
    )
    return {day: int(total) for day, total in rows}


def calculate_streak_values(daily_totals: dict[date, int], daily_goal_pages: int, today: date):
    counted_dates = {
        day for day, pages in daily_totals.items()
        if pages >= daily_goal_pages and day <= today
    }

    longest = 0
    current_run = 0
    previous_day = None
    for day in sorted(counted_dates):
        if previous_day is not None and day == previous_day + timedelta(days=1):
            current_run += 1
        else:
            current_run = 1
        longest = max(longest, current_run)
        previous_day = day

    # A streak remains active through today if today is counted, or through
    # yesterday if today's reading goal has not yet been reached.
    if today in counted_dates:
        anchor = today
    elif today - timedelta(days=1) in counted_dates:
        anchor = today - timedelta(days=1)
    else:
        anchor = None

    current = 0
    cursor = anchor
    while cursor is not None and cursor in counted_dates:
        current += 1
        cursor -= timedelta(days=1)

    return current, longest


def get_streak_summary(db: Session, user: User, today: date | None = None):
    today = today or today_local()
    totals = daily_page_totals(db, user.id)
    current, longest = calculate_streak_values(totals, user.daily_goal_pages, today)
    today_pages = totals.get(today, 0)
    return {
        "user_id": user.id,
        "current_streak": current,
        "longest_streak": longest,
        "daily_goal_pages": user.daily_goal_pages,
        "today_pages": today_pages,
        "today_counted": today_pages >= user.daily_goal_pages,
        "as_of_date": today,
    }


def get_longest_streak(db: Session, user: User, today: date | None = None) -> int:
    return get_streak_summary(db, user, today)["longest_streak"]
