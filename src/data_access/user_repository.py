import logging

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from src.extensions import db as db_extension
from src.models.db.User import User


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UserRepository:
    def __init__(self, db: SQLAlchemy = db_extension) -> None:
        self.db = db

    def get_users(self) -> list[User]:
        return User.query.all()

    def get_user_by_username(self, username: str) -> User:
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email: str) -> User:
        return User.query.filter_by(email=email).first()
    
    def get_user_by_id(self, id: int) -> User:
        return self.db.session.get(User, int(id))
    
    def add_user(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=generate_password_hash(password))
        
        self.db.session.add(user)
        self.db.session.commit()

        return user
    
    def remove_user(self, user: User) -> bool:
        try:
            self.db.session.delete(instance=user)
            self.db.session.commit()

            return True
        except Exception as ex:
            logging.info(ex)
            return False