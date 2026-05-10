from unittest.mock import patch

import pytest

from src.models.orm.user import User
from src.services.user_service import UserService


class TestUserService:
    @pytest.mark.unit
    def test_add_user_calls_dao_add(self) -> None:
        user: User = User(username="alice", email="a@test.com", password="hash")
        with patch("src.services.user_service.UserDAO.add", return_value=user) as mock_add:
            result: User = UserService.add_user(user)
        mock_add.assert_called_once_with(user)
        assert result is user

    @pytest.mark.unit
    def test_get_all_users_returns_list(self) -> None:
        mock_users: list[User] = [User(username="a", email="a@t.com", password="h")]
        with patch("src.services.user_service.UserDAO.query_all", return_value=mock_users):
            result: list[User] = UserService.get_all_users()
        assert result is mock_users

    @pytest.mark.unit
    def test_get_all_users_returns_empty(self) -> None:
        with patch("src.services.user_service.UserDAO.query_all", return_value=[]):
            result: list[User] = UserService.get_all_users()
        assert result == []

    @pytest.mark.unit
    def test_get_user_by_id_returns_user(self) -> None:
        user: User = User(username="bob", email="b@test.com", password="hash")
        with patch("src.services.user_service.UserDAO.query_by_id", return_value=user):
            result: User | None = UserService.get_user_by_id(id=1)
        assert result is user

    @pytest.mark.unit
    def test_get_user_by_id_returns_none(self) -> None:
        with patch("src.services.user_service.UserDAO.query_by_id", return_value=None):
            result: User | None = UserService.get_user_by_id(id=99999)
        assert result is None

    @pytest.mark.unit
    def test_get_user_by_username_returns_user(self) -> None:
        user: User = User(username="carol", email="c@test.com", password="hash")
        with patch("src.services.user_service.UserDAO.query_by_username", return_value=user):
            result: User | None = UserService.get_user_by_username(username="carol")
        assert result is user

    @pytest.mark.unit
    def test_get_user_by_username_returns_none(self) -> None:
        with patch("src.services.user_service.UserDAO.query_by_username", return_value=None):
            result: User | None = UserService.get_user_by_username(username="nobody")
        assert result is None

    @pytest.mark.unit
    def test_get_user_by_email_returns_user(self) -> None:
        user: User = User(username="dave", email="d@test.com", password="hash")
        with patch("src.services.user_service.UserDAO.query_by_email", return_value=user):
            result: User | None = UserService.get_user_by_email(email="d@test.com")
        assert result is user

    @pytest.mark.unit
    def test_get_user_by_email_returns_none(self) -> None:
        with patch("src.services.user_service.UserDAO.query_by_email", return_value=None):
            result: User | None = UserService.get_user_by_email(email="nobody@test.com")
        assert result is None
