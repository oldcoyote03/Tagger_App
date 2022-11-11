import pytest

def pytest_addoption(parser):
    parser.addoption('--add-conn', action='store', default='false')
    
"""
@pytest.fixture
def db_conn(pytestconfig):
    return pytestconfig.getoption("db-conn")
"""

################
# unit testing #
################

import uuid
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app.api import BookmarksResource, BookmarkResource, TestResource

#from app.schema import Bookmarks
#from app.schema import db, ma, Bookmarks, BookmarksSchema

# mock flask app
@pytest.fixture
def flask_app_mock():
    app_mock = Flask(__name__)
    db = SQLAlchemy(app_mock)
    db.init_app(app_mock)
    api = Api(app_mock)
    ma = Marshmallow(app_mock)
    ma.init_app(app_mock)
    api.add_resource(BookmarksResource, '/bookmarks')
    api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    api.add_resource(TestResource, '/test')
    return app_mock

# mock db objects

"""
@pytest.fixture
def mock_bookmark_object():
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.foo.com"
    )
    return bookmark

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

"""
@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value = mocker.Mock()
    return mock

@pytest.fixture
def mock_get_bookmark(mocker):
    return mocker.patch("app.api.BookmarkResource.get")
"""


#######################
# integration testing #
#######################

from app import create_app

db_arg = pytest.config.getoption('--db-conn')
if db_arg and db_arg == "True":
    @pytest.fixture
    def app():
        app = create_app()
        return app
