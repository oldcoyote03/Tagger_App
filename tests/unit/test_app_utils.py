"""
pytest /app/tests/unit/test_app_utils.py
"""

import sys
import pytest
from app.utils import strtobool, flatten_dict, parse_args


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Y", True,), ("Yes", True,), ("T", True,),
        ("TRUE", True,), ("ON", True,), ("1", True,),
        ("N", False,), ("No", False,), ("F", False,),
        ("FALSE", False,), ("OFF", False,), ("0", False,),
    ]
)
def test_strtobool_true_false(test_input, expected):
    """ Test the healthcheck endpoint """
    assert strtobool(test_input) is expected

def test_strtobool_exception():
    """ Test the healthcheck endpoint """
    with pytest.raises(Exception) as exc:
        strtobool("exception")
    assert str(exc.value) == "Invalid truth value exception"

@pytest.mark.parametrize(
    "test_parent, expected",
    [
        ({"TESTKEY1": "TESTVAL1"}, {"TESTKEY1": "TESTVAL1"}),
        ({},{}),
        ({"TESTKEY1": ["1", 2, True]}, {"TESTKEY1": "1,2,True"}),
        (
            {
                "TESTKEY1": "TESTVAL1",
                "TESTKEY2": {
                    "TESTKEY3": "TESTVAL3",
                    "TESTKEY4": {
                        "TESTKEY5": "TESTVAL5"
                    }
                },
            },
            {
                "TESTKEY1": "TESTVAL1",
                    "TESTKEY2_TESTKEY3": "TESTVAL3",
                    "TESTKEY2_TESTKEY4_TESTKEY5": "TESTVAL5"
            },
        ),
    ]
)
def test_flatten_dict_works(log, test_parent, expected):
    """ Test the healthcheck endpoint """
    flattened_dict = flatten_dict(test_parent)
    log.info(f"Flattened Dictionary : {flattened_dict}")
    log.info(f"Expected             : {expected}")
    assert flattened_dict == expected

def test_flatten_dict_separator(log):
    """ Test the healthcheck endpoint """
    test_parent = {
        "TESTKEY1": "TESTVAL1",
        "TESTKEY2": {
            "TESTKEY3": "TESTVAL3",
            "TESTKEY4": {
                "TESTKEY5": "TESTVAL5"
            }
        },
    }
    expected = {
        "TESTKEY1": "TESTVAL1",
        "TESTKEY2--TESTKEY3": "TESTVAL3",
        "TESTKEY2--TESTKEY4--TESTKEY5": "TESTVAL5"
    }
    flattened_dict = flatten_dict(test_parent, separator="--")
    log.info(f"Flattened Dictionary : {flattened_dict}")
    log.info(f"Expected             : {expected}")
    assert flattened_dict == expected

def test_parse_args(mock_argparse):
    """ Test CLI args parser """
    sys.argv = [1]
    mock_argparse.return_value.parse_args.return_value = "test args"
    result = parse_args()
    assert result == "test args"

def test_parse_args_exit(mock_argparse):
    """ Test CLI args parser """
    sys.argv = [1,2]
    with pytest.raises(SystemExit):
        parse_args()
    mock_argparse.return_value.print_usage.assert_called_once()
