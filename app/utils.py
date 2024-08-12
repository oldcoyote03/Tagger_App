""" App Utilities """

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
