import logging
from unittest.mock import patch

import pytest
from flask import Flask

from src.configs.sql_alchemy_config import db
from src.data_access.note_dao import NoteDAO
from src.models.orm.note import Note
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService


def _create_user(username: str = "u", email: str = "u@t.com") -> User:
    user: User = User(username=username, email=email, password=EncryptService("p").password_hashed)
    db.session.add(user)
    db.session.commit()
    return user


class TestNoteDAO:
    @pytest.mark.integration
    def test_query_all_returns_empty_list(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: list[Note] = NoteDAO.query_all()
            assert result == []

    @pytest.mark.integration
    def test_add_persists_note(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = Note(content="hello", user_id=user.id)
            result: Note = NoteDAO.add(note)
            assert result.id is not None
            assert result.content == "hello"

    @pytest.mark.integration
    def test_query_all_returns_added_notes(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _create_user()
            NoteDAO.add(Note(content="a", user_id=user.id))
            NoteDAO.add(Note(content="b", user_id=user.id))
            result: list[Note] = NoteDAO.query_all()
            assert len(result) == 2

    @pytest.mark.integration
    def test_query_by_id_returns_note(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = NoteDAO.add(Note(content="find me", user_id=user.id))
            result: Note | None = NoteDAO.query_by_id(note.id)
            assert result is not None
            assert result.content == "find me"

    @pytest.mark.integration
    def test_query_by_id_returns_none_when_missing(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            result: Note | None = NoteDAO.query_by_id(99999)
            assert result is None

    @pytest.mark.integration
    def test_update_changes_content(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = NoteDAO.add(Note(content="old", user_id=user.id))
            NoteDAO.update(note, {"content": "new"})
            result: Note | None = NoteDAO.query_by_id(note.id)
            assert result is not None
            assert result.content == "new"

    @pytest.mark.integration
    def test_update_rollbacks_on_exception(self, app: Flask, db_session: None, caplog) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = NoteDAO.add(Note(content="x", user_id=user.id))
            with caplog.at_level(logging.CRITICAL, logger="noti"):
                with patch("src.data_access.note_dao.db") as mock_db:
                    mock_db.session.commit.side_effect = Exception("db error")
                    mock_db.session.rollback = db.session.rollback
                    with pytest.raises(Exception, match="db error"):
                        NoteDAO.update(note, {"content": "y"})

    @pytest.mark.integration
    def test_delete_removes_note(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = NoteDAO.add(Note(content="to delete", user_id=user.id))
            note_id: int = note.id
            NoteDAO.delete(note)
            assert NoteDAO.query_by_id(note_id) is None

    @pytest.mark.integration
    def test_delete_rollbacks_on_exception(self, app: Flask, db_session: None, caplog) -> None:
        with app.app_context():
            user: User = _create_user()
            note: Note = NoteDAO.add(Note(content="x", user_id=user.id))
            with caplog.at_level(logging.CRITICAL, logger="noti"):
                with patch("src.data_access.note_dao.db") as mock_db:
                    mock_db.session.delete = db.session.delete
                    mock_db.session.commit.side_effect = Exception("db error")
                    mock_db.session.rollback = db.session.rollback
                    with pytest.raises(Exception, match="db error"):
                        NoteDAO.delete(note)
