from typing import Any

from flask import Flask
from pytest import MonkeyPatch

from config.sql_alchemy_config import db
from src.data_access.user_dao import UserDAO
from src.models.orm.user import User


def test_query_all(flask_app: Flask) -> None:
    with flask_app.app_context():
        users: list[User] = UserDAO.query_all()

        assert isinstance(users, list)
        assert users == []


def test_query_by_username_not_found(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User | None = UserDAO.query_by_username("ghost_user")
        assert user is None


def test_query_by_email_not_found(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User | None = UserDAO.query_by_email("ghost@example.com")
        assert user is None


def test_query_by_id_not_found(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User | None = UserDAO.query_by_id(999)
        assert user is None


def test_add_user_success(flask_app: Flask, unique_user: dict[str, Any]) -> None:
    with flask_app.app_context():
        user_obj: User = User(
            username=unique_user["username"],
            password=unique_user["password"],
            email=unique_user["email"],
        )

        added_user: User = UserDAO.add(user_obj)

        assert isinstance(added_user, User)
        assert added_user.id is not None
        assert added_user.username == unique_user["username"]
        assert added_user.email == unique_user["email"]

        db_user: User | None = UserDAO.query_by_id(added_user.id)
        assert db_user is not None
        assert db_user.username == unique_user["username"]


def test_delete_user_success(flask_app: Flask, unique_user: dict[str, Any]) -> None:
    with flask_app.app_context():
        user_obj: User = User(
            username=unique_user["username"],
            password=unique_user["password"],
            email=unique_user["email"],
        )
        db.session.add(user_obj)
        db.session.commit()

        success: bool = UserDAO.delete(user_obj)
        assert success is True

        deleted_user: User | None = UserDAO.query_by_id(user_obj.id)
        assert deleted_user is None


def test_delete_user_failure(
    monkeypatch: MonkeyPatch, flask_app: Flask, unique_user: dict[str, Any]
) -> None:
    with flask_app.app_context():
        user_obj: User = User(
            username=unique_user["username"],
            password=unique_user["password"],
            email=unique_user["email"],
        )
        db.session.add(user_obj)
        db.session.commit()

        def mock_delete(user: User) -> None:
            raise Exception("DB error")

        monkeypatch.setattr(db.session, "delete", mock_delete)

        success: bool = UserDAO.delete(user_obj)
        assert success is False
