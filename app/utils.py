""" App Utilities """

import sys
import argparse


def parse_args():
    """ Parse CLI arguments """
    parser = argparse.ArgumentParser(description="Manage the database")
    parser.add_argument("--env", default="local", help="Appplication configuration")
    parser.add_argument("--view", action="store_true", help="View the database tables")
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    parser.add_argument("--remove", action="store_true", help="Reset the database")
    parser.add_argument(
        "--debug",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Appplication logging level"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    args = parser.parse_args()
    not_none_count = sum([args.view, args.reset, args.remove])
    if not_none_count > 1:
        sys.exit(parser.print_usage())
    return args

def strtobool(val):
    """ Convert a string representation of truth to true (1) or false (0) """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1",):
        return True
    elif val in ("n", "no", "f", "false", "off", "0",):
        return False
    else:
        raise ValueError(f"Invalid truth value {val}")

def flatten_dict(parent_value, parent_key="", separator="_"):
    """ Flatten nested dictionary """
    items = []
    for key, value in parent_value.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator=separator).items())
        elif isinstance(value, list):
            items.append((new_key.upper(), ",".join((str(item) for item in value))))
        else:
            items.append((new_key.upper(), str(value)))
    return dict(items)
