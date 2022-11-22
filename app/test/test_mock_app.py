# pytest /tagger_api/app/test/test_mock_app.py -v -s --env=dev

from flask import url_for
import json
import uuid

def test_endpoint(client):
    response = client.get(url_for('testresource'))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'msg' in data_obj
    assert data_obj['msg'] == "This is the test endpoint"

def parse_response_str(r):
    data = r.get_data()
    s = data.decode()
    print(f"data: {data}; data.decode: {s}")
    s_split = s.split('"')
    r = ''
    if len(s_split) > 1:
        r = s_split[1]
    return ''

def valid_uuid(s):
    try:
        uuid.UUID(s)
        return True
    except:
        return False

def test_get_bookmark(
        client,
        mock_get_sqlalchemy,
        mock_bookmark_object,
        mock_bookmark_not_found_exc
):
    # successful get
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = mock_bookmark_object

    # test with mock
    response = client.get(url_for(
        'bookmarkresource',
        bookmark_id=mock_bookmark_object.id
    ))
    assert response.status_code == 200

    # failed get
    # prep mock
    mock_get_sqlalchemy.get_or_404.side_effect = mock_bookmark_not_found_exc

    # test with mock
    response = client.get(url_for(
        'bookmarkresource',
        bookmark_id=mock_bookmark_object.id
    ))
    assert response.status_code == 404
    data = response.get_data()
    data_obj = json.loads(data)
    assert 'message' in data_obj
    assert data_obj['message'] == "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."

def test_delete_bookmark(
        client,
        mock_get_sqlalchemy,
        mock_session_delete_sqlalchemy,
        mock_session_commit_sqlalchemy,
        mock_bookmark_object,
        mock_bookmark_not_found_exc
):
    # success delete
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = mock_bookmark_object
    mock_session_delete_sqlalchemy.return_value = None
    mock_session_commit_sqlalchemy.return_value = None

    # test with mock
    response = client.delete(url_for(
        'bookmarkresource',
        bookmark_id=mock_bookmark_object.id
    ))
    assert response.status_code == 204

    # failed get bookmark
    # prep mock
    mock_get_sqlalchemy.get_or_404.side_effect = mock_bookmark_not_found_exc
    
    # test with mock
    response = client.delete(url_for(
        'bookmarkresource',
        bookmark_id=mock_bookmark_object.id
    ))
    assert response.status_code == 404
    data = response.get_data()
    data_obj = json.loads(data)
    assert 'message' in data_obj
    assert data_obj['message'] == "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."

def test_get_bookmarks(
        client,
        mock_get_sqlalchemy,
        mock_bookmarks_object,
        mock_bookmarks_filter_object
):
    # successful get all
    # prep mock
    mock_get_sqlalchemy.all.return_value = mock_bookmarks_object

    # test with mock
    response = client.get(url_for('bookmarksresource'))
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 2

    # successful get with filter
    # prep mock
    mock_get_sqlalchemy.all.return_value = None
    mock_get_sqlalchemy.filter_by.return_value = mock_bookmarks_filter_object

    url = "https://www.foo.com"
    response = client.get(url_for('bookmarksresource') + "?url=" + url)
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 1
    
    # successful get invalid filter filter
    # prep mock

"""
def test_post_bookmark(
    mock_session_commit_integrity_error_sqlalchemy
):
    # successful post
    # prep mock

    # failed post: duplicate url
    mock_session_commit_integrity_error_sqlalchemy.side_effect = mock_integrity_error

    # test with mock
    response = client.delete(url_for(
        'bookmarksresource',
        bookmark_id=mock_bookmark_object.id
    ))
    assert response.status_code == 400
    assert data == f"Bad Request: IntegrityError: Bookmark {mock_bookmark_obj.url} may already exist."
"""
