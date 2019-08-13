import abc

from schema import Schema


class ConfigSchema(abc.ABC):

    def __init__(self):
        self.schema = self.init_schema()

    @abc.abstractmethod
    def init_schema(self) -> Schema:
        pass

    @abc.abstractclassmethod
    def get_schema_dict(cls):
        pass

