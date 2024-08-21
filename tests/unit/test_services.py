"""
pytest /app/tests/unit/test_services.py

"""

from unittest import mock
import pytest
from app.services import rt_wrapper, SqlaRunner, SqlaNotFound


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
        assert resp == test_resp
        mock_run_transaction_services.assert_called_with(sessionmaker_resp, mock.ANY)
        mock_sessionmaker_services.assert_called_with(mock_db_services.engine)
        log.info(f"mock_callback.call_args: {mock_callback.call_args}")
        mock_callback.assert_called_with(sessionmaker_resp, *args, **kwargs)

    def test_session_get(self, mock_session, mock_model, mock_sqla_attrs):  # pylint: disable=unused-argument
        """ Test the session get method """
        SqlaRunner.model = mock_model
        test_input = "test_input"
        resp = SqlaRunner.session_get(mock_session, test_input)
        assert resp == mock_session.get.return_value
        mock_session.get.assert_called_with(mock_model, test_input)

    def test_get_callback(self, mock_schema, mock_session_get, mock_sqla_attrs):  # pylint: disable=unused-argument
        """ Test the get callback """
        SqlaRunner.schema = mock_schema
        test_session = "test_session"
        test_record_id = "test_record_id"
        resp = SqlaRunner.get_callback(test_session, test_record_id)
        assert resp == mock_schema.dump.return_value
        mock_session_get.assert_called_with(test_session, test_record_id)
        mock_schema.dump.assert_called_with(mock_session_get.return_value)

    def test_get(self, mock_rt_wrapper):
        """ Test the get method """
        test_input = "test_input"
        resp = SqlaRunner.get(test_input)
        assert resp == mock_rt_wrapper.return_value
        mock_rt_wrapper.assert_called_with(SqlaRunner.get_callback, test_input)

    def test_session_delete(self, mock_session):
        """ Test the session get method """
        test_input = "test_input"
        resp = SqlaRunner.session_delete(mock_session, test_input)
        assert resp == mock_session.delete.return_value
        mock_session.delete.assert_called_with(test_input)

    def test_delete_callback_found(self, mock_session_get, mock_session_delete):
        """ Test the get callback """
        test_session = "test_session"
        test_record_id = "test_record_id"
        resp = SqlaRunner.delete_callback(test_session, test_record_id)
        assert resp == mock_session_delete.return_value
        mock_session_get.assert_called_with(test_session, test_record_id)
        mock_session_delete.assert_called_with(test_session, mock_session_get.return_value)

    def test_delete_callback_not_found(
        self, mock_model, mock_session_get, mock_session_delete, mock_sqla_attrs  # pylint: disable=unused-argument
    ):
        """ Test the get callback """
        SqlaRunner.model = mock_model
        mock_session_get.return_value = None
        test_session = "test_session"
        test_record_id = "test_record_id"
        with pytest.raises(SqlaNotFound) as snf:
            SqlaRunner.delete_callback(test_session, test_record_id)
        expected_exc = f"SQL Not Found: model={mock_model.__name__}; record ID: {test_record_id}"
        assert str(snf.value) == expected_exc
        mock_session_get.assert_called_with(test_session, test_record_id)
        mock_session_delete.assert_not_called()

    def test_delete(self, mock_rt_wrapper):
        """ Test the delete method """
        test_input = "test_input"
        resp = SqlaRunner.delete(test_input)
        assert resp == mock_rt_wrapper.return_value
        mock_rt_wrapper.assert_called_with(SqlaRunner.delete_callback, test_input)
