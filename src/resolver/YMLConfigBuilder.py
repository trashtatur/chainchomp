from resolver.jinja.JinjaResolver import JinjaResolver
from src.configs.MQs import MQTypes


class YMLConfigBuilder:
    """
    This class loads a previously merged config map and builds the rest of the configuration
    like external sources and profile yml files
    """

    def __init__(self, mqtype: MQTypes, helper: str):
        self.mqtype = mqtype
        self.__jinja_resolver = JinjaResolver(helper)

    def parse_and_build_config(self, raw_config_data: dict) -> dict:
        built_dict = {}
        for key, value in raw_config_data.items():
            if isinstance(value, dict):
                built_dict[key] = self.parse_and_build_config(value)
            elif isinstance(value,str) and value[:2] == "{{":
                built_dict[key] = self.__resolve_variable(value)
            else:
                built_dict[key] = value
        return built_dict

    def __resolve_variable(self, var: str) -> str:
        return self.__jinja_resolver.parse_config_template_strings(var)



