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
    return s.split('"')[1]

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

def test_delete_bookmark(
        client,
        mock_get_sqlalchemy,
        mock_sqlalchemy,
        mock_create_scoped_session_sqlalchemy,
        mock_bookmark_object
):
    # prep mock
    mock_get_sqlalchemy.get_or_404.return_value = mock_bookmark_object
    mock_sqlalchemy.session.delete.return_value = None
    mock_sqlalchemy.session.commit.return_value = None
    #mock_session_sqlalchemy.delete.return_value = None
    #mock_session_sqlalchemy.commit.return_value = None
    mock_create_scoped_session_sqlalchemy.return_value = None

    # test with mock
    response = client.delete(url_for(
        'bookmarkresource', 
        bookmark_id=mock_bookmark_object.id
    ))    
    assert response.status_code == 204
    data = parse_response_str(response)
    assert data == ''
