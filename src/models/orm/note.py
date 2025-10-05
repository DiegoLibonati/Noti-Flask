from datetime import datetime, timezone
from typing import Any

from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column

from config.sql_alchemy_config import db


class Note(db.Model):
    __tablename__ = "Note"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(db.String(250))
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("User.id"))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        if not getattr(self, "created_at", None):
            self.created_at: datetime = datetime.now(timezone.utc)


@event.listens_for(Note, "load")
@event.listens_for(Note, "refresh")
def ensure_utc_timezone(note: Note, *_: Any) -> None:
    if note.created_at and note.created_at.tzinfo is None:
        note.created_at = note.created_at.replace(tzinfo=timezone.utc)
