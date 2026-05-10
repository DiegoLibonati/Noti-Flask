import logging
from unittest.mock import patch

import pytest
from flask import Flask

from src.configs.sql_alchemy_config import db
from src.data_access.user_dao import UserDAO
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService


def _make_user(username: str, email: str, password: str = "pass") -> User:
    return User(username=username, email=email, password=EncryptService(password).password_hashed)


class TestUserDAO:
    @pytest.mark.integration
    def test_query_all_returns_empty_list(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: list[User] = UserDAO.query_all()
            assert result == []

    @pytest.mark.integration
    def test_add_persists_user(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _make_user("alice", "alice@test.com")
            result: User = UserDAO.add(user)
            assert result.id is not None
            assert result.username == "alice"

    @pytest.mark.integration
    def test_query_all_returns_added_users(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            UserDAO.add(_make_user("u1", "u1@test.com"))
            UserDAO.add(_make_user("u2", "u2@test.com"))
            result: list[User] = UserDAO.query_all()
            assert len(result) == 2

    @pytest.mark.integration
    def test_query_by_id_returns_user(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = UserDAO.add(_make_user("bob", "bob@test.com"))
            result: User | None = UserDAO.query_by_id(user.id)
            assert result is not None
            assert result.username == "bob"

    @pytest.mark.integration
    def test_query_by_id_returns_none_when_missing(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: User | None = UserDAO.query_by_id(99999)
            assert result is None

    @pytest.mark.integration
    def test_query_by_username_returns_user(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            UserDAO.add(_make_user("findme", "findme@test.com"))
            result: User | None = UserDAO.query_by_username("findme")
            assert result is not None
            assert result.username == "findme"

    @pytest.mark.integration
    def test_query_by_username_returns_none_when_missing(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: User | None = UserDAO.query_by_username("nobody")
            assert result is None

    @pytest.mark.integration
    def test_query_by_email_returns_user(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            UserDAO.add(_make_user("carol", "carol@test.com"))
            result: User | None = UserDAO.query_by_email("carol@test.com")
            assert result is not None
            assert result.email == "carol@test.com"

    @pytest.mark.integration
    def test_query_by_email_returns_none_when_missing(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: User | None = UserDAO.query_by_email("nobody@test.com")
            assert result is None

    @pytest.mark.integration
    def test_update_changes_username(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = UserDAO.add(_make_user("old_name", "old@test.com"))
            UserDAO.update(user, {"username": "new_name"})
            result: User | None = UserDAO.query_by_id(user.id)
            assert result is not None
            assert result.username == "new_name"

    @pytest.mark.integration
    def test_update_rollbacks_on_exception(self, app: Flask, db_session: None, caplog) -> None:
        with app.app_context():
            user: User = UserDAO.add(_make_user("rollback_u", "rb@test.com"))
            with caplog.at_level(logging.CRITICAL, logger="noti"):
                with patch("src.data_access.user_dao.db") as mock_db:
                    mock_db.session.commit.side_effect = Exception("db error")
                    mock_db.session.rollback = db.session.rollback
                    with pytest.raises(Exception, match="db error"):
                        UserDAO.update(user, {"username": "x"})

    @pytest.mark.integration
    def test_delete_removes_user(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = UserDAO.add(_make_user("del_user", "del@test.com"))
            user_id: int = user.id
            UserDAO.delete(user)
            assert UserDAO.query_by_id(user_id) is None
