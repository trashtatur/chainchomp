import os
import click
from cli.resolver.CommandModuleLocationResolver import CommandModuleLocationResolver
import definitions
import chainchomplib

commandModuleResolver = CommandModuleLocationResolver()


@click.group()
def chainchomp():
    pass


def search_for_sub_commands(directory=definitions.ROOT_DIR):
    for element in os.scandir(directory):
        if element.is_file():
            commandModuleResolver.import_click_module(element, chainchomp)
        if element.is_dir():
            search_for_sub_commands(directory)


def main():
    search_for_sub_commands()
    chainchomp()


if __name__ == '__main__':
    main()
