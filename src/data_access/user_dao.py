from typing import Any

from src.configs.logger_config import setup_logger
from src.configs.sql_alchemy_config import db
from src.models.orm.user import User

logger = setup_logger()


class UserDAO:
    @staticmethod
    def query_all() -> list[User]:
        return db.session.execute(db.select(User)).scalars().all()

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
    def add(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User, data: dict[str, Any]) -> None:
        try:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            logger.error("Error updating user", exc_info=ex)
            raise

    @staticmethod
    def delete(user: User) -> None:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            logger.error("Error deleting user", exc_info=ex)
            raise
