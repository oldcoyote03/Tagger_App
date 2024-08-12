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
