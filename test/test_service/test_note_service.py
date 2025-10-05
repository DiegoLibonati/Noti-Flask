from typing import Any

import pytest
from pytest import MonkeyPatch

from src.constants.codes import CODE_NOT_EXISTS_NOTE
from src.constants.messages import MESSAGE_NOT_EXISTS_NOTE
from src.data_access.note_dao import NoteDAO
from src.models.orm.note import Note
from src.services.note_service import NoteService
from src.utils.exceptions import NotFoundAPIError


def test_add_note_success(monkeypatch: MonkeyPatch) -> None:
    note: Note = Note(content="Nueva nota", user_id=1)

    def mock_add(note_param: Note) -> Note:
        return note_param

    monkeypatch.setattr(NoteDAO, "add", mock_add)

    result: Note = NoteService.add_note(note)
    assert isinstance(result, Note)
    assert result.content == "Nueva nota"
    assert result.user_id == 1


def test_get_all_notes(monkeypatch: MonkeyPatch) -> None:
    mock_notes: list[Note] = [
        Note(content="Nota 1", user_id=1),
        Note(content="Nota 2", user_id=1),
    ]

    monkeypatch.setattr(NoteDAO, "query_all", lambda: mock_notes)

    result: list[Note] = NoteService.get_all_notes()

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(n, Note) for n in result)


def test_get_note_by_id_found(monkeypatch: MonkeyPatch) -> None:
    mock_note: Note = Note(content="Existente", user_id=1)
    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: mock_note)

    result: Note | None = NoteService.get_note_by_id(1)

    assert isinstance(result, Note)
    assert result.content == "Existente"


def test_get_note_by_id_not_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: None)

    result: Note | None = NoteService.get_note_by_id(99)
    assert result is None


def test_delete_note_success(monkeypatch: MonkeyPatch) -> None:
    mock_note: Note = Note(id=1, content="Borrar", user_id=1)
    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: mock_note)
    monkeypatch.setattr(NoteDAO, "delete", lambda note: True)

    result: bool = NoteService.delete_note(mock_note)
    assert result is True


def test_delete_note_not_found(monkeypatch: MonkeyPatch) -> None:
    mock_note: Note = Note(id=99, content="Inexistente", user_id=1)
    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: None)

    with pytest.raises(NotFoundAPIError) as exc_info:
        NoteService.delete_note(mock_note)

    err: NotFoundAPIError = exc_info.value
    assert err.code == CODE_NOT_EXISTS_NOTE
    assert err.message == MESSAGE_NOT_EXISTS_NOTE


def test_update_note_success(monkeypatch: MonkeyPatch) -> None:
    mock_note: Note = Note(id=1, content="Editar", user_id=1)
    data: dict[str, Any] = {"content": "Editado"}

    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: mock_note)
    monkeypatch.setattr(NoteDAO, "update", lambda n, d: True)

    result: bool = NoteService.update_note(mock_note, data)
    assert result is True


def test_update_note_not_found(monkeypatch: MonkeyPatch) -> None:
    mock_note: Note = Note(id=99, content="Inexistente", user_id=1)
    data: dict[str, Any] = {"content": "Editado"}

    monkeypatch.setattr(NoteDAO, "query_by_id", lambda _id: None)

    with pytest.raises(NotFoundAPIError) as exc_info:
        NoteService.update_note(mock_note, data)

    err: NotFoundAPIError = exc_info.value
    assert err.code == CODE_NOT_EXISTS_NOTE
    assert err.message == MESSAGE_NOT_EXISTS_NOTE
