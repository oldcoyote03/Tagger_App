""" Schema for Bookmarks """

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy.types import Uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

db = SQLAlchemy()
ma = Marshmallow()

class Bookmarks(db.Model):
    """ Bookmarks schema """

    id = db.Column(Uuid(native_uuid=True), primary_key=True)
    # id = db.Column(db.String, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True)  # behaves like UUID
    # id = db.Column(UUID(as_uuid=False), primary_key=True)  # behaves like str
    url = db.Column(db.String, index=True, unique=True, nullable=False)
    created_at = db.Column(
        db.Date,
        server_default=func.current_date(type=db.Date,inherit_cache=False)
    )

    def __repr__(self):
        return f'<Bookmarks {self.id}>'


class BookmarksSchema(ma.SQLAlchemyAutoSchema):
    """ Bookmarks schema """

    class Meta:
        """ Meta class """
        model = Bookmarks
