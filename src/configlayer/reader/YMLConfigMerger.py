import os

import yaml

import definitions
from configlayer.model.ChainlinkRawConfigModel import ChainlinkConfigModel
from configlayer.model import MQTypes
from configlayer.resolver import ProfileResolver


class YMLConfigMerger:
    """
    This class merges externally provided model with the default config
    """

    def __init__(self, mqtype: MQTypes):
        self.mqtype = mqtype
        self.profileResolver = None

    def load_and_merge(self, path="") -> ChainlinkConfigModel:
        """
        Loads a provided chainlink application configuration file and merges it with
        the default configuration, prioritizing the users config

        :param path: The path to the external YAML config
        :return: A merged config packed into a dict
        """

        with open(self.__build_default_config_path()) as defaultConfig:
            # TODO this is messy. Make it better!
            try:
                provided_data = yaml.safe_load(self.__resolve_provided_config(path))
                default_data = yaml.safe_load(defaultConfig)
                if provided_data is not None:
                    default_data.update(provided_data)
                default_data = self.__check_for_and_resolve_profile(default_data)
            except yaml.YAMLError as exc:
                print(exc)

            return ChainlinkConfigModel(default_data)

    def __build_default_config_path(self):
        return os.path.join(definitions.CONFIG_FOLDER, "default.yml")

    def __resolve_provided_config(self, path: str) -> dict or str:
        if path is not "" and os.path.isfile(path):
            return open(path)
        return ""

    def __check_for_and_resolve_profile(self, data):
        try:
            self.profileResolver = ProfileResolver(data['chainlink'][self.mqtype.value]['profile'])
        except KeyError:
            data['chainlink'][self.mqtype.value] = {'profile': {'type': 'default'}}
            self.profileResolver = ProfileResolver(data['chainlink'][self.mqtype.value]['profile'])
        data['chainlink'][self.mqtype.value]['profile'] = self.profileResolver.resolve_profile(
            self.mqtype)
        return data
