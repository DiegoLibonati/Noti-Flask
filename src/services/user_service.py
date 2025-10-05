from src.constants.codes import CODE_ALREADY_USER_EXISTS
from src.constants.messages import MESSAGE_ALREADY_USER_EXISTS
from src.data_access.user_dao import UserDAO
from src.models.orm.user import User
from src.utils.exceptions import ConflictAPIError


class UserService:
    @staticmethod
    def add_user(user: User) -> User:
        existing = UserDAO.query_by_username(user.username)
        if existing:
            raise ConflictAPIError(
                code=CODE_ALREADY_USER_EXISTS,
                message=MESSAGE_ALREADY_USER_EXISTS,
            )
        return UserDAO.add(user)

    @staticmethod
    def get_all_users() -> list[User]:
        return UserDAO.query_all()

    @staticmethod
    def get_user_by_id(id: int) -> User | None:
        return UserDAO.query_by_id(id)

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        return UserDAO.query_by_username(username)

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return UserDAO.query_by_email(email)
