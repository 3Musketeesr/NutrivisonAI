import pytest
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from pydantic import ValidationError
import builtins

from backend.users.model import User
from backend.helpers import engine as b_engine


@pytest.fixture(autouse=True)
def test_db_engine(monkeypatch):
    # Use in-memory SQLite that persists across connections
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Ensure application code uses this engine
    monkeypatch.setattr(b_engine, "_engine", engine, raising=False)
    monkeypatch.setattr(b_engine, "get_engine", lambda: engine, raising=False)

    yield engine


def test_create_user_success(test_db_engine):
    username = "alice"
    email = "alice@example.com"
    password = "Str0ng_P@ssw0rd!"

    user = User.create_user(username=username, email=email, password=password)

    assert user is not None
    assert user.id is not None
    assert user.username == username
    assert user.email == email
    # password should be hashed, not equal to plain
    assert user.password != password


def test_create_user_duplicate_username_returns_none(test_db_engine):
    username = "bob"
    email1 = "bob1@example.com"
    email2 = "bob2@example.com"
    password = "Str0ng_P@ssw0rd!"

    user1 = User.create_user(username=username, email=email1, password=password)
    assert user1 is not None

    user2 = User.create_user(username=username, email=email2, password=password)
    assert user2 is None


def test_create_user_weak_password_raises(test_db_engine):
    username = "charlie"
    email = "charlie@example.com"
    weak_password = "short"  # < 8 chars triggers length rule

    with pytest.raises(ValueError):
        User.create_user(username=username, email=email, password=weak_password)


def test_create_user_invalid_email_raises(test_db_engine):
    username = "dana"
    bad_email = "not-an-email"
    password = "Str0ng_P@ssw0rd!"

    with pytest.raises(ValueError):
        User.create_user(username=username, email=bad_email, password=password)


