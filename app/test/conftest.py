from app import create_app

@pytest.fixture
def client():
    app = create_app()
    test_client = app.test_client()
    return test_client
