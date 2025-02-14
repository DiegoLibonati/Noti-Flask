import logging

from flask_sqlalchemy import SQLAlchemy

from src.extensions import db as db_extension
from src.models.db.Note import Note


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class NoteRepository:
    def __init__(self, db: SQLAlchemy = db_extension) -> None:
        self.db = db

    def get_notes(self) -> list[Note]:
        return Note.query.all()

    def get_note_by_id(self, id: int) -> Note:
        return self.db.session.get(Note, int(id))
    
    def add_note(self, user_id: str, content: str = "") -> Note:
        try:
            note = Note(content=content, user_id=int(user_id))
        
            self.db.session.add(note)
            self.db.session.commit()

            return note
        except Exception as ex:
            logging.info(ex)
            return False
        
    def remove_note(self, note: Note) -> bool:
        try:
            self.db.session.delete(instance=note)
            self.db.session.commit()

            return True
        except Exception as ex:
            logging.info(ex)
            return False