# pytest /tagger_api/app/test/test_mock_app.py -v -s

from flask import url_for
import json
import uuid

def test_endpoint(flask_app_mock):
    with flask_app_mock..app_context():
        #response = flask_app_mock.get(url_for('testresource'))
        response = get(url_for('testresource'))
        assert response.status_code == 200

        data = response.get_data()
        data_obj = json.loads(data)
        assert 'msg' in data_obj
        assert data_obj['msg'] == "This is the test endpoint"
