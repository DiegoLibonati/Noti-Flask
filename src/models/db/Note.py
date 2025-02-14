from datetime import datetime
from datetime import timezone

from src.extensions import db


class Note(db.Model):
    __tablename__ = 'Note'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))