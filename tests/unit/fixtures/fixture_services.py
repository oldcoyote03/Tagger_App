""" SQLAlchemy Fixtures """

import pytest
from app.services import SqlaRunner


@pytest.fixture
def mock_sessionmaker_services(mocker):
    """ Mock Bookmarks """
    return mocker.patch("app.services.sessionmaker")

@pytest.fixture
def mock_sqla_attrs():
    """ Mock Bookmarks """
    yield SqlaRunner
    for attr in ["model", "schema"]:
        if hasattr(SqlaRunner, attr):
            delattr(SqlaRunner, attr)

@pytest.fixture
def mock_model(mocker):
    """ Mock Bookmarks """
    mock_generic = mocker.MagicMock()
    mock_generic.__name__ = "mock Generic Model"
    mock_generic.id = "mock_id"
    return mock_generic

@pytest.fixture
def mock_schema(mocker):
    """ Mock Bookmarks """
    mock_generic = mocker.MagicMock()
    mock_generic.dump.return_value = "mock Generic Schema"
    return mock_generic

@pytest.fixture
def mock_bookmarks_services(mocker):
    """ Mock Bookmarks """
    mock_bookmarks = mocker.patch("app.services.Bookmarks")
    mock_bookmarks.__name__ = "mock Bookmarks"
    return mock_bookmarks

@pytest.fixture
def mock_run_transaction_services(mocker):
    """ Mock Bookmarks """
    return mocker.patch("app.services.run_transaction")

@pytest.fixture
def mock_rt_wrapper(mocker):
    """ Mock Bookmarks """
    mock_sqla_rt = mocker.patch("app.services.rt_wrapper")
    mock_sqla_rt.return_value = "rt_wrapper_response"
    return mock_sqla_rt

@pytest.fixture
def mock_db_services(mocker):
    """ Mock db """
    mock_db = mocker.patch("app.services.db")
    mock_db.engine = None
    return mock_db

@pytest.fixture
def mock_session(mocker):
    """ Mock Session.get """
    mock_session_obj = mocker.patch("sqlalchemy.orm.session.Session")
    mock_session_obj.get.return_value = "session_get"
    mock_session_obj.delete.return_value = "session_delete"
    mock_session_obj.add.return_value = "session_add"
    return mock_session_obj

@pytest.fixture
def mock_session_get(mocker):
    """ Mock Session.get """
    sqla_session_get = mocker.patch("app.services.SqlaRunner.session_get")
    sqla_session_get.return_value="session_get"
    return sqla_session_get

@pytest.fixture
def mock_session_delete(mocker):
    """ Mock Session.delete """
    sqla_session_delete = mocker.patch("app.services.SqlaRunner.session_delete")
    sqla_session_delete.return_value="session_delete"
    return sqla_session_delete

@pytest.fixture
def mock_session_add_sqlalchemy(mocker):
    """ Mock session.add """
    return mocker.patch("sqlalchemy.orm.session.Session.add")

@pytest.fixture
def mock_get_sqlalchemy(mocker):
    """ DEPRECATED: Mock get_or_404 """
    return mocker.patch("flask_sqlalchemy._QueryProperty.__get__").return_value

@pytest.fixture
def mock_session_commit_sqlalchemy(mocker):
    """ DEPRECATED: Mock session.commit """
    return mocker.patch("sqlalchemy.orm.Session.commit")
