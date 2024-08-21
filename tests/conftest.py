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
import json
import uuid
import datetime
import logging

import pytest
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError

# from app.api import TestResource, BookmarkResource, BookmarksResource
from app.config import get_logging_config
from app import create_app
from app.schema import Bookmarks


pytest_plugins = [
    "tests.unit.fixtures.fixture_api",
    "tests.unit.fixtures.fixture_schema",
    "tests.unit.fixtures.fixture_services",
    "tests.unit.fixtures.fixture_utils",
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
    logging.config.dictConfig(get_logging_config(test_logs_path))
    return logging.getLogger(module_name)

@pytest.fixture()
def app(request):
    """ Create a API client fixture """
    return create_app(request.config.option.env)

@pytest.fixture(autouse=True)
def mock_os_environ(mocker):
    """ Mock os.environ """
    return mocker.patch.dict(os.environ, {}, clear=True)

@pytest.fixture(autouse=True)
def mock_sys_argv(mocker):
    """ Mock CLI args list """
    return mocker.patch("sys.argv", [])

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

@pytest.fixture
def get_data():
    """ Parse response function """
    def func(response):
        try:
            return json.loads(response.get_data())
        except json.decoder.JSONDecodeError:
            return response.get_data().decode()
    return func



############################################################################

@pytest.fixture
def bookmark_obj():
    """ Bookmark object """
    bookmark = Bookmarks(
        id=uuid.uuid4(),
        url="https://www.test.com",
        created_at=datetime.date(2000, 1, 1)
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
            url=f"https://www.{name}.com",
            created_at=datetime.date(2000, 1, 1)
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
