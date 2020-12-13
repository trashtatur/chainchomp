import importlib.machinery
import os

from chainchomplib.abstracts.AbstractResolver import AbstractResolver
from jinja2 import Template

from chainchomp.src import errors


class JinjaResolver(AbstractResolver):

    def __init__(self, helper_path: str):

        self.helper_path = helper_path
        self.helper = self.find_and_resolve_helper()

    def __init_funs(self, template: Template):
        """
        Processes all functions in the given helper object and maps helper functions to the template.
        Inspired by: https://stackoverflow.com/questions/1911281/how-do-i-get-list-of-methods-in-a-python-class
        """
        for fun in dir(self.helper):
            if callable(getattr(self.helper, fun)) and not fun.startswith("__"):
                template.globals[fun] = getattr(self.helper, fun)
        return template

    def find_and_resolve_helper(self, helper_path):
        """
        Finds the indicated helper file if it was correctly denoted and imports it
        so that the functions can be used to resolve values in the YAML config file.

        :raises: errors.VoidHelperSuppliedError
        :raises: errors.InvalidHelperModuleError
        :return: The created helper object
        """
        if helper_path is not None:
            try:
                if os.path.isfile(helper_path):
                    module_name = os.path.basename(helper_path).split(".")[0]
                    imported = importlib.machinery.SourceFileLoader(module_name, self.helper_path).load_module()
                    helper_class = getattr(imported, module_name)
                    return helper_class()
                else:
                    raise errors.VoidHelperSuppliedError(self.helper_path, "The supplied helper class could not be found. Might not be a file")
            except FileNotFoundError:
                raise errors.VoidHelperSuppliedError(self.helper_path, "The supplied helper class was not found")
            except AttributeError:
                raise errors.InvalidHelperModuleError("Your helper class name must be the same as the file name")

    def parse_config_template_strings(self, jinjastring: str) -> str:
        template = self.__init_funs(Template(jinjastring))
        return template.render()
