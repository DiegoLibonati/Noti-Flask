from typing import Any
from unittest.mock import patch

import pytest

from src.models.orm.note import Note
from src.services.note_service import NoteService


class TestNoteService:
    @pytest.mark.unit
    def test_get_all_notes_returns_list(self) -> None:
        mock_notes: list[Note] = [Note(content="a", user_id=1), Note(content="b", user_id=1)]
        with patch("src.services.note_service.NoteDAO.query_all", return_value=mock_notes):
            result: list[Note] = NoteService.get_all_notes()
        assert len(result) == 2

    @pytest.mark.unit
    def test_get_all_notes_returns_empty_list(self) -> None:
        with patch("src.services.note_service.NoteDAO.query_all", return_value=[]):
            result: list[Note] = NoteService.get_all_notes()
        assert result == []

    @pytest.mark.unit
    def test_get_note_by_id_returns_note(self) -> None:
        mock_note: Note = Note(content="found", user_id=1)
        with patch("src.services.note_service.NoteDAO.query_by_id", return_value=mock_note):
            result: Note | None = NoteService.get_note_by_id(id=1)
        assert result is mock_note

    @pytest.mark.unit
    def test_get_note_by_id_returns_none_when_missing(self) -> None:
        with patch("src.services.note_service.NoteDAO.query_by_id", return_value=None):
            result: Note | None = NoteService.get_note_by_id(id=99999)
        assert result is None

    @pytest.mark.unit
    def test_add_note_calls_dao_add(self) -> None:
        note: Note = Note(content="new", user_id=1)
        with patch("src.services.note_service.NoteDAO.add", return_value=note) as mock_add:
            result: Note = NoteService.add_note(note)
        mock_add.assert_called_once_with(note)
        assert result is note

    @pytest.mark.unit
    def test_delete_note_calls_dao_delete(self) -> None:
        note: Note = Note(content="del", user_id=1)
        with patch("src.services.note_service.NoteDAO.delete") as mock_delete:
            NoteService.delete_note(note)
        mock_delete.assert_called_once_with(note)

    @pytest.mark.unit
    def test_update_note_calls_dao_update(self) -> None:
        note: Note = Note(content="old", user_id=1)
        data: dict[str, Any] = {"content": "new"}
        with patch("src.services.note_service.NoteDAO.update") as mock_update:
            NoteService.update_note(note, data)
        mock_update.assert_called_once_with(note, data)
