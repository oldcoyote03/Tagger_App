"""
pytest /app/tests/unit/test_bookmarks_api.py

"""

from unittest.mock import MagicMock, call
import pytest
from flask import url_for
from app.api import (
    SqlaNotFound, register_api, register_healthcheck, use_args_wrapper,
    use_args_json, use_args_query, handle_request_parsing_error
)

class TestHealthcheckEndpoint:
    """ Test the healthcheck endpoint """

    def test_healtcheck_endpoint(self, client):
        """ Test the healthcheck endpoint """
        response = client.get(url_for('healthcheck'))
        assert response.status_code == 200
        assert response.get_data().decode() == "OK"


@pytest.mark.usefixtures("client_unit_class")
class TestServiceItemView:
    """ Test the item view """

    def test_get_item_found(self, mock_service, get_data):
        """ Test the get item endpoint - found"""
        test_item_id = "test_item_id"
        response = self.client.get(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        mock_service.get.assert_called_once_with(str(test_item_id))
        assert get_data(response) == mock_service.get.return_value
        assert response.status_code == 200

    def test_get_item_not_found(self, mock_service, get_data):
        """ Test the get item endpoint - not found"""
        test_item_id = "test_item_id"
        mock_service.get.return_value = None
        expected_resp = f"{mock_service.get_name()} {test_item_id} not found"
        response = self.client.get(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        mock_service.get.assert_called_with(test_item_id)
        assert response.status_code == 404
        assert get_data(response) == expected_resp

    def test_delete_item(self, mock_service, get_data):
        """ Test the delete item endpoint """
        test_item_id = "test_item_id"
        response = self.client.delete(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        mock_service.delete.assert_called_with(test_item_id)
        assert response.status_code == 204
        assert get_data(response) == ""


    def test_delete_item_not_found(self, mock_service, get_data):
        """ Test the delete item endpoint - not found """
        test_item_id = "test_item_id"
        mock_model = MagicMock()
        mock_model.__name__ = "Mock Model"
        mock_service.delete.side_effect = SqlaNotFound(mock_model, test_item_id)
        response = self.client.delete(url_for("example-item", item_id=test_item_id))  # pylint: disable=no-member
        mock_service.delete.assert_called_with(test_item_id)
        expected_exc = f"{mock_service.get_name()} {test_item_id} not found"
        assert response.status_code == 404
        assert get_data(response) == expected_exc


@pytest.mark.usefixtures("client_unit_class")
class TestServiceGroupView:
    """ Test the service group view """

    def test_get_group(self, mock_service, get_data):
        """ Test the get group endpoint """
        key = "query"
        arg = "test_query"
        response = self.client.get(f"{url_for('example-group')}?{key}={arg}")  # pylint: disable=no-member
        mock_service.get_all.assert_called_once_with(**{key: arg})
        assert response.status_code == 200
        assert get_data(response) == mock_service.get_all.return_value

    def test_add_item(self, mock_service, get_data):
        """ Test the add item endpoint"""
        test_payload = {"json": "payload"}
        response = self.client.post(url_for("example-group"), json=test_payload)  # pylint: disable=no-member
        mock_service.model.assert_called_with(**test_payload)
        mock_service.add.assert_called_with(mock_service.model.return_value)
        assert response.status_code == 200
        assert get_data(response) == mock_service.get_all.return_value[0].get("id")

    def test_add_item_integrity_error(
        self, mock_service, integrity_error_exc, get_data
    ):
        """ Test the get bookmarks endpoint - found"""
        test_payload = {"json": "payload"}
        mock_service.add.side_effect = integrity_error_exc
        response = self.client.post(url_for("example-group"), json=test_payload)  # pylint: disable=no-member
        mock_service.model.assert_called_with(**test_payload)
        mock_service.add.assert_called_with(mock_service.model.return_value)
        expected_exc = f"Add {mock_service.get_name.return_value} error: {integrity_error_exc.orig}"
        assert response.status_code == 400
        assert get_data(response) == expected_exc

def test_register_api(mock_app_api, mock_service, mock_item_api, mock_group_api):
    """ Test the register_api function """
    register_api(mock_app_api, mock_service)
    mock_service.get_name.assert_called_once_with()
    mock_item_api.as_view.assert_called_once_with(
        f"{mock_service.get_name.return_value}-item", mock_service,
    )
    mock_group_api.as_view.assert_called_once_with(
        f"{mock_service.get_name.return_value}-group", mock_service,
    )
    mock_app_api.add_url_rule.assert_has_calls([
        call(
            f"/{mock_service.get_name.return_value}/<item_id>",
            view_func=mock_item_api.as_view.return_value
        ),
        call(
            f"/{mock_service.get_name.return_value}/",
            view_func=mock_group_api.as_view.return_value
        ),
    ])

def test_register_healthcheck(mock_app_api, mock_healthcheck):
    """ Test the register_healthcheck function """
    register_healthcheck(mock_app_api)
    mock_healthcheck.as_view.assert_called_once_with("healthcheck")
    mock_app_api.add_url_rule.assert_called_once_with(
        "/healthcheck", view_func=mock_healthcheck.as_view.return_value
    )

def test_use_args_wrapper(mock_service, mock_use_args):
    """ Test the use_args_json decorator """
    mock_view_method = MagicMock()
    location = "json"
    decorated_view = use_args_wrapper(mock_view_method, location)
    mock_self = MagicMock(service=mock_service)
    arg1 = "arg1"
    kwarg1 = "kwarg1"
    decorated_view(mock_self, arg1, kwarg1=kwarg1)
    mock_use_args.assert_called_once_with(mock_service.json_args, location=location)
    mock_use_args.return_value.assert_called_once_with(mock_view_method)
    mock_use_args.return_value.return_value.assert_called_once_with(mock_self, arg1, kwarg1=kwarg1)

def test_use_args_json(mock_use_args_wrapper):
    """ Test the use_args_json decorator """
    mock_view_method = MagicMock()
    decorated_view = use_args_json(mock_view_method)
    mock_use_args_wrapper.assert_called_once_with(mock_view_method, "json")
    assert decorated_view() == mock_use_args_wrapper.return_value.return_value

def test_use_args_query(mock_use_args_wrapper):
    """ Test the use_args_query decorator """
    mock_view_method = MagicMock()
    decorated_view = use_args_query(mock_view_method)
    mock_use_args_wrapper.assert_called_once_with(mock_view_method, "query")
    assert decorated_view() == mock_use_args_wrapper.return_value.return_value

def test_handle_request_parsing_error(mock_parsing_error, mock_webargs_abort):
    """ Test the handle_request_parsing_error function """
    handle_request_parsing_error(mock_parsing_error)
    mock_webargs_abort.assert_called_once_with(422, errors=mock_parsing_error.messages.get("json"))
