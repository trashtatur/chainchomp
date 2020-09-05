import importlib
import os
from typing import List
import yaml
import definitions
from cli.errors.ConfigKeyError import ConfigKeyError


def read_paths_config_of_modules(paths: List[str]) -> List[dict]:
    list_of_sub_command_definition_locations = []
    for module_path in paths:
        full_path = module_path+'/config/paths.yml'
        if not os.path.exists(full_path):
            continue
        with open(full_path) as submodule_paths_config:
            try:
                sub_commands = yaml.safe_load(submodule_paths_config)
                if sub_commands is None:
                    continue
                list_of_sub_command_definition_locations.append(sub_commands)
            except yaml.YAMLError as exc:
                # TODO proper Exception
                print(exc)

    return list_of_sub_command_definition_locations


def read_module_locations(registered_modules: dict) -> List[str]:
    modules_list = registered_modules.get('registered_chainchomp_modules')
    if modules_list is None:
        raise ConfigKeyError
    module_paths = [importlib.import_module(name).__path__[0] for name in modules_list]
    return module_paths


def read_registered_modules() -> dict:
    paths_location = definitions.ROOT_DIR + '/config/paths.yml'
    if not os.path.exists(paths_location):
        return {}
    with open(paths_location) as paths:
        try:
            provided_data = yaml.safe_load(paths)
            return provided_data
        except yaml.YAMLError as exc:
            print(exc)


