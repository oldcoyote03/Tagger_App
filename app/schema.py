from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import date

db = SQLAlchemy()
ma = Marshmallow()

class Bookmarks(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    url = db.Column(db.String, index=True, unique=True, nullable=False)
    created_at = db.Column(
        db.Date,
        server_default=func.current_date(type=db.Date,inherit_cache=False)
    )

    def __repr__(self):
        return f'<Bookmarks {self.id}>'


class BookmarksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bookmarks
