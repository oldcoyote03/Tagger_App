"""
pytest /app/tests/unit/test_config_utils.py

"""

import logging
import os
from unittest.mock import MagicMock

import pytest

from app.config.utils import (
    load_configs, get_config, get_logging_config, DevelopmentConfig, LocalConfig, DockerConfig
)

log = logging.getLogger(__name__)

def test_load_configs(mock_os_path_join, mock_dynaconf):
    """ Test the healthcheck endpoint """
    mock_os_path_join.return_value = "/test/config/path.json"
    mock_dynaconf_instances = [MagicMock(), MagicMock()]
    mock_dynaconf_instances[0].as_dict.return_value = {}
    mock_dynaconf_instances[1].as_dict.return_value = {
        "TESTKEY1": "ENV",
        "TESTKEY2": "ENV",
    }
    mock_dynaconf.side_effect = mock_dynaconf_instances
    os.environ["TESTKEY2"] = "OS"
    load_configs("test_env")
    assert os.environ.get("TESTKEY1") == "ENV"
    assert os.environ.get("TESTKEY2") == "OS"

@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("default", DevelopmentConfig,), ("development", DevelopmentConfig,),
        ("local", LocalConfig,), ("docker", DockerConfig,),
    ]
)
def test_get_config_args(test_input, expected):
    """ Test getting config with args """
    os.environ["APP_ENV"] = test_input
    assert isinstance(get_config(), expected)
    # os env contradicts given arg
    os.environ["APP_ENV"] = "local" if test_input != "local" else test_input
    assert isinstance(get_config(test_input), expected)

def test_get_config_no_args():
    """ Test getting config with args without args """
    assert os.environ.get("APP_ENV") is None
    assert isinstance(get_config(), DevelopmentConfig)

def test_get_config_unexpected():
    """ Test getting config with args without args """
    unexpected_arg = "unexpected"
    expected_msg = "'NoneType' object has no attribute 'NAME'"
    assert os.environ.get("APP_ENV") is None
    with pytest.raises(AttributeError) as exc:
        get_config(unexpected_arg)
    assert str(exc.value) == expected_msg
    os.environ["APP_ENV"] = unexpected_arg
    with pytest.raises(AttributeError) as exc:
        get_config()
    assert str(exc.value) == expected_msg

def test_get_logging_config():
    """ Test getting logging config """
    log_config = get_logging_config()
    assert log_config.get("handlers",{}).get("file") is None
    test_file = "test.log"
    log_config = get_logging_config(test_file)
    assert log_config.get("handlers").get("file").get("filename") == test_file
