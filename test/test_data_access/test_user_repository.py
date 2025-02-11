from typing import Any

from src.data_access.user_repository import UserRepository
from src.models.db.User import User

def test_add_user(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")
    
    user = user_repository.add_user(username=username, password=password, email=email)

    assert user
    assert isinstance(user, User)


def test_get_users(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")

    user = user_repository.get_user_by_username(username=username)
    users = user_repository.get_users()

    assert users
    assert user in users


def test_get_user_by_username(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")

    user = user_repository.get_user_by_username(username=username)

    assert user
    assert isinstance(user, User)


def test_get_user_by_email(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    email = mock_user.get("email")

    user = user_repository.get_user_by_email(email=email)

    assert user
    assert isinstance(user, User)


def test_get_user_by_id(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    email = mock_user.get("email")

    user = user_repository.get_user_by_email(email=email)
    user = user_repository.get_user_by_id(id=user.id)

    assert user
    assert isinstance(user, User)


def test_remove_user(user_repository: UserRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")

    user = user_repository.get_user_by_username(username=username)

    remove = user_repository.remove_user(user=user)
    
    assert remove