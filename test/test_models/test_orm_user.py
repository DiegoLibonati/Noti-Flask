from datetime import datetime, timezone

import pytest
from flask import Flask

from config.sql_alchemy_config import db
from src.models.orm.note import Note
from src.models.orm.user import User


def test_create_user_instance(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User = User(
            username="test_user",
            email="test_user@gmail.com",
            password="1234",
        )

        assert isinstance(user, User)
        assert user.username == "test_user"
        assert user.email == "test_user@gmail.com"
        assert user.password == "1234"
        assert isinstance(user.created_at, datetime)
        assert user.created_at.tzinfo == timezone.utc
        assert user.id is None


def test_persist_user(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User = User(
            username="db_user",
            email="db_user@gmail.com",
            password="5678",
        )
        db.session.add(user)
        db.session.commit()

        db_user: User | None = db.session.get(User, user.id)

        assert db_user is not None
        assert db_user.username == "db_user"
        assert db_user.email == "db_user@gmail.com"
        assert db_user.password == "5678"
        assert isinstance(db_user.created_at, datetime)
        assert db_user.created_at.tzinfo == timezone.utc


def test_relationship_with_notes(flask_app: Flask) -> None:
    with flask_app.app_context():
        user: User = User(
            username="rel_user", email="rel_user@gmail.com", password="abcd"
        )
        db.session.add(user)
        db.session.commit()

        note1: Note = Note(content="Nota 1", user_id=user.id)
        note2: Note = Note(content="Nota 2", user_id=user.id)
        db.session.add_all([note1, note2])
        db.session.commit()

        db_user: User | None = db.session.get(User, user.id)
        assert db_user is not None
        assert len(db_user.notes) == 2

        db.session.delete(db_user)
        db.session.commit()

        assert db.session.get(User, user.id) is None
        assert db.session.get(Note, note1.id) is None
        assert db.session.get(Note, note2.id) is None


def test_unique_constraints(flask_app: Flask) -> None:
    with flask_app.app_context():
        user1: User = User(
            username="unique_user", email="unique@gmail.com", password="a"
        )
        db.session.add(user1)
        db.session.commit()

        user2: User = User(
            username="unique_user", email="other@gmail.com", password="b"
        )
        db.session.add(user2)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

        user3: User = User(
            username="other_user", email="unique@gmail.com", password="c"
        )
        db.session.add(user3)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()
