# Initial configuration with default values
_config = {
    'api_key': None,
    'db_string': None,
    'ui_endpoint': '/glassboxx',
    'db_connection': None
}

def get_config(item=None):
    """Function to access the global configuration."""
    if item is not None and item in _config:
        return _config[item]
    return _config
