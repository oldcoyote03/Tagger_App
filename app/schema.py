""" Schema for Bookmarks """

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy_utils.types.uuid import UUIDType
from sqlalchemy.types import Uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

db = SQLAlchemy()
ma = Marshmallow()

class Bookmarks(db.Model):
    """ Bookmarks schema """

    # cbd resolves to BINARY; sqlite resolves to ?
    # no type conversion at API layer
    id = db.Column(UUIDType(), primary_key=True)  # cdb resolves to BINARY
    
    # all resolve to CHAR
    # no type conversions at API layer
    # id = db.Column(Uuid(native_uuid=True), primary_key=True)

    # cdb    : resolves to UUID
    # sqlite : behaves like UUID, i.e. GET /.../<id> convert to UUID
    # id = db.Column(UUID(as_uuid=True), primary_key=True)

    # all resolve to CHAR
    # POST /... convert UUID to str
    # id = db.Column(db.String, primary_key=True)

    # cdb    : resolves to CHAR
    # sqlite : behaves like str, i.e. POST /... convert UUID to str
    # id = db.Column(UUID(as_uuid=False), primary_key=True)

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
