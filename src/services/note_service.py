from typing import Any

from src.data_access.note_dao import NoteDAO
from src.models.orm.note import Note


class NoteService:
    @staticmethod
    def get_all_notes() -> list[Note]:
        return NoteDAO.query_all()

    @staticmethod
    def get_note_by_id(id: int) -> Note | None:
        return NoteDAO.query_by_id(id)

    @staticmethod
    def add_note(note: Note) -> Note:
        return NoteDAO.add(note)

    @staticmethod
    def delete_note(note: Note) -> None:
        NoteDAO.delete(note)

    @staticmethod
    def update_note(note: Note, data: dict[str, Any]) -> None:
        NoteDAO.update(note, data)
