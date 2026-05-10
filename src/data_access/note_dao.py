from typing import Any

from src.configs.logger_config import setup_logger
from src.configs.sql_alchemy_config import db
from src.models.orm.note import Note

logger = setup_logger()


class NoteDAO:
    @staticmethod
    def query_all() -> list[Note]:
        return db.session.execute(db.select(Note)).scalars().all()

    @staticmethod
    def query_by_id(id: int) -> Note | None:
        return db.session.get(Note, id)

    @staticmethod
    def add(note: Note) -> Note:
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def update(note: Note, data: dict[str, Any]) -> None:
        try:
            for key, value in data.items():
                setattr(note, key, value)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            logger.error("Error updating note", exc_info=ex)
            raise

    @staticmethod
    def delete(note: Note) -> None:
        try:
            db.session.delete(note)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            logger.error("Error deleting note", exc_info=ex)
            raise
