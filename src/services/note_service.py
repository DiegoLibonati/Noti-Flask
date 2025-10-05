from typing import Any

from src.constants.codes import CODE_NOT_EXISTS_NOTE
from src.constants.messages import MESSAGE_NOT_EXISTS_NOTE
from src.data_access.note_dao import NoteDAO
from src.models.orm.note import Note
from src.utils.exceptions import NotFoundAPIError


class NoteService:
    @staticmethod
    def add_note(note: Note) -> Note:
        return NoteDAO.add(note)

    @staticmethod
    def get_all_notes() -> list[Note]:
        return NoteDAO.query_all()

    @staticmethod
    def get_note_by_id(id: int) -> Note | None:
        return NoteDAO.query_by_id(id)

    @staticmethod
    def delete_note(note: Note) -> bool:
        existing = NoteDAO.query_by_id(note.id)

        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_EXISTS_NOTE, message=MESSAGE_NOT_EXISTS_NOTE
            )

        return NoteDAO.delete(note)

    @staticmethod
    def update_note(note: Note, data: dict[str, Any]) -> bool:
        existing = NoteDAO.query_by_id(note.id)

        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_EXISTS_NOTE, message=MESSAGE_NOT_EXISTS_NOTE
            )

        return NoteDAO.update(note, data)
