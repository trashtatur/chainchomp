from schema import Schema, Optional
from chainchomplib.configlayer.verify.schema.AbstractConfigSchema import AbstractConfigSchema


class ChainFileSchema(AbstractConfigSchema):

    def __init__(self):
        super().__init__()

    def init_schema(self) -> Schema:
        return Schema(ChainFileSchema.get_schema_dict())

    @classmethod
    def get_schema_dict(cls):
        return {
            'project': str,
            'chainlink': ChainFileSchema.get_schema_dict(),
            Optional('start'): str,
            Optional('stop'): str,
            Optional('masterLink'): str,
            Optional('profile'): str
        }
