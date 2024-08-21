""" Schema for Bookmarks """

import logging
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import make_url
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy_utils.types.uuid import UUIDType


log = logging.getLogger(__name__)

class Base(DeclarativeBase):
    """ Model class for Flask-SQLAlchemy """

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
func: callable  # E1102

def view_database_details():
    """ View database details """
    log.info(f"DB Engine : {db.engine}")
    log.info(f"DB API    : {db.engine.driver}")
    log.info(f"Dialect   : {db.engine.dialect.name}")
    for table_name in db.metadata.tables.keys():
        table = db.metadata.tables.get(table_name)
        log.info(f"{CreateTable(table).compile(db.engine)}")
        log.info(f"{table.primary_key}")

def manage_db(app, args):
    """ Manage database """
    with app.app_context():
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_name = make_url(database_uri).database
        log.info(f"Database Name: {database_name}")
        if args.view:
            log.info("Displaying database tables...")
        elif args.reset:
            log.info("Resetting database tables...")
            db.drop_all()
            db.create_all()
        elif args.remove:
            log.info("Removing database tables...")
            db.drop_all()
        else:
            log.info("Initializing database tables...")
            db.create_all()
        view_database_details()

class BaseModel(db.Model):
    """ Base model """
    __abstract__ = True
    id = db.Column(UUIDType(), primary_key=True)
    created_at = db.Column(
        db.Date,
        server_default=func.current_date(type=db.Date,inherit_cache=False)
    )

class Bookmarks(BaseModel):
    """ Bookmarks model """
    url = db.Column(db.String, index=True, unique=True, nullable=False)

    def __repr__(self):
        return f'<Bookmarks {self.id}>'


class BookmarksSchema(ma.SQLAlchemyAutoSchema):
    """ Bookmarks schema """

    class Meta:
        """ Meta class """
        model = Bookmarks
        # include_fk = True
        # include_relationships = True

    # column_name = ma.HyperlinkRelated("column_endpoint_url_for")
