import pytest
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.api import TestResource
#from app.api import BookmarksResource, BookmarkResource, TestResource
from app import create_app
#import uuid
#from app.schema import Bookmarks
#from app.schema import db, ma, Bookmarks, BookmarksSchema

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
        db = SQLAlchemy(test_app)
        db.init_app(test_app)
        api = Api(test_app)
        ma = Marshmallow(test_app)
        ma.init_app(test_app)
        api.add_resource(TestResource, '/test')
        #api.add_resource(BookmarksResource, '/bookmarks')
        #api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    elif request.config.option.env == 'test':
        # valid DB connection
        test_app = create_app()
    return test_app

# mock db objects

@pytest.fixture
def mock_bookmark_object():
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.foo.com"
    )
    return bookmark

"""
@pytest.fixture
def mock_bookmarks_object():
    bookmarks = []
    for name in ['foo', 'bar']:
        bookmarks.append(Bookmarks(
            id=uuid.uuid4(),
            url=f"https://www.{name}.com"
        ))
    return bookmarks
"""

# mock actions

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
    return mock

@pytest.fixture
def mock_get_bookmark(mocker):
    return mocker.patch("app.api.BookmarkResource.get")
