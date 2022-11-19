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
        mock_bookmark_object
):
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = mock_bookmark_object
    
    # test with mock
    response = client.get(url_for(
        'bookmarkresource', 
        bookmark_id=mock_bookmark_object.id
    ))    
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert 'id' in data_obj
    assert 'created_at' in data_obj
    assert 'url' in data_obj
    assert mock_bookmark_object.url == data_obj['url']


from sqlalchemy.exc import IntegrityError

def test_delete_bookmark(
        client,
        mock_get_sqlalchemy,
        mock_session_delete_sqlalchemy,
        mock_session_commit_sqlalchemy,
        mock_session_commit_integrity_error_sqlalchemy,
        mock_bookmark_object,
        mock_integrity_error
):
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
    data = parse_response_str(response)
    assert data == ''

    # prep mock
    mie = lambda: IntegrityError('Mock', ['mock'], IntegrityError)
    mock_session_commit_integrity_error_sqlalchemy.side_effect = mie
    #mock_session_commit_integrity_error_sqlalchemy.side_effect = mock_integrity_error
    
    # test with mock
    response = client.delete(url_for(
        'bookmarkresource', 
        bookmark_id=mock_bookmark_object.id
    ))    
    data = parse_response_str(response)
    assert response.status_code == 400
    #data = parse_response_str(response)
    assert data == 'Bad Request: IntegrityError: Bookmark {} may already exist.'.format(mock_bookmark_object.url)
