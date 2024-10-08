""" App utilities fixtures """

import pytest

@pytest.fixture
def mock_flatten_dict(mocker):
    """ Mock flatten_dict """
    return mocker.patch("app.utils.flatten_dict")

@pytest.fixture
def mock_dynaconf(mocker):
    """ Mock load_configs_from_file """
    return mocker.patch("app.config.utils.Dynaconf")

@pytest.fixture
def mock_argparse(mocker):
    """ Mock argparse """
    mock_parse_args = mocker.MagicMock()
    mock_parse_args.env = "local"
    mock_parse_args.view = False
    mock_parse_args.reset = False
    mock_parse_args.remove = False
    mock_parse_args.debug = True
    mock_parse_args.host = "0.0.0.0"
    mock_argument_parser_instance = mocker.MagicMock()
    mock_argument_parser_instance.add_argument.return_value = None
    mock_argument_parser_instance.parse_args.return_value = mock_parse_args
    mock_argument_parser = mocker.patch("app.utils.argparse.ArgumentParser")
    mock_argument_parser.return_value = mock_argument_parser_instance
    return mock_argument_parser
