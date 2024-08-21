""" Local Test Fixtures """

import pytest
from pytest_sqlalchemy_mock.model_mocker import ModelMocker
from sqlalchemy.orm.session import Session
from app.schema import Base
from tests.local.data import MockData


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    """ Tables: pytest-sqlalchemy-mock for fixture mocked_session """
    return Base

@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    """ Load data: pytest-sqlalchemy-mock for fixture mocked_session """
    return [("bookmarks", MockData.BOOKMARKS_DATA)]

@pytest.fixture(scope="function")
def mocked_session_wrapper(
    mocker, mocked_session,
    sqlalchemy_declarative_base, sqlalchemy_mock_config  # pylint: disable=redefined-outer-name
):
    """
    Session.begin side effect to create data
    cockroachdb : 
      - run_transaction expects a session that has not begun
      - when a session that is based on in-memory DB is begins, there is no data
      - therefore, once run_transaction begins the session, we need to load the data
    pytest-sqlalchemy-mock : 
      - mocked_session begins the session in the fixture
      - it needs to be closed before run_transaction, otherwise it will fail
    """
    session_begin = Session.begin
    def session_begin_wrapper(nested=None):
        trans = session_begin(mocked_session, nested)
        if not nested:
            ModelMocker(
                mocked_session, sqlalchemy_declarative_base, sqlalchemy_mock_config
            ).create_all()
        return trans
    mock_session_begin = mocker.patch("sqlalchemy.orm.session.Session.begin")
    mock_session_begin.side_effect = session_begin_wrapper
    mocked_session.close()
    return mock_session_begin

@pytest.fixture
def mock_sessionmaker_mock_session(mock_sessionmaker_services, mocked_session):
    """
    Mock sessionmaker
    Pass in pytest-sqlalchemy-mock fixture mocked_session to sqlalchemy-cockroachdb run_transaction
    """
    mock_sessionmaker_services.return_value = mocked_session
    return mock_sessionmaker_services

@pytest.fixture
def client_memory_class(
    request, client,
    mock_sessionmaker_mock_session,  # pylint: disable=unused-argument, disable=redefined-outer-name
    mocked_session_wrapper,  # pylint: disable=unused-argument, disable=redefined-outer-name
):
    """
    Set a ``client`` class attribute to current Flask test client::

    @pytest.mark.usefixtures('client_memory_class')
    class TestView:

        def test_login(self, email, password):
            credentials = {'email': email, 'password': password}
            return self.client.post(url_for('login'), data=credentials)
            assert self.login('foo@example.com', 'pass').status_code == 200

    """
    if request.cls is not None:
        request.cls.client = client
