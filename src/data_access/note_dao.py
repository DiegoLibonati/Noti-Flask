from typing import Any

from src.configs.sql_alchemy_config import db
from src.models.orm.note import Note
from src.utils.commit_or_rollback_decorator import commit_or_rollback_decorator


class NoteDAO:
    @staticmethod
    def query_all() -> list[Note]:
        return list(db.session.execute(db.select(Note)).scalars().all())

    @staticmethod
    def query_by_id(id: int) -> Note | None:
        return db.session.get(Note, id)

    @staticmethod
    @commit_or_rollback_decorator("adding note")
    def add(note: Note) -> Note:
        db.session.add(note)
        return note

    @staticmethod
    @commit_or_rollback_decorator("updating note")
    def update(note: Note, data: dict[str, Any]) -> None:
        for key, value in data.items():
            setattr(note, key, value)

    @staticmethod
    @commit_or_rollback_decorator("deleting note")
    def delete(note: Note) -> None:
        db.session.delete(note)
