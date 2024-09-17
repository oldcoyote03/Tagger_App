""" Local Test Fixtures """

import pytest
from pytest_sqlalchemy_mock.model_mocker import ModelMocker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.schema import Base
from app.api import register_api
from tests.local.data import MockData
from tests.local.example_service import ExampleService


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    """ Tables: pytest-sqlalchemy-mock for fixture mocked_session """
    return Base

@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    """ Load data: pytest-sqlalchemy-mock for fixture mocked_session """
    return [
        ("bookmarks", MockData.BOOKMARKS_DATA),
        ("example", MockData.EXAMPLE_DATA),
    ]

@pytest.fixture(scope="function")
def mocked_session_wrapper(
    mocker, mocked_session,
    sqlalchemy_declarative_base, sqlalchemy_mock_config,  # pylint: disable=redefined-outer-name
    log,
):
    """
    Session.begin side effect to create data
    cockroachdb : 
      - run_transaction expects a session that has not begun
      - when a session that is based on in-memory DB begins, there is no data
      - therefore, once run_transaction begins the session, we need to load the data
    pytest-sqlalchemy-mock : 
      - mocked_session begins the session in the fixture
      - it needs to be closed before run_transaction, otherwise it will fail
    """
    session_begin = Session.begin
    def session_begin_wrapper(nested=None):
        log.info(f"Session.begin(nested={nested})")
        if nested:
            return session_begin(mocked_session, nested)
        mocked_session.close()
        trans = session_begin(mocked_session, nested)
        log.info(f"ModelMocker.create_all : {sqlalchemy_mock_config}")
        try:
            ModelMocker(
                mocked_session, sqlalchemy_declarative_base, sqlalchemy_mock_config
            ).create_all()
            log.info("Loaded mock data")
        except IntegrityError as ie:
            log.info(f"Mock data already loaded: {ie.orig}")
        return trans
    mock_session_begin = mocker.patch("sqlalchemy.orm.session.Session.begin")
    mock_session_begin.side_effect = session_begin_wrapper
    # run_transaction expects the session instance to have right attribute at left location
    mocked_session.bind.driver = mocked_session.bind.engine.driver
    return mock_session_begin

@pytest.fixture(scope="function")
def mock_sessionmaker_mock_session(mock_sessionmaker_services, mocked_session):
    """
    Pass in pytest-sqlalchemy-mock fixture mocked_session to sqlalchemy-cockroachdb run_transaction
    """
    mock_sessionmaker_services.return_value = mocked_session
    return mock_sessionmaker_services

@pytest.fixture
def client_memory_class(
    request, client, mock_sessionmaker_mock_session, mocked_session_wrapper,  # pylint: disable=unused-argument, disable=redefined-outer-name
):
    """
    Set a ``client`` class attribute to current Flask test client::

    @pytest.mark.usefixtures('client_memory_class')
    class TestView:
        def test_resource(self):
            resp = self.client.get(url_for('resource'), resource_id="resource_id")
            assert resp.status_code == 200
    """
    if request.cls is not None:
        request.cls.client = client

@pytest.fixture
def client_example_memory(
    request, app, mock_sessionmaker_mock_session, mocked_session_wrapper,  # pylint: disable=unused-argument, disable=redefined-outer-name
):
    """ Example API """
    if request.cls is not None:
        register_api(app, ExampleService)
        with app.test_client() as client:
            request.cls.client = client
