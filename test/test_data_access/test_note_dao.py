from typing import Any

from flask import Flask
from pytest import MonkeyPatch

from config.sql_alchemy_config import db
from src.data_access.note_dao import NoteDAO
from src.models.orm.note import Note


def test_query_all(flask_app: Flask) -> None:
    with flask_app.app_context():
        notes: list[Note] = NoteDAO.query_all()

        assert isinstance(notes, list)
        assert notes == []


def test_query_by_id_not_found(flask_app: Flask) -> None:
    with flask_app.app_context():
        note: Note | None = NoteDAO.query_by_id(999)
        assert note is None


def test_add_note_success(flask_app: Flask, unique_note: dict[str, Any]) -> None:
    with flask_app.app_context():
        note_obj: Note = Note(
            content=unique_note["content"],
            user_id=unique_note["user_id"],
        )

        added_note: Note = NoteDAO.add(note_obj)

        assert isinstance(added_note, Note)
        assert added_note.id is not None
        assert added_note.content == unique_note["content"]

        # Verificar persistencia
        db_note: Note | None = NoteDAO.query_by_id(added_note.id)
        assert db_note is not None
        assert db_note.content == unique_note["content"]


def test_update_note_success(flask_app: Flask, unique_note: dict[str, Any]) -> None:
    with flask_app.app_context():
        note_obj: Note = Note(content="old_content", user_id=unique_note["user_id"])
        db.session.add(note_obj)
        db.session.commit()

        new_data: dict[str, Any] = {"content": unique_note["content"]}
        success: bool = NoteDAO.update(note_obj, new_data)

        db.session.refresh(note_obj)

        assert success is True
        assert note_obj.content == unique_note["content"]


def test_update_note_failure(
    monkeypatch: MonkeyPatch, flask_app: Flask, unique_note: dict[str, Any]
) -> None:
    with flask_app.app_context():
        note_obj: Note = Note(content="old_content", user_id=unique_note["user_id"])
        db.session.add(note_obj)
        db.session.commit()

        def mock_commit() -> None:
            raise Exception("DB error")

        monkeypatch.setattr(db.session, "commit", mock_commit)

        success: bool = NoteDAO.update(note_obj, {"content": "new_content"})
        assert success is False


def test_delete_note_success(flask_app: Flask, unique_note: dict[str, Any]) -> None:
    with flask_app.app_context():
        note_obj: Note = Note(
            content=unique_note["content"], user_id=unique_note["user_id"]
        )
        db.session.add(note_obj)
        db.session.commit()

        success: bool = NoteDAO.delete(note_obj)
        assert success is True

        deleted_note: Note | None = NoteDAO.query_by_id(note_obj.id)
        assert deleted_note is None


def test_delete_note_failure(
    monkeypatch: MonkeyPatch, flask_app: Flask, unique_note: dict[str, Any]
) -> None:
    with flask_app.app_context():
        note_obj: Note = Note(
            content=unique_note["content"], user_id=unique_note["user_id"]
        )
        db.session.add(note_obj)
        db.session.commit()

        def mock_delete(note: Note) -> None:
            raise Exception("DB error")

        monkeypatch.setattr(db.session, "delete", mock_delete)

        success: bool = NoteDAO.delete(note_obj)
        assert success is False
