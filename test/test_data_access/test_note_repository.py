from typing import Any

from src.data_access.note_repository import NoteRepository
from src.data_access.user_repository import UserRepository
from src.models.db.Note import Note


def test_add_note(user_repository: UserRepository, note_repository: NoteRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")
    password = mock_user.get("password")
    email = mock_user.get("email")

    user = user_repository.add_user(username=username, password=password, email=email)
    note = note_repository.add_note(user_id=user.id)

    assert note
    assert isinstance(note, Note)


def test_get_notes(note_repository: NoteRepository) -> None:
    notes = note_repository.get_notes()

    assert notes


def test_get_note_by_id(note_repository: NoteRepository) -> None:
    notes = note_repository.get_notes()
    last_note = notes[len(notes) - 1]

    note = note_repository.get_note_by_id(id=last_note.id)

    assert note
    assert isinstance(note, Note)


def test_remove_note(user_repository: UserRepository, note_repository: NoteRepository, mock_user: dict[str, Any]) -> None:
    username = mock_user.get("username")

    notes = note_repository.get_notes()
    
    last_note = notes[len(notes) - 1]
    user = user_repository.get_user_by_username(username=username)

    remove_note = note_repository.remove_note(note=last_note)
    remove_user = user_repository.remove_user(user=user)
    
    assert remove_note
    assert remove_user