from typing import Any

from config.logger_config import setup_logger
from config.sql_alchemy_config import db
from src.models.orm.note import Note

logger = setup_logger()


class NoteDAO:
    @staticmethod
    def query_all() -> list[Note]:
        return Note.query.all()

    @staticmethod
    def query_by_id(id: int) -> Note | None:
        return db.session.get(Note, int(id))

    @staticmethod
    def add(note: Note) -> Note:
        db.session.add(note)
        db.session.commit()

        return note

    @staticmethod
    def update(note: Note, data: dict[str, Any]) -> bool:
        try:
            note.content = data.get("content")
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            logger.error("Error updating note", exc_info=ex)
            return False

    @staticmethod
    def delete(note: Note) -> bool:
        try:
            db.session.delete(note)
            db.session.commit()
            return True
        except Exception as ex:
            db.session.rollback()
            logger.error("Error deleting note", exc_info=ex)
            return False
