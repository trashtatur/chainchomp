from configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from configlayer.resolver.JinjaResolver import JinjaResolver


class YMLConfigBuilder:
    """
    This class loads a previously merged config map and builds the rest of the configuration
    """

    def __init__(self, mq_type: str, helper: str):
        self.mqtype = mq_type
        self.__jinja_resolver = JinjaResolver(helper)

    def parse_and_build_config(self, config: ChainlinkConfigModel) -> ChainlinkConfigModel:
        config.raw_config = self.__recursive_build_config_data(config.raw_config)
        return config

    def __recursive_build_config_data(self, config_data) -> dict:
        built_dict = {}
        for key, value in config_data.items():
            if isinstance(value, dict):
                built_dict[key] = self.__recursive_build_config_data(value)
            elif isinstance(value, str) and "{{" in value and "}}" in value:
                built_dict[key] = self.__resolve_variable(value)
            else:
                built_dict[key] = value
        return built_dict

    def __resolve_variable(self, var: str) -> str:
        return self.__jinja_resolver.parse_config_template_strings(var)



