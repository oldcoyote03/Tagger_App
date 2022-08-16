
from app import api
from flask import url_for
import json

def test_endpoint(client):
    #response = client.get('/test')
    response = client.get(url_for('api.TestResource'))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'msg' in data_obj
    assert data_obj['msg'] == "This is the test endpoint"

def test_post_bookmarks(client):
    global URL
    URL = "https://www.imdb.com"
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
    
def test_get_bookmark(client):
    global BOOKMARK
    response = client.get('/bookmarks/{}'.format(BOOKMARK['id']))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'id' in data_obj
    assert 'created_at' in data_obj
    assert 'url' in data_obj
    global URL
    assert URL == data_obj['url']

