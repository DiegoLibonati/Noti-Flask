from datetime import UTC, datetime
from typing import Any

import pytest
from flask import Flask

from src.configs.sql_alchemy_config import db
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService


class TestUserModel:
    @pytest.mark.unit
    def test_init_sets_username(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        assert user.username == "alice"

    @pytest.mark.unit
    def test_init_sets_email(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        assert user.email == "a@test.com"

    @pytest.mark.unit
    def test_init_sets_password(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hashed_pw")
        assert user.password == "hashed_pw"

    @pytest.mark.unit
    def test_init_sets_created_at(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)

    @pytest.mark.unit
    def test_init_created_at_has_utc_timezone(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        assert user.created_at.tzinfo == UTC

    @pytest.mark.unit
    def test_to_dict_has_expected_keys(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        result: dict[str, Any] = user.to_dict()
        assert "id" in result
        assert "username" in result
        assert "email" in result
        assert "created_at" in result

    @pytest.mark.unit
    def test_to_dict_does_not_include_password(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="secret")
        result: dict[str, Any] = user.to_dict()
        assert "password" in result is False or result.get("password") is None

    @pytest.mark.unit
    def test_to_dict_values_match(self) -> None:
        user: User = User(username="bob", email="b@test.com", password="hash")
        result: dict[str, Any] = user.to_dict()
        assert result["username"] == "bob"
        assert result["email"] == "b@test.com"

    @pytest.mark.unit
    def test_to_dict_created_at_is_isoformat(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        result: dict[str, Any] = user.to_dict()
        datetime.fromisoformat(result["created_at"])

    @pytest.mark.integration
    def test_ensure_utc_event_sets_timezone_after_load(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = User(username="ev_user", email="ev@test.com", password=EncryptService("p").password_hashed)
            db.session.add(user)
            db.session.commit()
            user_id: int = user.id
            db.session.expire(user)
            reloaded: User | None = db.session.get(User, user_id)
            assert reloaded is not None
            assert reloaded.created_at.tzinfo is not None
