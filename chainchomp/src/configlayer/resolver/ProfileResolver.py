import os

import yaml

import definitions


class ProfileResolver:

    def __init__(self, data: dict):
        self.data = data

    def __check_for_provided_profile(self) -> bool:
        if 'profile' in self.data:
            return True
        return False

    def resolve_profile(self, mq_type: str) -> dict:
        """
        Tries to extract profile information from a referenced profile file
        and returns it as a dict object

        :return: The resolved profile information from the referenced file
        """
        profile = self.data['type']
        path = os.path.join(definitions.PROFILES_FOLDER, mq_type) + "/{0}.yml".format(profile)
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
