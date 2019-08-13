import os
import yaml
import definitions
from configs.MQs import MQTypes


class YMLConfigMerger:
    """
    This class merges externally provided configs with the default config
    """

    def __init__(self, mqtype: MQTypes):
        self.mqtype = mqtype

    def load_and_merge(self, path="") -> dict:

        with open(self.__build_default_config_path()) as defaultConfig:
            # TODO this is messy. Make it better!
            try:
                providedConfig = self.__resolve_provided_config(path)
                provided_data = yaml.safe_load(providedConfig)
                default_data = yaml.safe_load(defaultConfig)
            except yaml.YAMLError as exc:
                print(exc)
            if provided_data is not None:
                default_data.update(provided_data)
            if 'profile' in default_data['chainlink'][self.mqtype.value].keys():
                default_data['chainlink'][self.mqtype.value]['profile'] = \
                    self.__resolve_profile(default_data['chainlink'][self.mqtype.value]['profile'])
            return default_data

    def __build_default_config_path(self):
        return os.path.join(definitions.CONFIG_FOLDER, "{0}/default.yml".format(self.mqtype.value))

    def __resolve_provided_config(self, path: str) -> dict or str:
        if path is not "" and os.path.isfile(path):
            return open(path)
        return ""

    def __resolve_profile(self, profiledata: dict) -> dict:
        profile = profiledata['type']
        if profiledata['stock']:
            path = os.path.join(definitions.PROFILES_FOLDER, str(self.mqtype.value)) + "/{0}.yml".format(profile)
        else:
            path = profile
        if os.path.isfile(path):
            try:
                profilemap = yaml.safe_load(open(path))
                return profilemap
            except yaml.YAMLError as error:
                # TODO raise well defined error
                print(error)
        else:
            # TODO raise well defined error
            print("profile path is no file")
            return {}
