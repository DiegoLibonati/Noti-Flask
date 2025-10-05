from config.logger_config import setup_logger
from config.sql_alchemy_config import db
from src.models.orm.user import User

logger = setup_logger()


class UserDAO:
    @staticmethod
    def query_all() -> list[User]:
        return User.query.all()

    @staticmethod
    def query_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def query_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def query_by_id(id: int) -> User | None:
        return db.session.get(User, int(id))

    @staticmethod
    def add(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user: User) -> bool:
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            logger.error("Error deleting user", exc_info=ex)
            return False
