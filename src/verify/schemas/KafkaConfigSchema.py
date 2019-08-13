from schema import Optional, Schema

from verify.schemas.ConfigSchema import ConfigSchema


class KafkaConfigSchema(ConfigSchema, object):



    def __init__(self):
        super().__init__()

    def init_schema(self) -> Schema:
        #TODO Needs actual schema
        return Schema({
            'hostname': str,
            'erlangcookie': str,
            Optional('profile'): {
                'stock': bool,
                'type': str
            }
        })

    @classmethod
    def get_schema_dict(cls):
        #TODO Needs actual schema
        return {
            'hostname': str,
            'erlangcookie': str,
            Optional('profile'): {
                'stock': bool,
                'type': str
            }
        }
