import importlib
import os
from typing import List
import yaml
import definitions


def read_paths_config_of_module(paths: List[str]) -> List[dict]:
    list_of_sub_command_definition_locations = []
    for module_path in paths:
        full_path = module_path+'/config/paths.yml'
        if not os.path.isdir(full_path):
            continue
            # TODO proper Exception
        with open(full_path) as submodule_paths_config:
            try:
                sub_commands = yaml.safe_load(submodule_paths_config)
                list_of_sub_command_definition_locations.append(sub_commands)
            except yaml.YAMLError as exc:
                # TODO proper Exception
                print(exc)

    return list_of_sub_command_definition_locations

def read_module_location(registered_modules: dict) -> list:
    modules_list = registered_modules.get('registered_chainchpomp_modules')
    module_paths = [importlib.import_module(name).__path__[0] for name in modules_list]
    print(module_paths)
    return module_paths


def read_registered_modules() -> dict:
    with open(definitions.ROOT_DIR+'/config/paths.yml') as paths:
        try:
            provided_data = yaml.safe_load(paths)
            return provided_data
        except yaml.YAMLError as exc:
            print(exc)


