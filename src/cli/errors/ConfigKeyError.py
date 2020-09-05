class ConfigKeyError(Exception):
    """
    Raised when a key does not exist in a config file
    even though at that point it was expected to exist
    """
    pass
