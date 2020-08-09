import importlib.machinery
import os

import click

from configlayer.resolver.AbstractResolver import AbstractResolver


class CommandModuleLocationResolver(AbstractResolver):

    def import_click_module(self, mod, main_command):
        module_name = os.path.basename(mod.path).split(".")[0]
        module_ending = os.path.basename(mod.path).split(".")[1]
        if '__init__' in module_name and 'py' != module_ending:
            return
        print(module_name)
        imported = importlib.machinery.SourceFileLoader(module_name, mod.path).load_module()
        # filter out any things that aren't a click Command
        for attr in dir(imported):
            foo = getattr(imported, attr)
            if callable(foo) and type(foo) is click.core.Command:
                main_command.add_command(foo)
