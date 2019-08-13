from verify.schemas.ChainlinkSchema import ChainlinkSchema


class SchemaVerifier:

    __CHAINLINK_SCHEMA = ChainlinkSchema()

    @classmethod
    def verifiy(cls, data: dict) -> bool:
        return SchemaVerifier.__CHAINLINK_SCHEMA.schema.validate(data)
