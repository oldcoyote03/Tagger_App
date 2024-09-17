""" Bookmarks Service """

import os
import logging
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from webargs import fields
from app.schema import db, Bookmarks, BookmarksSchema


log = logging.getLogger(__name__)


class SqlaNotFound(Exception):
    """ SQLAlchemy Not Found """
    def __init__(self, model=None, record_id=None):
        super().__init__(f"SQL Not Found: model={model.__name__}; record ID: {record_id}")


def rt_wrapper(callback, *args, **kwargs):
    """ run_transaction wrapper for SQLAlchemy clients """
    # log.info(f"conn type                    : {type(conn)}")  # temp
    # log.info(f"conn.bind.driver             : {conn.bind.driver}")  # temp
    return run_transaction(
        sessionmaker(db.engine),
        lambda s: callback(s, *args, **kwargs),
        max_retries=os.environ.get("DATABASE_MAX_RETRIES", 0),
    )

def get_callback(session, model, schema, record_id):
    """ Get a model record by id """
    return schema.dump(session.get(model, record_id))

def delete_callback(session, model, record_id):
    """ Delete a model record """
    record = session.get(model, record_id)
    if not record:
        raise SqlaNotFound(model, record_id)
    session.delete(record)

def add_callback(session, record):
    """ Add a record """
    session.add(record)

def get_all_callback(session, model, schema, **filters):
    """ Get all model records """
    stmt = select(model)
    for key, value in filters.items():
        stmt = stmt.where(getattr(model, key) == value)
    return schema.dump(session.scalars(stmt).all())


class SqlaRunner:
    """ SQLAlchemy interface """

    @classmethod
    def get_name(cls):
        """ Model name """
        return cls.model.__name__.lower()  # pylint: disable=no-member

    @classmethod
    def get(cls, record_id):
        """ Get a model record by id """
        return rt_wrapper(get_callback, cls.model, cls.schema, record_id)  # pylint: disable=no-member

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
        return rt_wrapper(get_all_callback, cls.model, cls.schema_list, **filters)  # pylint: disable=no-member


class BookmarksService(SqlaRunner):
    """ Bookmarks Service """
    model = Bookmarks
    schema = BookmarksSchema()
    schema_list = BookmarksSchema(many=True)
    query_args = {'url': fields.String(required=False)}
    json_args = {'url': fields.String(required=True)}
