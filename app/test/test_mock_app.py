"""
Testing the mock app 
pytest /tagger_api/app/test/test_mock_app.py -v -s --env=dev
"""

import json
import uuid

from flask import url_for

def test_endpoint(client):
    """ Test the healthcheck endpoint """
    response = client.get(url_for('testresource'))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'msg' in data_obj
    assert data_obj['msg'] == "This is the test endpoint"

def parse_response_str(r):
    """ Parse the response string """
    data = r.get_data()
    s = data.decode()
    s_split = s.split('"')
    r = ''
    if len(s_split) > 1:
        r = s_split[1]
    return r

def valid_uuid(s):
    """ Check if the string is a valid uuid """
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False

def test_get_bookmark(client, mock_get_sqlalchemy, bookmark_obj, not_found_exc):
    """ Test the get bookmark endpoint """

    # successful get
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = bookmark_obj

    # test with mock
    response = client.get(url_for(
        'bookmarkresource',
        bookmark_id=bookmark_obj.id
    ))
    assert response.status_code == 200

    # failed get
    # prep mock
    mock_get_sqlalchemy.get_or_404.side_effect = not_found_exc

    # test with mock
    response = client.get(url_for(
        'bookmarkresource',
        bookmark_id=bookmark_obj.id
    ))
    assert response.status_code == 404
    data = response.get_data()
    data_obj = json.loads(data)
    assert 'message' in data_obj
    expected_msg = "The requested URL was not found on the server. If you entered the URL " \
                 + "manually please check your spelling and try again."
    assert data_obj['message'] == expected_msg

def test_delete_bookmark(client, mock_get_sqlalchemy, mock_session_delete_sqlalchemy,
                         mock_session_commit_sqlalchemy, bookmark_obj, not_found_exc):
    """ Test the delete bookmark endpoint """

    # success delete
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = bookmark_obj
    mock_session_delete_sqlalchemy.return_value = None
    mock_session_commit_sqlalchemy.return_value = None

    # test with mock
    response = client.delete(url_for(
        'bookmarkresource',
        bookmark_id=bookmark_obj.id
    ))
    assert response.status_code == 204

    # failed get bookmark
    # prep mock
    mock_get_sqlalchemy.get_or_404.side_effect = not_found_exc

    # test with mock
    response = client.delete(url_for(
        'bookmarkresource',
        bookmark_id=bookmark_obj.id
    ))
    assert response.status_code == 404
    data = response.get_data()
    data_obj = json.loads(data)
    assert 'message' in data_obj
    expected_msg = "The requested URL was not found on the server. If you entered the URL " \
                 + "manually please check your spelling and try again."
    assert data_obj['message'] == expected_msg

def test_get_bookmarks(client, mock_get_sqlalchemy, bookmarks_obj,bookmarks_filter_obj):
    """ Test the get bookmarks endpoint """

    # get all
    # prep mock
    mock_get_sqlalchemy.all.return_value = bookmarks_obj

    # test with mock
    response = client.get(url_for('bookmarksresource'))
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 2

    # get with filter, match
    # prep mock
    mock_get_sqlalchemy.all.return_value = None
    mock_get_sqlalchemy.filter_by.return_value = bookmarks_filter_obj

    url = "https://www.foo.com"
    response = client.get(url_for('bookmarksresource') + "?url=" + url)
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 1

    # get with filter, no match
    # prep mock
    mock_get_sqlalchemy.filter_by.return_value = []

    url = "https://www.foo.com"
    response = client.get(url_for('bookmarksresource') + "?url=" + url)
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 0

    # successful get with invalid filter
    # prep mock
    mock_get_sqlalchemy.filter_by.return_value = None
    mock_get_sqlalchemy.all.return_value = bookmarks_obj

    # test with mock
    response = client.get(url_for('bookmarksresource') + "?foo=" + url)
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 2

def test_post_bookmark(client, mock_session_add_sqlalchemy, mock_session_commit_sqlalchemy,
                       integrity_error_exc):
    """ Test the post bookmark endpoint """

    # successful post
    # prep mock
    mock_session_add_sqlalchemy.return_value = None
    mock_session_commit_sqlalchemy.return_value = None

    # test with mock
    payload = { "url": "https://www.foo.com" }
    response = client.post(
        url_for('bookmarksresource'),
        json=payload
    )
    assert response.status_code == 200
    data = parse_response_str(response)
    assert valid_uuid(data)

    # failed post: duplicate url
    mock_session_commit_sqlalchemy.side_effect = integrity_error_exc

    # test with mock
    response = client.post(
        url_for('bookmarksresource'),
        json=payload
    )
    assert response.status_code == 400
    data = parse_response_str(response)
    assert data == f"Bad Request: IntegrityError: Bookmark {payload['url']} may already exist."

    # failed post: url attribute value is not string
    mock_session_commit_sqlalchemy.side_effect = None
    response = client.post(
        url_for('bookmarksresource'),
        json={ "url": 0 }
    )
    assert response.status_code == 422
    data = response.get_data()
    assert json.loads(data)
    data_obj = json.loads(data)
    assert 'errors' in data_obj
    assert 'url' in data_obj['errors']
    assert len(data_obj['errors']['url']) == 1
    assert data_obj['errors']['url'][0] == "Not a valid string."

    # failed post: incorrect attribute
    mock_session_commit_sqlalchemy.side_effect = None
    unknown_field = "foo"
    response = client.post(
        url_for('bookmarksresource'),
        json={ unknown_field: "https://www.bar.com" }
    )
    assert response.status_code == 422
    data = response.get_data()
    assert json.loads(data)
    data_obj = json.loads(data)
    assert 'errors' in data_obj
    assert 'url' in data_obj['errors']
    assert len(data_obj['errors']['url']) == 1
    assert data_obj['errors']['url'][0] == "Missing data for required field."
    assert unknown_field in data_obj['errors']
    assert len(data_obj['errors'][unknown_field]) == 1
    assert data_obj['errors'][unknown_field][0] == "Unknown field."
