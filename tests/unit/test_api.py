"""
pytest /app/tests/unit/test_bookmarks_api.py

"""

from unittest.mock import MagicMock
from flask import url_for
from app.api import SqlaNotFound


class TestHealthcheckEndpoint:
    """ Test the healthcheck endpoint """

    def test_healtcheck_endpoint(self, client):
        """ Test the healthcheck endpoint """
        response = client.get(url_for('healthcheckresource'))
        assert response.status_code == 200
        assert response.get_data().decode() == "OK"


class TestBookmarkResource:
    """ Test the bookmark resource """

    def test_get_bookmark_found(self, client, mock_bookmarks_service_api, get_data):
        """ Test the get bookmarks endpoint - found"""
        test_input = "input"
        response = client.get(url_for("bookmarkresource", bookmark_id=test_input))
        assert response.status_code == 200
        mock_bookmarks_service_api.get.assert_called_with(test_input)
        assert get_data(response) == mock_bookmarks_service_api.get.return_value

    def test_get_bookmark_not_found(self, client, mock_bookmarks_service_api, get_data):
        """ Test the get bookmarks endpoint - not found"""
        test_input = "input"
        mock_bookmarks_service_api.get.return_value = None
        expected_resp = f"Bookmark {test_input} not found"
        response = client.get(url_for("bookmarkresource", bookmark_id=test_input))
        assert response.status_code == 404
        mock_bookmarks_service_api.get.assert_called_with(test_input)
        assert get_data(response) == expected_resp

    def test_delete_bookmark(self, client, mock_bookmarks_service_api, get_data):
        """ Test the get bookmarks endpoint """
        test_input = "test_input"
        response = client.delete(url_for("bookmarkresource", bookmark_id=test_input))
        assert response.status_code == 204
        mock_bookmarks_service_api.delete.assert_called_with(test_input)
        assert get_data(response) == ""

    def test_delete_bookmark_not_found(self, client, mock_bookmarks_service_api, get_data):
        """ Test the delete bookmarks endpoint - not found """
        test_input = "test_input"
        mock_model = MagicMock()
        mock_model.__name__ = "Mock Model"
        mock_bookmarks_service_api.delete.side_effect = SqlaNotFound(mock_model, test_input)
        response = client.delete(url_for("bookmarkresource", bookmark_id=test_input))
        assert response.status_code == 404
        mock_bookmarks_service_api.delete.assert_called_with(test_input)
        expected_exc = f"SQL Not Found: model={mock_model.__name__}; record ID: {test_input}"
        assert get_data(response) == expected_exc


class TestBookmarksResource:
    """ Test the bookmarks resource """

    def test_add_bookmarks(
        self, client, mock_bookmarks_api, mock_uuid_api, mock_bookmarks_service_api, get_data
    ):
        """ Test the get bookmarks endpoint - found"""
        test_input = {"url": mock_bookmarks_api.return_value.url}
        response = client.post(url_for("bookmarksresource"), json=test_input)
        assert response.status_code == 200
        mock_bookmarks_service_api.add.assert_called_with(mock_bookmarks_api.return_value)
        assert get_data(response) == str(mock_uuid_api.return_value)

    def test_add_bookmarks_integrity_error(
        self, client, mock_bookmarks_api, mock_uuid_api, integrity_error_exc,  # pylint: disable=unused-argument
        mock_bookmarks_service_api, get_data
    ):
        """ Test the get bookmarks endpoint - found"""
        test_input = {"url": mock_bookmarks_api.return_value.url}
        mock_bookmarks_service_api.add.side_effect = integrity_error_exc
        response = client.post(url_for("bookmarksresource"), json=test_input)
        assert response.status_code == 400
        mock_bookmarks_service_api.add.assert_called_with(mock_bookmarks_api.return_value)
        expected_exc = f"Add bookmark error: {integrity_error_exc.orig}"
        assert get_data(response) == expected_exc
