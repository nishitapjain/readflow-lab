from datetime import date, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def sample_user_and_book(db_session):
    from app.models import Book, User

    user = User(name="Test Reader", email="reader@example.com", daily_goal_pages=10)
    db_session.add(user)
    db_session.flush()
    book = Book(
        user_id=user.id,
        title="Test Book",
        author="A. Author",
        total_pages=200,
        status="reading",
        started_on=date.today() - timedelta(days=20),
    )
    db_session.add(book)
    db_session.commit()
    return user, book
