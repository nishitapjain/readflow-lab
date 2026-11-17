"""Date helpers. The app uses APP_TIMEZONE to determine the current calendar day."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import APP_TIMEZONE


def today_local():
    return datetime.now(ZoneInfo(APP_TIMEZONE)).date()
