from typing import Any

from src.configs.sql_alchemy_config import db
from src.models.orm.user import User
from src.utils.commit_or_rollback_decorator import commit_or_rollback_decorator


class UserDAO:
    @staticmethod
    def query_all() -> list[User]:
        return list(db.session.execute(db.select(User)).scalars().all())

    @staticmethod
    def query_by_username(username: str) -> User | None:
        return db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

    @staticmethod
    def query_by_email(email: str) -> User | None:
        return db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

    @staticmethod
    def query_by_id(id: int) -> User | None:
        return db.session.get(User, id)

    @staticmethod
    @commit_or_rollback_decorator("adding user")
    def add(user: User) -> User:
        db.session.add(user)
        return user

    @staticmethod
    @commit_or_rollback_decorator("updating user")
    def update(user: User, data: dict[str, Any]) -> None:
        for key, value in data.items():
            setattr(user, key, value)

    @staticmethod
    @commit_or_rollback_decorator("deleting user")
    def delete(user: User) -> None:
        db.session.delete(user)
