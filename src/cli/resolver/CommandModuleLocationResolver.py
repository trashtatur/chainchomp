import importlib.machinery
import os

import click

from configlayer.resolver.AbstractResolver import AbstractResolver


class CommandModuleLocationResolver(AbstractResolver):

    def import_click_module(self, mod, main_command):
        imported = importlib.import_module(mod)
        # filter out any things that aren't a click Command
        for attr in dir(imported):
            foo = getattr(imported, attr)
            if callable(foo) and type(foo) is click.core.Command:
                main_command.add_command(foo)
