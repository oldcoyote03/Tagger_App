"""
pytest /app/tests/integration/test_bookmarks_api.py --env=local

"""

from uuid import UUID
import pytest
from flask import url_for


@pytest.mark.usefixtures('client_class')
@pytest.mark.usefixtures('setup_test_bookmarks')
class TestBookmarksApi:
    """ Test the Bookmarks API """

    def test_bookmarks_api(self, get_data, bookmarks_urls, log):
        """ Test the /bookmarks endpoint """

        # Get all bookmarks - empty DB
        response = self.client.get(url_for("bookmarks-group"))  # pylint: disable=no-member
        log.info(f"Initialized DB: {get_data(response)}")
        assert response.status_code == 200
        assert len(get_data(response)) == 0

        # Add bookmark
        response = self.client.post(url_for("bookmarks-group"), json=bookmarks_urls[0])  # pylint: disable=no-member
        assert response.status_code == 200
        test_bookmark_id = get_data(response)
        assert UUID(test_bookmark_id)

        # Adding the same bookmark URL raises an IntegrityError
        response = self.client.post(url_for("bookmarks-group"), json=bookmarks_urls[0])  # pylint: disable=no-member
        assert response.status_code == 400
        assert get_data(response) == "Add bookmarks error: UNIQUE constraint failed: bookmarks.url"

        # Get bookmark
        response = self.client.get(url_for("bookmarks-item", item_id=test_bookmark_id))  # pylint: disable=no-member
        test_bookmark = get_data(response)
        assert response.status_code == 200
        assert test_bookmark.get("id") == test_bookmark_id
        assert test_bookmark.get("url") == bookmarks_urls[0].get("url")

        # Get bookmarks - filter by URL
        response = self.client.post(url_for("bookmarks-group"), json=bookmarks_urls[1])  # pylint: disable=no-member
        assert response.status_code == 200
        response = self.client.get(url_for("bookmarks-group"))  # pylint: disable=no-member
        assert response.status_code == 200
        assert len(get_data(response)) == 2

        response = self.client.get(url_for('bookmarks-group', **bookmarks_urls[1]))  # pylint: disable=no-member
        assert response.status_code == 200
        assert len(get_data(response)) == 1
        assert get_data(response)[0].get("url") == bookmarks_urls[1].get("url")

        # Delete bookmark
        response = self.client.delete(url_for("bookmarks-item", item_id=test_bookmark_id))  # pylint: disable=no-member
        assert response.status_code == 204
        assert get_data(response) == ""

        # Not found
        expected_data = f"bookmarks {test_bookmark_id} not found"
        response = self.client.get(url_for("bookmarks-item", item_id=test_bookmark_id))  # pylint: disable=no-member
        assert response.status_code == 404
        assert get_data(response) == expected_data

        response = self.client.delete(url_for("bookmarks-item", item_id=test_bookmark_id))  # pylint: disable=no-member
        assert response.status_code == 404
        assert get_data(response) == expected_data
