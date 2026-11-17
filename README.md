# ReadFlow Backend

FastAPI + PostgreSQL + SQLAlchemy backend for the ReadFlow reading-habit tracker MVP.

## Included functionality

- Create and retrieve users, including their daily page goal.
- Create, list, and update books.
- Record multiple reading sessions on the same date.
- Retrieve reading history for a book.
- Estimate a book's days remaining and expected finish date.
- Calculate current and longest reading streaks.
- Return a full daily heatmap window, including zero-reading days.
- Award one-time streak badges at 7, 30, and 100 days.
- Initialize the four MVP tables automatically when the API starts.

## Requirements

- Python 3.10 or newer (Python 3.12 recommended)
- PostgreSQL 15 or newer

## 1. Create the database

Create a PostgreSQL database named `readflow` using pgAdmin or `psql`:

```sql
CREATE DATABASE readflow;
```

## 2. Configure environment variables

From this `backend` directory, copy `.env.example` to `.env` and edit the password:

```powershell
Copy-Item .env.example .env
```

Example connection string:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/readflow
APP_TIMEZONE=Asia/Kolkata
```

Do not commit `.env`. Commit `.env.example` only.

## 3. Install and run

Run these commands from the `backend` directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Linux/macOS activation:

```bash
source venv/bin/activate
```

Open:

- API root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

The first server start creates the four tables if they do not exist. This `create_all` approach is convenient for the MVP. Use Alembic migrations before treating the service as production software.

## API contract

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/users` | Create a user and daily goal |
| GET | `/users/{user_id}` | Retrieve a user |
| POST | `/books` | Add a book |
| GET | `/users/{user_id}/books` | List a user's books |
| PATCH | `/books/{book_id}` | Update book details/status |
| POST | `/logs` | Record a reading session |
| GET | `/books/{book_id}/logs` | Reading history for a book |
| GET | `/books/{book_id}/prediction` | Pace prediction |
| GET | `/users/{user_id}/streak` | Current and longest streak |
| GET | `/users/{user_id}/heatmap?days=90` | Daily pages for 1–365 days |
| GET | `/users/{user_id}/badges` | Earned badges |

## Example API requests

Create a user:

```json
{
  "name": "Aarav",
  "email": "aarav@example.com",
  "daily_goal_pages": 20
}
```

Create a book (use the returned user ID):

```json
{
  "user_id": 1,
  "title": "Atomic Habits",
  "author": "James Clear",
  "total_pages": 320
}
```

Create a reading log (use the returned user and book IDs):

```json
{
  "user_id": 1,
  "book_id": 1,
  "pages_read": 25,
  "log_date": "2026-11-16"
}
```

`log_date` can be omitted to use the current date in `APP_TIMEZONE`.

## Business rules implemented

### Pace prediction

- Uses the selected book's reading logs from the last seven calendar days, including zero-reading dates in the seven-day denominator.
- Requires logs on at least three distinct dates in that window.
- Average daily pages = pages logged in the seven-day window divided by seven.
- Pages remaining = total book pages minus all pages logged for that book.
- Days left are rounded up. The expected date is the current app-local date plus days left.
- Returns `not_enough_data` when fewer than three distinct dates have logs or the average is zero.

### Streak

- Pages are aggregated across all the user's books for each date.
- A date counts when the daily total reaches the user's daily goal.
- Current streak ends today, or yesterday when today has not yet met the goal.
- Longest streak is the longest consecutive run in the user's history.

### Badges

- `week_warrior`: 7-day longest streak.
- `month_master`: 30-day longest streak.
- `century_legend`: 100-day longest streak.
- Each badge is stored once per user.

### Reading log validation

- Pages must be positive.
- The selected book must belong to the supplied user.
- Future-dated reading logs are rejected.
- A reading log cannot take a book's total logged pages above its total page count.
- The book is automatically marked finished when all pages have been logged.
- Multiple logs per book per date are allowed.

## Run tests

From this directory:

```powershell
python -m pytest -q
```

Tests use an in-memory SQLite database; they do not need the PostgreSQL service.

## Important MVP limitation

This version does not implement login/JWT authentication. The `user_id` fields are therefore identifiers for the MVP, not proof of identity. Do not expose this API publicly with real user data until authentication and authorization are added. CORS is configured for local React development and should be restricted to the actual deployed frontend origin before deployment.
