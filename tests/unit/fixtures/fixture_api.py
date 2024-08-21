""" Boomkarks resource fixtures """

import pytest
from app.api import BookmarkResource, BookmarksResource

@pytest.fixture
def bookmark_resource():
    """ BookmarkResource """
    return BookmarkResource()

@pytest.fixture
def bookmarks_resource():
    """ BookmarksResource """
    return BookmarksResource()

@pytest.fixture
def mock_bookmarks_service_api(mocker):
    """ Mock Bookmarks """
    mock_bookmarks_service = mocker.patch("app.api.BookmarksService")
    mock_bookmarks_service.get.return_value = {"get": "bookmark"}
    mock_bookmarks_service.delete.return_value = "bookmarks_service_delete"
    mock_bookmarks_service.add.return_value = "bookmarks_service_add"
    mock_bookmarks_service.get_all.return_value = {"get_all": "bookmarks"}
    mock_bookmarks_service.filter_by.return_value = "bookmarks_service_filter_by"
    return mock_bookmarks_service

@pytest.fixture
def mock_bookmark_schema(mocker):
    """ DEPRECATED: Mock Bookmark schema """
    return mocker.patch("app.api.bookmark_schema")

@pytest.fixture
def mock_bookmark_schema_dump(mocker):
    """ DEPRECATED: Mock Bookmark schema dump """
    return mocker.patch("app.api.bookmark_schema.dump")

@pytest.fixture
def mock_sessionmaker_bm_resource(mocker):
    """ DEPRECATED: Mock sessionmaker """
    return mocker.patch("app.api.sessionmaker")

@pytest.fixture
def mock_db_engine_bm_resource(mocker):
    """ DEPRECATED: Mock db """
    return mocker.patch("app.api.db.engine")

@pytest.fixture
def mock_bookmarks_api(mocker):
    """ BookmarkResource """
    return mocker.patch("app.api.Bookmarks")

@pytest.fixture
def mock_db_bm_resource(mocker):
    """ DEPRECATED: Mock bookmark schema """
    return mocker.patch("app.api.db")
