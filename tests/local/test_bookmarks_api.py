"""
pytest /app/tests/local/test_bookmarks_api.py

"""

import pytest
from flask import url_for
from tests.local.data import MockData


@pytest.mark.usefixtures("client_memory_class")
class TestBookmarksApi:
    """ Test the Bookmarks API """

    def test_get_bookmark(self, get_data, log):
        """ Test the get single bookmark endpoint """
        test_bookmark_raw = MockData.BOOKMARKS_DATA[1]
        test_bookmark = {
            "id": str(test_bookmark_raw.get("id")),
            "url": test_bookmark_raw.get("url"),
            "created_at": str(test_bookmark_raw.get("created_at")),
        }
        log.info(f"test_bookmark: {test_bookmark}")
        response = self.client.get(  # pylint: disable=no-member
            url_for('bookmarkresource', bookmark_id=test_bookmark.get("id"))
        )
        assert get_data(response) == test_bookmark

    def test_delete_bookmarks_found(self, get_data):
        """ Test the delete endpont """
        test_bookmark = MockData.BOOKMARKS_DATA[1]
        test_bookmark_id = str(test_bookmark.get("id"))
        response = self.client.delete(  # pylint: disable=no-member
            url_for('bookmarkresource', bookmark_id=test_bookmark_id)
        )
        assert response.status_code == 204
        assert get_data(response) == ""

    def test_delete_bookmarks_not_found(self, get_data, log):
        """ Test the delete endpont """
        test_bookmark_id = "9f03ef77-6501-449f-8902-0eca657e9db9"
        response = self.client.delete(  # pylint: disable=no-member
            url_for('bookmarkresource', bookmark_id=test_bookmark_id)
        )
        log.info(f"response: {get_data(response)}")
        assert response.status_code == 404
        expected_data = f"SQL Not Found: model=Bookmarks; record ID: {test_bookmark_id}"
        assert get_data(response) == expected_data

    # def test_get_bookmarks(self, client, log):
    #     """ Test the get bookmarks endpoint - all bookmarks """
    #     test_bookmark_raw = MockData.BOOKMARKS_DATA
    #     test_bookmarks = []
    #     for bm in test_bookmark_raw:
    #         test_bm = dict(bm)
    #         for key in bm:
    #             bm[key] = str(bm[key])
    #         test_bookmarks.append(test_bm)
    #     log.info(f"test_bookmark: {test_bookmarks}")
    #     response = client.get(
    #         url_for('bookmarksresource')
    #     )
    #     log.info(f"resp: {json.loads(response.get_data())}")
    #     assert json.loads(response.get_data()) == test_bookmarks
