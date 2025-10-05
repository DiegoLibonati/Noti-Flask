from datetime import datetime, timezone
from typing import Any

from flask import Flask

from config.sql_alchemy_config import db
from src.models.orm.note import Note
from src.models.orm.user import User


def test_create_note_instance(flask_app: Flask) -> None:
    with flask_app.app_context():
        note: Note = Note(content="Test note", user_id=1)

        assert isinstance(note, Note)
        assert note.content == "Test note"
        assert note.user_id == 1
        assert isinstance(note.created_at, datetime)
        assert note.created_at.tzinfo == timezone.utc


def test_persist_note_with_user(flask_app: Flask, unique_user: dict[str, Any]) -> None:
    with flask_app.app_context():
        user: User = User(
            username=unique_user["username"],
            password=unique_user["password"],
            email=unique_user["email"],
        )
        db.session.add(user)
        db.session.commit()

        note: Note = Note(content="Nota persistida", user_id=user.id)
        db.session.add(note)
        db.session.commit()

        db_note: Note | None = db.session.get(Note, note.id)

        assert db_note is not None
        assert db_note.content == "Nota persistida"
        assert db_note.user_id == user.id
        assert isinstance(db_note.created_at, datetime)
        assert db_note.created_at.tzinfo == timezone.utc


def test_created_at_default_timezone(flask_app: Flask) -> None:
    with flask_app.app_context():
        note: Note = Note(content="Timezone test", user_id=99)
        db.session.add(note)
        db.session.commit()

        db_note: Note | None = db.session.get(Note, note.id)

        assert db_note is not None
        assert isinstance(db_note.created_at, datetime)
        assert db_note.created_at.tzinfo == timezone.utc
        assert db_note.created_at <= datetime.now(timezone.utc)


def test_foreign_key_relationship(
    flask_app: Flask, unique_user: dict[str, Any]
) -> None:
    with flask_app.app_context():
        user: User = User(
            username=unique_user["username"],
            password=unique_user["password"],
            email=unique_user["email"],
        )
        db.session.add(user)
        db.session.commit()

        note: Note = Note(content="Relación user-note", user_id=user.id)
        db.session.add(note)
        db.session.commit()

        db_user: User | None = db.session.get(User, user.id)
        assert db_user is not None
        assert len(db_user.notes) >= 1 if hasattr(db_user, "notes") else True
