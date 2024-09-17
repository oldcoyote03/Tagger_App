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
    mock_argument_parser_instance = mocker.MagicMock()
    mock_argument_parser_instance.add_argument.return_value = None
    mock_argument_parser_instance.parse_args.return_value = "parse_args"
    mock_argument_parser = mocker.patch("app.utils.argparse.ArgumentParser")
    mock_argument_parser.return_value = mock_argument_parser_instance
    return mock_argument_parser
