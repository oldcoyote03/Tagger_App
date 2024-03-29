import pytest
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.api import TestResource, BookmarkResource, BookmarksResource
from app import create_app
from app.schema import Bookmarks
import uuid
import datetime

def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='dev')

"""
@pytest.fixture
def options(request):
    yield request.config.option
"""

@pytest.fixture
def app(request):
    test_app = None
    if request.config.option.env == 'dev':
        # mock app
        test_app = Flask(__name__)
        test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = SQLAlchemy(test_app)
        db.init_app(test_app)
        api = Api(test_app)
        ma = Marshmallow(test_app)
        ma.init_app(test_app)
        api.add_resource(TestResource, '/test')
        api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
        api.add_resource(BookmarksResource, '/bookmarks')
    elif request.config.option.env == 'test':
        # valid DB connection
        test_app = create_app()
    return test_app

# db objects

@pytest.fixture
def bookmark_obj():
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.foo.com",
        created_at=datetime.date.today()
    )
    return bookmark

from werkzeug.exceptions import NotFound
@pytest.fixture
def not_found_exc():
    return NotFound

from sqlalchemy.exc import IntegrityError
@pytest.fixture
def integrity_error_exc():
    return IntegrityError('Mock', ['mock'], IntegrityError)


@pytest.fixture
def bookmarks_obj():
    bookmarks = []
    for name in ['foo', 'bar']:
        bookmarks.append(Bookmarks(
            id=uuid.uuid4(),
            url=f"https://www.{name}.com"
        ))
    return bookmarks

@pytest.fixture
def bookmarks_filter_obj():
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url=f"https://www.foo.com"
    )
    return [bookmark]

# mock actions
# https://pytest-mock.readthedocs.io/en/latest/

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    return mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value

@pytest.fixture
def mock_session_delete_sqlalchemy(mocker):
    return mocker.patch("sqlalchemy.orm.Session.delete")

@pytest.fixture
def mock_session_add_sqlalchemy(mocker):
    return mocker.patch("sqlalchemy.orm.Session.add")

@pytest.fixture
def mock_session_commit_sqlalchemy(mocker):
    return mocker.patch("sqlalchemy.orm.Session.commit")
