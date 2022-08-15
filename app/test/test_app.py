
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

def test_post_bookmarks(client):
    payload = { "url": "https://www.imdb.com" }
    response = client.post('/bookmarks', json=payload)
    assert response.status_code == 200

    data = response.get_data()
    assert data == "post"

def test_get_bookmarks(client):
    response = client.get('/bookmarks')
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert len(data_obj) == 0
