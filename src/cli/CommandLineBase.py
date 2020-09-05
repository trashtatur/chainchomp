import click

from cli.reader.CommandModuleLocationReader import read_registered_modules, read_module_locations, \
    read_paths_config_of_modules
from cli.resolver.CommandModuleLocationResolver import CommandModuleLocationResolver

commandModuleResolver = CommandModuleLocationResolver()


@click.group()
def chainchomp():
    pass


def search_for_sub_commands():
    modules = read_registered_modules()
    module_locations = read_module_locations(modules)
    sub_command_locations = read_paths_config_of_modules(module_locations)
    for command_location in sub_command_locations:
        commandModuleResolver.import_click_module(command_location.get('commands'), chainchomp)


def main():
    search_for_sub_commands()
    chainchomp()


if __name__ == '__main__':
    main()
