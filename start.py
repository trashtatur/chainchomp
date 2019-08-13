import os
import yaml

import definitions
from configs import MQs
import errors
from resolver.YMLConfigBuilder import YMLConfigBuilder
from resolver.YMLConfigMerger import YMLConfigMerger
from verify.SchemaVerifier import SchemaVerifier


def read_config(path: str) -> dict:
    # 1 VERIFY YML CONFIG SUPPLIED
    verifier = SchemaVerifier()
    verifier.verifiy(__read_in_external_config(path))
    # 2 MERGE WITH DEFAULT CONFIG
    type = __extract_config_type(yaml.safe_load(open(path)))
    mergedConfig = YMLConfigMerger(type).load_and_merge(path)
    # 3 RESOLVE VARS IN CONFIG AND BUILD IT
    helper_path = __extract_helper(path)
    builder = YMLConfigBuilder(type, helper_path)
    return builder.parse_and_build_config(mergedConfig)


def __read_in_external_config(path: str) -> dict:
    if os.path.isfile(path):
        try:
            conf = yaml.safe_load(open(path))
            return conf
        except yaml.YAMLError as error:
            raise errors.InvalidExternalConfigurationError(path, "This seems to be an invalid YML file", error)
    else:
        raise errors.VoidExternalConfigurationError(path, "The config file could not be found at the given path")


def __extract_config_type(config: dict) -> MQs.MQTypes:
    if 'rabbitmq' in config['chainlink'].keys():
        return MQs.MQTypes.RABBITMQ
    if 'kafka' in config['chainlink'].keys():
        return MQs.MQTypes.KAFKA
    else:
        raise errors.InvalidMessageQueueTypeError(
            "The supplied messagequeuetype is not supported. Must be either 'kafka' or 'rabbitmq'")


def __extract_helper(path: str):
    if os.path.isfile(path):
        line = open(path).readline()
        if line[:1] == "#":
            if "stock:" in line[:8]:
                filename = line.split("stock:", 1)[1].strip().rstrip()
                return os.path.join(definitions.STOCK_HELPER_PATH, filename)
            else:
                return line[1:]
    return None


print(read_config(os.path.join(definitions.CONFIG_FOLDER, "rabbitmq/default.yml")))