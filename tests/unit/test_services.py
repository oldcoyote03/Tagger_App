"""
pytest /app/tests/unit/test_services.py

"""

from unittest import mock
import pytest
from app.services import (
    rt_wrapper, SqlaRunner, SqlaNotFound, get_callback, delete_callback, add_callback,
    get_all_callback,
)

class TestSqlaRunner:
    """ Test the SqlaRunner class """

    @pytest.mark.parametrize(
        "args, kwargs", [((), {}), ((1,), {}), ((), {"one": 1}), ((1,), {"two": 2})]
    )
    def test_run_transaction(
        self, args, kwargs, mock_sessionmaker_services, mock_run_transaction_services,
        mock_db_services, log,
    ):
        """ Test the run_transaction method """
        sessionmaker_resp = "test_session"
        mock_sessionmaker_services.return_value = sessionmaker_resp
        rt_side_effect = lambda session, lambda_callback: lambda_callback(session)  # pylint: disable=unnecessary-lambda-assignment
        mock_run_transaction_services.side_effect = rt_side_effect
        test_resp = "test_response"
        original_callback = lambda s, *args, **kwargs: test_resp  # pylint: disable=unnecessary-lambda-assignment
        mock_callback = mock.MagicMock(side_effect=original_callback)
        resp = rt_wrapper(mock_callback, *args, **kwargs)
        mock_run_transaction_services.assert_called_with(sessionmaker_resp, mock.ANY)
        mock_sessionmaker_services.assert_called_with(mock_db_services.engine)
        log.info(f"mock_callback.call_args: {mock_callback.call_args}")
        mock_callback.assert_called_with(sessionmaker_resp, *args, **kwargs)
        assert resp == test_resp

    def test_get_callback(self, mock_session, mock_model):
        """ Test the get callback """
        test_record_id = "test_record_id"
        resp = get_callback(mock_session, mock_model, test_record_id)
        mock_session.get.assert_called_with(mock_model, test_record_id)
        assert resp == mock_session.get.return_value

    def test_get(self, mock_rt_wrapper, mock_model, mock_schema, mock_sqla_attrs):  # pylint: disable=unused-argument
        """ Test the get method """
        SqlaRunner.model = mock_model
        SqlaRunner.schema = mock_schema
        test_input = "test_input"
        resp = SqlaRunner.get(test_input)
        mock_schema.dump.assert_called_with(mock_rt_wrapper.return_value)
        mock_rt_wrapper.assert_called_with(get_callback, mock_model, test_input)
        assert resp == mock_schema.dump.return_value

    def test_delete_callback_found(self, mock_session, mock_model):
        """ Test the delete callback """
        test_record_id = "test_record_id"
        delete_callback(mock_session, mock_model, test_record_id)
        mock_session.get.assert_called_with(mock_model, test_record_id)
        mock_session.delete.assert_called_with(mock_session.get.return_value)

    def test_delete_callback_not_found(self, mock_session, mock_model):
        """ Test the delete callback - not found """
        mock_session.get.return_value = None
        test_record_id = "test_record_id"
        with pytest.raises(SqlaNotFound) as snf:
            delete_callback(mock_session, mock_model, test_record_id)
        expected_exc = f"SQL Not Found: model={mock_model.__name__}; record ID: {test_record_id}"
        assert str(snf.value) == expected_exc
        mock_session.get.assert_called_with(mock_model, test_record_id)
        mock_session.delete.assert_not_called()

    def test_delete(self, mock_model, mock_rt_wrapper, mock_sqla_attrs):  # pylint: disable=unused-argument
        """ Test the delete method """
        SqlaRunner.model = mock_model
        test_record_id = "test_record_id"
        SqlaRunner.delete(test_record_id)
        mock_rt_wrapper.assert_called_with(delete_callback, mock_model, test_record_id)

    def test_add_callback(self, mock_session):
        """ Test the add callback """
        test_record = "test_record"
        add_callback(mock_session, test_record)
        mock_session.add.assert_called_with(test_record)

    def test_add(self, mock_rt_wrapper):
        """ Test the add method """
        test_record = "test_record"
        SqlaRunner.add(test_record)
        mock_rt_wrapper.assert_called_with(add_callback, test_record)

    @pytest.mark.parametrize(
        "attrs, attr_vals, filters", 
        [
            ((), (), {},),  # no filters
            (("attr1",), ("attr1_val",), {"attr1": "attr1_val"},),  # one filter match
            (("attr1",), ("attr1_val",), {"attr1": "mismatch"},),  # one filter mismatch
            (
                ("attr1", "attr2"), ("attr1_val", "attr2_val"),
                {"attr1": "attr1_val", "attr2": "attr2_val"},
            ),
            (
                ("attr1", "attr2", "attr3"), ("attr1_val", "attr2_val", "attr3_val"), 
                {"attr1": "attr1_val", "attr2": "mismatch", "attr3": "attr3_val"},
            ),
        ],
    )
    def test_get_all_callback(
        self, attrs, attr_vals, filters, mock_session, mock_model, mock_select, log
    ):
        """ Test the get_all callback """
        for i, attr in enumerate(attrs):
            setattr(mock_model, attr, attr_vals[i])
        resp = get_all_callback(mock_session, mock_model, **filters)
        mock_select.assert_called_with(mock_model)
        mock_stmt = mock_select.return_value
        if not filters:
            mock_stmt.where.assert_not_called()
        for attr, filter_attr_val in filters.items():
            mock_attr_val = getattr(mock_model, attr)
            log.info(f"{filter_attr_val} == {mock_attr_val} --> {filter_attr_val == mock_attr_val}")
            mock_stmt.where.assert_called_with(mock_attr_val == filter_attr_val)
            mock_stmt = mock_stmt.where.return_value
        mock_session.scalars.assert_called_with(mock_stmt)
        mock_session.scalars.return_value.all.assert_called_with()
        assert resp == mock_session.scalars.return_value.all.return_value

    @pytest.mark.parametrize(
        "filters", 
        [{}, {"attr1": "attr1_val"}, {"attr1": "attr1_val", "attr2": "attr2_val"},]
    )
    def test_get_all(self, mock_model, mock_schema, filters, mock_rt_wrapper, mock_sqla_attrs):  # pylint: disable=unused-argument
        """ Test the get_all method """
        SqlaRunner.model = mock_model
        SqlaRunner.schema_list = mock_schema
        resp = SqlaRunner.get_all(**filters)
        mock_rt_wrapper.assert_called_with(get_all_callback, mock_model, **filters)
        mock_schema.dump.assert_called_with(mock_rt_wrapper.return_value)
        assert resp == mock_schema.dump.return_value
