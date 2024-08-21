"""
pytest /app/tests/unit/test_schema.py

"""

from unittest.mock import call, MagicMock
import pytest
from app.schema import Bookmarks, view_database_details, manage_db


def test_bookmarks_repr(mock_base_model_schema):  # pylint: disable=unused-argument
    """ Test Bookmarks repr """
    test_bookmarks = Bookmarks(url="test url")
    test_input = "test id"
    test_bookmarks.id = test_input
    assert repr(test_bookmarks) == f'<Bookmarks {test_input}>'

def test_view_database_details(mock_db_schema, mock_create_table_schema):
    """ Test view_database_details """
    view_database_details()
    mock_create_table_schema().compile.assert_called()
    create_table_calls = [
        call(mock_db_schema.metadata.tables.get("table_1_name")),
        call().compile(mock_db_schema.engine),
        call(mock_db_schema.metadata.tables.get("table_2_name")),
        call().compile(mock_db_schema.engine),
    ]
    mock_create_table_schema.assert_has_calls(create_table_calls)

@pytest.mark.parametrize(
    "test_input,expected", 
    [
        (
            {"view": False, "reset": False, "remove": False},
            {"create_all": True, "drop_all": False},
        ),
        (
            {"view": True, "reset": False, "remove": False},
            {"create_all": False, "drop_all": False},
        ),
        (
            {"view": False, "reset": True, "remove": False},
            {"create_all": True, "drop_all": True},
        ),
        (
            {"view": False, "reset": False, "remove": True},
            {"create_all": False, "drop_all": True},
        ),
    ]
)
def test_manage_db(
    test_input, expected, mock_db_schema, mock_app_schema, mock_make_url_schema,
    mock_view_db_details_schema
):
    """ Test Manage DB: Assumes calling method enforces max 1 arg as True """
    mock_app_schema.config["SQLALCHEMY_DATABASE_URI"] = "test_uri"
    args_attr = {
        "view": test_input["view"],
        "reset": test_input["reset"],
        "remove": test_input["remove"],
    }
    args = MagicMock()
    args.configure_mock(**args_attr)
    manage_db(mock_app_schema, args)
    if expected.get("create_all"):
        mock_db_schema.create_all.assert_called()
    else:
        mock_db_schema.create_all.assert_not_called()
    if expected.get("drop_all"):
        mock_db_schema.drop_all.assert_called()
    else:
        mock_db_schema.drop_all.assert_not_called()
    mock_make_url_schema.assert_called_with(mock_app_schema.config["SQLALCHEMY_DATABASE_URI"])
    mock_view_db_details_schema.assert_called()
