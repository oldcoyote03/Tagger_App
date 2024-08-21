""" DB Schema Utils """

import pytest


@pytest.fixture
def mock_base_model_schema(mocker):
    """ Mock BaseModel """
    return mocker.patch("app.schema.BaseModel")

@pytest.fixture
def mock_db_schema(mocker):
    """ Mock db """
    mock_db_engine_attrs = {
        "__str__.return_value": "test_engine",
        "driver.__str__.return_value": "test_driver",
        "dialect.name.__str__.return_value": "test_dialect",
    }
    mock_db_engine = mocker.MagicMock()
    mock_db_engine.configure_mock(**mock_db_engine_attrs)

    tables = {}
    for i, table in ((1, mocker.MagicMock(),), (2, mocker.MagicMock(),)):
        table.primary_key.__str__.return_value = f"primary_key_{i}"
        tables[f"table_{i}_name"] = table
    mock_db_metadata = mocker.MagicMock()
    mock_db_metadata.tables = tables

    mock_db_attrs  = {
        "__str__.return_value": "mock_db",
        "engine": mock_db_engine,
        "metadata": mock_db_metadata,
        "create_all.return_value": None,
        "drop_all.return_value": None,
    }
    mock_db = mocker.patch("app.schema.db")
    mock_db.configure_mock(**mock_db_attrs)
    return mock_db

@pytest.fixture
def mock_create_table_schema(mocker):
    """ Mock CreateTable """
    mock_create_table_instance = mocker.MagicMock()
    mock_create_table_instance.compile.return_value = "test_create_table_compile"
    mock_create_table = mocker.patch("app.schema.CreateTable")
    mock_create_table.return_value = mock_create_table_instance
    return mock_create_table

@pytest.fixture
def mock_app_schema(mocker):
    """ Mock app """
    mock_app_attrs = {"app_context.return_value.__enter__.return_value": None, "config": {}}
    mock_app = mocker.MagicMock()
    mock_app.configure_mock(**mock_app_attrs)
    return mock_app

@pytest.fixture
def mock_make_url_schema(mocker):
    """ Mock make_url """
    mock_make_url_instance = mocker.MagicMock()
    mock_make_url_instance.database.__str__.return_value = "test_database_name"
    mock_make_url = mocker.patch("app.schema.make_url")
    mock_make_url.return_value = mock_make_url
    return mock_make_url

@pytest.fixture
def mock_view_db_details_schema(mocker):
    """ Mock view_database_details """
    return mocker.patch("app.schema.view_database_details", return_value=None)
