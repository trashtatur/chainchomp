import logging
import click

from cli.errors.ConfigKeyError import ConfigKeyError
from cli.errors.MalformedConfigError import MalformedConfigError
from cli.reader.CommandModuleLocationReader import read_registered_modules, read_module_locations, \
    read_paths_config_of_modules
from cli.resolver.CommandModuleLocationResolver import CommandModuleLocationResolver

commandModuleResolver = CommandModuleLocationResolver()


@click.group()
def chainchomp():
    pass


def search_for_sub_commands():
    modules = read_registered_modules()
    try:
        module_locations = read_module_locations(modules)
    except ConfigKeyError:
        raise MalformedConfigError
    sub_command_locations = read_paths_config_of_modules(module_locations)
    for command_location in sub_command_locations:
        commands_path = command_location.get('commands')
        if commands_path is None:
            raise ConfigKeyError('key for commands should have been specified, instead it did not exist')
        commandModuleResolver.import_click_module(commands_path, chainchomp)


def main():
    try:
        search_for_sub_commands()
    except MalformedConfigError:
        logging.warning('Chainchomp was not able to import any subcommands', exc_info=True)
    chainchomp()


if __name__ == '__main__':
    main()
