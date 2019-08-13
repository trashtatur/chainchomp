from schema import Optional, Schema

from verify.schemas.ConfigSchema import ConfigSchema


class RabbitMQConfigSchema(ConfigSchema, object):

    def __init__(self):
        super().__init__()

    def init_schema(self) -> Schema:
        return Schema({
            'hostname': str,
            'erlangcookie': str,
            Optional('profile'): {
                'stock': bool,
                'type': str
            }
        })

    def validate(self, data):
        return self.schema.validate(data)



