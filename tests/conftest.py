""" 
Pytest fixtures 

pytest /app/tests/unit --cov=app --cov-report=term-missing
-v : method level detail
-s : logs

python manage_db.py
python run.py

docker stop tagger-cont
docker rm tagger-cont
docker build -t tagger-img .
docker run -d -p 5000:5000 --name tagger-cont \
    -v $(pwd):/app \
    -e APP_ENV='local' \
    tagger-img
docker exec -it tagger-cont /bin/bash

"""

import os
import uuid
import datetime
from unittest import mock
import logging
from logging import config

import pytest
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError

# from app.api import TestResource, BookmarkResource, BookmarksResource
from app.config import get_logging_config
from app import create_app
from app.schema import Bookmarks


pytest_plugins = [
    'tests.unit.fixtures.app_utils',
]

def pytest_addoption(parser):
    """ Add command line options """
    parser.addoption('--env', action='store', default='development')

@pytest.fixture
def options(request):
    """ Get command line options """
    yield request.config.option

@pytest.fixture(scope="module", autouse=True)
def log(request):
    """ Module logging config """
    test_logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(test_logs_dir, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module_name = request.module.__name__
    test_logs_path = os.path.join(test_logs_dir, f"{module_name}-{now}.log")
    config.dictConfig(get_logging_config(test_logs_path))
    return logging.getLogger(module_name)

@pytest.fixture()
def app(request):
    """ Create a API client fixture """
    return create_app(request.config.option.env)

@pytest.fixture(autouse=True)
def mock_os_environ():
    """ Mock os.environ """
    with mock.patch.dict(os.environ, {}, clear=True):
        yield

@pytest.fixture
def mock_os_path_exists(mocker):
    """ Mock os.path.exists """
    return mocker.patch("os.path.exists")

@pytest.fixture
def mock_open(mocker):
    """ Mock open """
    mock_read_data = mocker.mock_open(read_data="test")
    return mocker.patch("builtins.open", mock_read_data)

@pytest.fixture
def mock_os_path_join(mocker):
    """ Mock os.path.join """
    return mocker.patch("os.path.join")

@pytest.fixture
def mock_json_loads(mocker):
    """ Mock json.loads """
    return mocker.patch("json.loads")


############################################################################

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
