from datetime import timedelta

from app.models import ReadingLog
from app.services.pace import predict_book_finish
from app.services.streak import calculate_streak_values, get_streak_summary
from app.services.badges import award_eligible_badges
from app.time_utils import today_local


def test_pace_prediction_uses_seven_day_average(db_session, sample_user_and_book):
    user, book = sample_user_and_book
    today = today_local()
    logs = [
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=20, log_date=today - timedelta(days=1)),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=20, log_date=today - timedelta(days=3)),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=20, log_date=today - timedelta(days=5)),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=20, log_date=today - timedelta(days=15)),
    ]
    db_session.add_all(logs)
    db_session.commit()

    result = predict_book_finish(db_session, book)
    assert result.status == "ready"
    assert result.pages_remaining == 120
    assert result.average_daily_pages == 8.57
    assert result.days_left == 14


def test_pace_returns_not_enough_data_for_fewer_than_three_dates(
    db_session, sample_user_and_book
):
    user, book = sample_user_and_book
    today = today_local()
    db_session.add_all([
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=15, log_date=today - timedelta(days=1)),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=10, log_date=today - timedelta(days=2)),
    ])
    db_session.commit()

    result = predict_book_finish(db_session, book)
    assert result.status == "not_enough_data"
    assert result.days_left is None
    assert result.expected_finish_date is None


def test_current_and_longest_streak_aggregate_same_day_logs(
    db_session, sample_user_and_book
):
    user, book = sample_user_and_book
    today = today_local()
    db_session.add_all([
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=5, log_date=today),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=5, log_date=today),
        ReadingLog(user_id=user.id, book_id=book.id, pages_read=10, log_date=today - timedelta(days=1)),
    ])
    db_session.commit()

    summary = get_streak_summary(db_session, user, today=today)
    assert summary["today_pages"] == 10
    assert summary["today_counted"] is True
    assert summary["current_streak"] == 2
    assert summary["longest_streak"] == 2


def test_streak_remains_active_through_yesterday():
    today = today_local()
    totals = {today - timedelta(days=1): 10, today - timedelta(days=2): 12}
    current, longest = calculate_streak_values(totals, daily_goal_pages=10, today=today)
    assert current == 2
    assert longest == 2


def test_badges_are_awarded_once_at_milestone(db_session, sample_user_and_book):
    user, book = sample_user_and_book
    today = today_local()
    db_session.add_all([
        ReadingLog(
            user_id=user.id,
            book_id=book.id,
            pages_read=10,
            log_date=today - timedelta(days=offset),
        )
        for offset in range(7)
    ])
    db_session.flush()

    first_awards = award_eligible_badges(db_session, user)
    db_session.commit()
    second_awards = award_eligible_badges(db_session, user)

    assert [badge.badge_code for badge in first_awards] == ["week_warrior"]
    assert second_awards == []
