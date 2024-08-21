""" Bookmarks Service """

import logging
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


class SqlaRunner:
    """ SQLAlchemy interface """

    @classmethod
    def session_get(cls, session, record_id):
        """ Get a model record by id """
        return session.get(cls.model, record_id)  # pylint: disable=no-member

    # @classmethod
    # def session_add(cls, session, record):
    #     """ Add a model record """
    #     return session.add(record)  # pylint: disable=no-member

    @classmethod
    def session_delete(cls, session, record):
        """ Delete a model record """
        return session.delete(record)  # pylint: disable=no-member

    @classmethod
    def get_callback(cls, session, record_id):
        """ Get callback """
        return cls.schema.dump(cls.session_get(session, record_id))  # pylint: disable=no-member

    @classmethod
    def get(cls, record_id):
        """ Get a model record by id """
        return rt_wrapper(cls.get_callback, record_id)

    @classmethod
    def delete_callback(cls, session, record_id):
        """ Delete callback """
        record = cls.session_get(session, record_id)
        if not record:
            raise SqlaNotFound(cls.model, record_id)  # pylint: disable=no-member
        return cls.session_delete(session, record)

    @classmethod
    def delete(cls, record_id):
        """ Delete a model record by id """
        return rt_wrapper(cls.delete_callback, record_id)


class BookmarksService(SqlaRunner):
    """ Bookmarks Service """
    model = Bookmarks
    schema = BookmarksSchema()
