""" Boomkarks resource fixtures """

import pytest
from webargs import fields
from app.api import register_api


@pytest.fixture
def mock_service(mocker):
    """ Mock Bookmarks """
    mock_service_class = mocker.MagicMock()
    mock_service_attrs = {
        "model.return_value": "mock_model_instance",
        "get_name.return_value": "example",
        "get.return_value": {"get": "item"},
        "delete.return_value": "service_delete",
        "add.return_value": "service_add",
        "get_all.return_value": [{"get_all": "items"}],
        "json_args": {"json": fields.String(required=True)},
        "query_args": {"query": fields.String(required=False)},
    }
    mock_service_class.configure_mock(**mock_service_attrs)
    return mock_service_class

@pytest.fixture
def client_unit_class(request, app, mock_service):  # pylint: disable=redefined-outer-name
    """ Unit test client """
    if request.cls is not None:
        register_api(app, mock_service)
        with app.test_client() as client:
            request.cls.client = client

@pytest.fixture
def mock_uuid_api(mocker):
    """ Mock uuid """
    return mocker.patch("app.api.uuid.uuid4", return_value="mock_uuid")

@pytest.fixture
def mock_app_api(mocker):
    """ Mock Flask app """
    mock_app = mocker.MagicMock()
    mock_app.add_url_rule.return_value = "mock_app_add_url_rule"
    return mock_app

@pytest.fixture
def mock_item_api(mocker):
    """ Mock ItemAPI """
    mock_item_class = mocker.patch("app.api.ItemAPI")
    mock_item_class.as_view.return_value = "mock_item_api_as_view"
    return mock_item_class

@pytest.fixture
def mock_group_api(mocker):
    """ Mock GroupAPI """
    mock_group_class = mocker.patch("app.api.GroupAPI")
    mock_group_class.as_view.return_value = "mock_group_api_as_view"
    return mock_group_class

@pytest.fixture
def mock_healthcheck(mocker):
    """ Mock Healthcheck """
    mock_healthcheck_class = mocker.patch("app.api.HealthcheckView")
    mock_healthcheck_class.as_view.return_value = "mock_healthcheck_as_view"
    return mock_healthcheck_class

@pytest.fixture
def mock_use_args(mocker):
    """ Mock use_args """
    return mocker.patch("app.api.use_args")

@pytest.fixture
def mock_use_args_wrapper(mocker):
    """ Mock use_args_wrapper """
    wrapper_return = mocker.MagicMock(return_value="callable")
    return mocker.patch("app.api.use_args_wrapper", return_value=wrapper_return)

@pytest.fixture
def mock_parsing_error(mocker):
    """ Mock parsing error """
    return mocker.MagicMock(messages={"json": "parsing_error"})

@pytest.fixture
def mock_webargs_abort(mocker):
    """ Mock webargs abort """
    return mocker.patch("app.api.webargs_abort", return_value="abort")
