import pytest
from pytest import MonkeyPatch

from src.models.orm.user import User
from src.services.user_service import UserService
from src.utils.exceptions import ConflictAPIError


def test_add_user_success(monkeypatch: MonkeyPatch) -> None:
    mock_user: User = User(username="user_ok", email="ok@gmail.com", password="1234")

    def mock_query_by_username(_: str) -> None:
        return None

    def mock_add(u: User) -> User:
        return u

    monkeypatch.setattr(
        "src.services.user_service.UserDAO.query_by_username", mock_query_by_username
    )
    monkeypatch.setattr("src.services.user_service.UserDAO.add", mock_add)

    result: User = UserService.add_user(mock_user)

    assert isinstance(result, User)
    assert result.username == "user_ok"
    assert result.email == "ok@gmail.com"
    assert result.password == "1234"


def test_add_user_conflict(monkeypatch: MonkeyPatch) -> None:
    mock_user: User = User(
        username="user_exists", email="exist@gmail.com", password="1234"
    )

    def mock_query_by_username(_: str) -> User:
        return mock_user

    monkeypatch.setattr(
        "src.services.user_service.UserDAO.query_by_username", mock_query_by_username
    )

    with pytest.raises(ConflictAPIError):
        UserService.add_user(mock_user)


def test_get_all_users(monkeypatch: MonkeyPatch) -> None:
    users: list[User] = [
        User(username="u1", email="u1@gmail.com", password="a"),
        User(username="u2", email="u2@gmail.com", password="b"),
    ]

    monkeypatch.setattr("src.services.user_service.UserDAO.query_all", lambda: users)

    result: list[User] = UserService.get_all_users()

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(u, User) for u in result)


def test_get_user_by_id(monkeypatch: MonkeyPatch) -> None:
    user: User = User(username="by_id", email="by_id@gmail.com", password="x")

    monkeypatch.setattr("src.services.user_service.UserDAO.query_by_id", lambda _: user)

    result: User | None = UserService.get_user_by_id(1)

    assert isinstance(result, User)
    assert result.username == "by_id"
    assert result.email == "by_id@gmail.com"


def test_get_user_by_username(monkeypatch: MonkeyPatch) -> None:
    user: User = User(
        username="by_username", email="by_username@gmail.com", password="y"
    )

    monkeypatch.setattr(
        "src.services.user_service.UserDAO.query_by_username", lambda _: user
    )

    result: User | None = UserService.get_user_by_username("by_username")

    assert isinstance(result, User)
    assert result.username == "by_username"


def test_get_user_by_email(monkeypatch: MonkeyPatch) -> None:
    user: User = User(username="by_email", email="by_email@gmail.com", password="z")

    monkeypatch.setattr(
        "src.services.user_service.UserDAO.query_by_email", lambda _: user
    )

    result: User | None = UserService.get_user_by_email("by_email@gmail.com")

    assert isinstance(result, User)
    assert result.email == "by_email@gmail.com"
