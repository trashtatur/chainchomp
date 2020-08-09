class ChainlinkConfigError(Exception):
    pass


class VoidExternalConfigurationError(ChainlinkConfigError):
    """
    Raised when an external configuration file can't be found / opened

    Attributes:
        path -- the path that the config file was said to be at
        message -- error message
    """

    def __init__(self, path, message):
        self.path = path
        self.message = message


class InvalidExternalConfigurationError(ChainlinkConfigError):
    """
    Raised when an external configuration file is not a valid YAML file

    Attributes:
        path -- the path that the config file was said to be at
        message -- error message
    """

    def __init__(self, path, message, previousError):
        self.path = path
        self.previousError = previousError
        self.message = message


class InvalidMessageQueueTypeError(ChainlinkConfigError):
    """
    Raised when the message queue type in the YAML file is not supported

    Attributes:
        path -- the path that the config file was said to be at
        message -- error message
    """

    def __init__(self, message):
        self.message = message


class VoidHelperSuppliedError(ChainlinkConfigError):
    """
    Raised when the provided helperclass in the config can't be found
    """

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message


class InvalidHelperModuleError(ChainlinkConfigError):
    """
    Raised when the supplied file and its contained class don't have the same name and
    thus the class name can't be inferred from the module
    """

    def __init__(self, message: str):
        self.message = message
