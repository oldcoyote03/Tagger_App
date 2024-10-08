""" SQLAlchemy Fixtures """

import pytest
from app.services import SqlaRunner


@pytest.fixture
def mock_sessionmaker_services(mocker):
    """ Mock Bookmarks """
    return mocker.patch("app.services.sessionmaker", return_value="test_session")

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
    mock_generic.__name__ = "mock_model"
    mock_generic.id = "mock_id"
    return mock_generic

@pytest.fixture
def mock_schema(mocker):
    """ Mock Bookmarks """
    mock_generic = mocker.MagicMock()
    mock_generic.dump.return_value = "mock_schema"
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
    mock_scalars_instance = mocker.MagicMock()
    mock_scalars_instance.all.return_value = "session_scalars_all"
    mock_scalars = mocker.MagicMock()
    mock_scalars.return_value = mock_scalars_instance
    mock_session_attrs = {
        "get.return_value": "session_get",
        "delete.return_value": "session_delete",
        "add.return_value": "session_add",
        "scalars": mock_scalars,
    }
    mock_session_obj = mocker.patch("sqlalchemy.orm.session.Session")
    mock_session_obj.configure_mock(**mock_session_attrs)
    return mock_session_obj

@pytest.fixture
def mock_select(mocker):
    """ Mock Session.get """
    mock_where_prev = "mock_where"
    for _ in range(3):
        mock_where_attrs = {
            "__str__.return_value": "mock_stmt",
            "where.return_value": mock_where_prev,
        }
        mock_where = mocker.MagicMock()
        mock_where.configure_mock(**mock_where_attrs)
        mock_where_prev = mock_where
    mock_select_obj_attrs = {
        "__str__.return_value": "mock_select",
        "return_value": mock_where,
    }
    mock_select_obj = mocker.MagicMock()
    mock_select_obj.configure_mock(**mock_select_obj_attrs)
    mock_select_func = mocker.patch("app.services.select", return_value=mock_select_obj)
    return mock_select_func

@pytest.fixture
def mock_get_callback(mocker):
    """ Mock Session.get """
    mock_get_callback_func = mocker.patch("app.services.get_callback")
    mock_get_callback_func.return_value = "mock_get_callback"
    return mock_get_callback_func
