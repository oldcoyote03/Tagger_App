"""
Testing the mock app
pytest /app/test/unit/test_bookmarks_api.py -v -s --env=dev
python manage_db.py
python run.py

docker stop test-flask-api
docker rm test-flask-api
docker build -t test-flask-api .
docker run -d -p 5000:5000 --name test-flask-api \
    -e SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db' \
    test-flask-api
docker exec -it test-flask-api /bin/bash

"""

import json
# import uuid

from flask import url_for

def test_endpoint(client):
    """ Test the healthcheck endpoint """
    response = client.get(url_for('testresource'))
    assert response.status_code == 200

    data = response.get_data()
    data_obj = json.loads(data)
    assert 'msg' in data_obj
    assert data_obj['msg'] == "This is the test endpoint"


# import unittest
# from unittest.mock import patch, MagicMock
# from app.api.bookmarks import get_bookmarks, create_bookmark, delete_bookmark

# class TestBookmarksAPI(unittest.TestCase):
#     """ Test the bookmarks API """

#     @patch('app.api.bookmarks.db')
#     def test_get_bookmarks(self, mock_get_db):
#         """ Test the get bookmarks endpoint """

#         mock_db = MagicMock()
#         mock_get_db.return_value = mock_db
#         mock_db.query.return_value.all.return_value = [
#             {'id': 1, 'url': 'https://example.com', 'title': 'Example'},
#             {'id': 2, 'url': 'https://test.com', 'title': 'Test'}
#         ]
#         bookmarks = get_bookmarks()
#         self.assertEqual(len(bookmarks), 2)
#         self.assertEqual(bookmarks[0]['url'], 'https://example.com')
#         self.assertEqual(bookmarks[1]['url'], 'https://test.com')

#     @patch('app.api.bookmarks.get_db')
#     def test_create_bookmark(self, mock_get_db):
#         mock_db = MagicMock()
#         mock_get_db.return_value = mock_db
#         bookmark = {'url': 'https://newsite.com', 'title': 'New Site'}
#         result = create_bookmark(bookmark)
#         mock_db.add.assert_called_once()
#         mock_db.commit.assert_called_once()
#         self.assertTrue(result)

#     @patch('app.api.bookmarks.get_db')
#     def test_delete_bookmark(self, mock_get_db):
#         mock_db = MagicMock()
#         mock_get_db.return_value = mock_db
#         mock_db.query.return_value.filter.return_value.one.return_value = MagicMock()
#         result = delete_bookmark(1)
#         mock_db.delete.assert_called_once()
#         mock_db.commit.assert_called_once()
#         self.assertTrue(result)

#     @patch('app.api.bookmarks.get_db')
#     def test_delete_bookmark_not_found(self, mock_get_db):
#         mock_db = MagicMock()
#         mock_get_db.return_value = mock_db
#         mock_db.query.return_value.filter.return_value.one.side_effect = Exception('Not found')
#         result = delete_bookmark(1)
#         self.assertFalse(result)
