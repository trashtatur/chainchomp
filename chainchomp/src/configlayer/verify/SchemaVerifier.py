from typing import List

from schema import Schema

from configlayer.verify import SchemaBuilder
from configlayer.verify.schemas.ChainFileSchema import ChainFileSchema


class SchemaVerifier:

    __CHAIN_FILE_SCHEMA = ChainFileSchema()

    def create_full_schema(self, schema_dicts: List[dict]) -> dict:
        output = {}
        for single_dict in schema_dicts:
            output.update(single_dict)
        return output

    @classmethod
    def verify(cls, data: dict, schema: Schema) -> bool:
        built_schema = SchemaBuilder.build_schema_from_dict(data)
        return schema.validate(built_schema)
