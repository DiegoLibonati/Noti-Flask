from datetime import UTC, datetime
from typing import Any

from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.sql_alchemy_config import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(20), unique=True)
    email: Mapped[str] = mapped_column(db.String(150), unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    notes = db.relationship("Note", cascade="all, delete", backref="user")

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        if not getattr(self, "created_at", None):
            self.created_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }


@event.listens_for(User, "load")
@event.listens_for(User, "refresh")
def ensure_utc_timezone(user: User, *_: Any) -> None:
    if user.created_at and user.created_at.tzinfo is None:
        user.created_at = user.created_at.replace(tzinfo=UTC)
