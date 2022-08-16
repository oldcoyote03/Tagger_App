import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app
    #test_client = app.test_client()
    #return test_client
