
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

def valid_uuid(s):
    try:
        uuid.UUID(s)
        return True
    except:
        return False

def parse_response_str(r):
    data = r.get_data()
    s = data.decode()
    return s.split('"')[1]

def test_post_bookmarks(client):
    global URL
    URL = "https://www.imdb.com"
    payload = { "url": URL }
    response = client.post(
        url_for('bookmarksresource'), 
        json=payload
    )
    assert response.status_code == 200
    data = parse_response_str(response)
    assert valid_uuid(data)

def test_post_bookmarks_duplicate(client):
    global URL
    payload = { "url": URL }
    response = client.post(
        url_for('bookmarksresource'),
        json=payload
    )
    assert response.status_code == 400
    data = parse_response_str(response)
    assert 'IntegrityError' in data

def test_get_bookmarks(client):
    response = client.get(url_for('bookmarksresource'))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 1
    global BOOKMARK
    BOOKMARK = data_obj[0]
    assert 'id' in BOOKMARK

def test_get_bookmarks_url_filter(client):
    # add another bookmark with different url
    payload = { "url": "https://www.billboard.com" }
    response = client.post(
        url_for('bookmarksresource'), 
        json=payload
    )
    assert response.status_code == 200

    # confirm there are 2 bookmarks
    response = client.get(url_for('bookmarksresource'))
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 2

    # filter for 1 bookmark
    global URL
    response = client.get(url_for('bookmarksresource') + "?url=" + URL)
    assert response.status_code == 200
    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 1
    global BOOKMARK
    assert data_obj[0]['id'] == BOOKMARK['id']

def test_get_bookmark(client):
    global BOOKMARK
    response = client.get(url_for(
        'bookmarkresource', 
        bookmark_id=BOOKMARK['id']
    ))    
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'id' in data_obj
    assert 'created_at' in data_obj
    assert 'url' in data_obj
    global URL
    assert URL == data_obj['url']

# cleanup DB with the last test
def cleanup(client):
    response = client.get(url_for('bookmarksresource'))
    data = response.get_data()
    data_obj = json.loads(data)
    for bm in data_obj:
        response = client.delete(url_for(
            'bookmarkresource',
            bookmark_id=bm['id']
        ))

def test_delete_bookmark(client):
    global BOOKMARK
    response = client.delete(url_for(
        'bookmarkresource',
        bookmark_id=BOOKMARK['id']
    ))
    assert response.status_code == 204
    
    response = client.get(url_for(
        'bookmarkresource', 
        bookmark_id=BOOKMARK['id']
    ))    
    assert response.status_code == 404

    # cleanup for entire suite
    cleanup(client)
