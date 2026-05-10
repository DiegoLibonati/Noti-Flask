from datetime import UTC, datetime
from typing import Any

import pytest
from flask import Flask

from src.configs.sql_alchemy_config import db
from src.models.orm.note import Note
from src.models.orm.user import User
from src.services.encrypt_service import EncryptService


class TestNoteModel:
    @pytest.mark.unit
    def test_init_sets_content(self) -> None:
        note: Note = Note(content="hello", user_id=1)
        assert note.content == "hello"

    @pytest.mark.unit
    def test_init_sets_user_id(self) -> None:
        note: Note = Note(content="x", user_id=42)
        assert note.user_id == 42

    @pytest.mark.unit
    def test_init_sets_created_at(self) -> None:
        note: Note = Note(content="x", user_id=1)
        assert note.created_at is not None
        assert isinstance(note.created_at, datetime)

    @pytest.mark.unit
    def test_init_created_at_has_utc_timezone(self) -> None:
        note: Note = Note(content="x", user_id=1)
        assert note.created_at.tzinfo == UTC

    @pytest.mark.unit
    def test_to_dict_has_expected_keys(self) -> None:
        note: Note = Note(content="hello", user_id=1)
        result: dict[str, Any] = note.to_dict()
        assert "id" in result
        assert "content" in result
        assert "user_id" in result
        assert "created_at" in result

    @pytest.mark.unit
    def test_to_dict_content_matches(self) -> None:
        note: Note = Note(content="test content", user_id=5)
        result: dict[str, Any] = note.to_dict()
        assert result["content"] == "test content"
        assert result["user_id"] == 5

    @pytest.mark.unit
    def test_to_dict_created_at_is_isoformat(self) -> None:
        note: Note = Note(content="x", user_id=1)
        result: dict[str, Any] = note.to_dict()
        datetime.fromisoformat(result["created_at"])

    @pytest.mark.integration
    def test_ensure_utc_event_sets_timezone_after_load(self, app: Flask, db_session: None) -> None:
        with app.app_context():
            user: User = User(username="u1", email="u1@test.com", password=EncryptService("p").password_hashed)
            db.session.add(user)
            db.session.commit()
            note: Note = Note(content="persisted", user_id=user.id)
            db.session.add(note)
            db.session.commit()
            note_id: int = note.id
            db.session.expire(note)
            reloaded: Note | None = db.session.get(Note, note_id)
            assert reloaded is not None
            assert reloaded.created_at.tzinfo is not None
