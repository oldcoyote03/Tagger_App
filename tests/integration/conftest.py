"""
pytest /app/tests/integration/test_bookmarks_api.py --env=local

"""

import pytest
from flask import url_for


def clear_records_with_filters(view, filters, client, get_data, log):
    """ Clear the record """
    log.info(f"Clearing {view} with filters: {filters}")
    response = client.get(url_for(f"{view}-group", **filters))
    if not response.status_code == 200:
        log.info(f"Error getting {view} with filters: {filters}")
        log.info(f"Response status_code={response.status_code}")
        log.info(f"Response data={get_data(response)}")
        return False
    records = get_data(response)
    if not records:
        log.info(f"No records found with filters {filters}")
        return
    for record in records:
        response = client.delete(url_for(f"{view}-item", item_id=record.get("id")))
        if not response.status_code == 204:
            log.info(f"Error deleting record {record}")

@pytest.fixture
def bookmarks_urls():
    """ Test bookmarks urls """
    return [
        {"url": "https://www.stackoverflow.com"},
        {"url": "https://www.hackernews.com"}
    ]

@pytest.fixture
def setup_test_bookmarks(client, get_data, bookmarks_urls, log):  # pylint: disable=redefined-outer-name
    """ Setup data for bookmarks tests """
    view = "bookmarks"
    for url in bookmarks_urls:
        clear_records_with_filters(view, url, client, get_data, log)
