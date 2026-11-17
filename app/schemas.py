"""Pydantic request and response schemas."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    daily_goal_pages: int = Field(default=10, gt=0)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    daily_goal_pages: int
    created_at: datetime


class BookCreate(BaseModel):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=150)
    total_pages: int = Field(gt=0)
    started_on: date | None = None


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, max_length=150)
    total_pages: int | None = Field(default=None, gt=0)
    status: Literal["reading", "finished"] | None = None


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    author: str | None
    total_pages: int
    status: Literal["reading", "finished"]
    started_on: date
    finished_on: date | None


class ReadingLogCreate(BaseModel):
    user_id: int = Field(gt=0)
    book_id: int = Field(gt=0)
    pages_read: int = Field(gt=0)
    log_date: date | None = None


class ReadingLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    pages_read: int
    log_date: date
    created_at: datetime


class PredictionOut(BaseModel):
    book_id: int
    status: Literal["ready", "not_enough_data", "finished"]
    pages_remaining: int
    average_daily_pages: float
    days_left: int | None
    expected_finish_date: date | None
    message: str


class StreakOut(BaseModel):
    user_id: int
    current_streak: int
    longest_streak: int
    daily_goal_pages: int
    today_pages: int
    today_counted: bool
    as_of_date: date


class HeatmapDay(BaseModel):
    date: date
    pages_read: int


class BadgeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    badge_code: str
    awarded_on: date


class ErrorMessage(BaseModel):
    detail: str
