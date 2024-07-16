""" Pytest fixtures """

import os
import uuid
import datetime

import pytest
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError

# from app.api import TestResource, BookmarkResource, BookmarksResource
from app import create_app
from app.schema import Bookmarks

def pytest_addoption(parser):
    """ Add command line options """
    parser.addoption('--env', action='store', default='dev')

@pytest.fixture
def app(request):
    """ Create a test app """
    if request.config.option.env == 'dev':
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return create_app()

# @pytest.fixture
# def options(request):
#     """ Get command line options """
#     yield request.config.option

@pytest.fixture
def bookmark_obj():
    """ Bookmark object """
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.foo.com",
        created_at=datetime.date.today()
    )
    return bookmark

@pytest.fixture
def not_found_exc():
    """ Not found exception """
    return NotFound

@pytest.fixture
def integrity_error_exc():
    """ Integrity error exception """
    return IntegrityError('Mock', ['mock'], IntegrityError)

@pytest.fixture
def bookmarks_obj():
    """ Bookmarks object """
    bookmarks = []
    for name in ['foo', 'bar']:
        bookmarks.append(Bookmarks(
            id=uuid.uuid4(),
            url=f"https://www.{name}.com"
        ))
    return bookmarks

@pytest.fixture
def bookmarks_filter_obj():
    """ Bookmarks object """
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.foo.com"
    )
    return [bookmark]

# mock actions
# https://pytest-mock.readthedocs.io/en/latest/

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    """ Mock get_or_404 """
    return mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value

@pytest.fixture
def mock_session_delete_sqlalchemy(mocker):
    """ Mock session.delete """
    return mocker.patch("sqlalchemy.orm.Session.delete")

@pytest.fixture
def mock_session_add_sqlalchemy(mocker):
    """ Mock session.add """
    return mocker.patch("sqlalchemy.orm.Session.add")

@pytest.fixture
def mock_session_commit_sqlalchemy(mocker):
    """ Mock session.commit """
    return mocker.patch("sqlalchemy.orm.Session.commit")
