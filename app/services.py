""" Bookmarks Service """

import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from app.schema import db, Bookmarks, BookmarksSchema


log = logging.getLogger(__name__)


class SqlaNotFound(Exception):
    """ SQLAlchemy Not Found """
    def __init__(self, model=None, record_id=None):
        super().__init__(f"SQL Not Found: model={model.__name__}; record ID: {record_id}")


def rt_wrapper(callback, *args, **kwargs):
    """ run_transaction wrapper for SQLAlchemy clients """
    return run_transaction(sessionmaker(db.engine), lambda s: callback(s, *args, **kwargs))

def get_callback(session, model, record_id):
    """ Get a model record by id """
    return session.get(model, record_id)

def delete_callback(session, model, record_id):
    """ Delete a model record """
    record = session.get(model, record_id)
    if not record:
        raise SqlaNotFound(model, record_id)
    session.delete(record)

def add_callback(session, record):
    """ Add a record """
    session.add(record)

def get_all_callback(session, model, **filters):
    """ Get all model records """
    stmt = select(model)
    for key, value in filters.items():
        stmt = stmt.where(getattr(model, key) == value)
    return session.scalars(stmt).all()


class SqlaRunner:
    """ SQLAlchemy interface """

    @classmethod
    def get(cls, record_id):
        """ Get a model record by id """
        return cls.schema.dump(rt_wrapper(get_callback, cls.model, record_id))  # pylint: disable=no-member

    @classmethod
    def delete(cls, record_id):
        """ Delete a model record by id """
        rt_wrapper(delete_callback, cls.model, record_id)  # pylint: disable=no-member

    @classmethod
    def add(cls, record):
        """ Get a model record by id """
        rt_wrapper(add_callback, record)

    @classmethod
    def get_all(cls, **filters):
        """ Get a model record by id """
        return cls.schema_list.dump(rt_wrapper(get_all_callback, cls.model, **filters))  # pylint: disable=no-member


class BookmarksService(SqlaRunner):
    """ Bookmarks Service """
    model = Bookmarks
    schema = BookmarksSchema()
    schema_list = BookmarksSchema(many=True)
