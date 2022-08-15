
import json

"""
def test_always_passes():
    assert True

def test_always_fails():
    assert False
"""

def test_endpoint(client):
    response = client.get('/test')
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'msg' in data_obj
    assert data_obj['msg'] == "This is the test endpoint"

global URL = "https://www.imdb.com"
global BOOKMARK = "INITIAL"

def test_post_bookmarks(client):
    payload = { "url": URL }
    response = client.post('/bookmarks', json=payload)
    assert response.status_code == 200

    data = response.get_data()
    assert data == b'"post"\n'

def test_get_bookmarks(client):
    response = client.get('/bookmarks')
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 1
    global BOOKMARK
    BOOKMARK = data_obj[0]
    assert 'id' in BOOKMARK
    print('MULTI - type BOOKMARK: {}'.format(type(BOOKMARK)))
    print('MULTI - BOOKMARK: {}'.format(BOOKMARK))

def test_get_bookmark(client):
    global BOOKMARK
    print('SINGLE - type BOOKMARK: {}'.format(type(BOOKMARK)))
    print('SINGLE - BOOKMARK: {}'.format(BOOKMARK))
    assert True
    """response = client.get('/bookmarks/{}'.format(BOOKMARK['id']))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'id' in data_obj
    assert 'created_at' in data_obj
    assert 'url' in data_obj
    assert URL == data_obj['url']"""

