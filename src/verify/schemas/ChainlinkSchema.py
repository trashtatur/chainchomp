from schema import Schema, Optional, Or

from verify.schemas.ConfigSchema import ConfigSchema
from verify.schemas.KafkaConfigSchema import KafkaConfigSchema
from verify.schemas.RabbitMQConfigSchema import RabbitMQConfigSchema


class ChainlinkSchema(ConfigSchema):

    def __init__(self):
        super().__init__()

    def init_schema(self) -> Schema:
        return Schema(ChainlinkSchema.get_schema_dict())

    @classmethod
    def get_schema_dict(cls) -> dict:
        return {
            'chainlink': {
                'chainlinkname': str,
                'next link': str,
                'remoteconf': bool,
                'type': str,
                Or("rabbitmq", "kafka"): Or(RabbitMQConfigSchema.get_schema_dict(),
                                            KafkaConfigSchema.get_schema_dict())
            }
        }


