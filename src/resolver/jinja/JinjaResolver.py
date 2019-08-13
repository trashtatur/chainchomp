import importlib.machinery
import os

from jinja2 import Template

import errors


class JinjaResolver:

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

    def find_and_resolve_helper(self):
        """
        Finds the helper module and creates an object from it
        :return: Object of the helper class
        """
        if self.helper_path is not None:
            try:
                if os.path.isfile(self.helper_path):
                    modulename = os.path.basename(self.helper_path).split(".")[0]
                    imported = importlib.machinery.SourceFileLoader(modulename, self.helper_path).load_module()
                    helperclass = getattr(imported, modulename)
                    return helperclass()
                else:
                    raise errors.VoidHelperSuppliedError(self.helper_path,
                                                    "The supplied helper class could not be found. Might not be a file")
            except FileNotFoundError:
                raise errors.VoidHelperSuppliedError(self.helper_path, "The supplied helper class was not found")
            except AttributeError:
                raise errors.InvalidHelperModuleError("Your helper class name must be the same as the file name")

    def parse_config_template_strings(self, jinjastring: str) -> str:
        template = self.__init_funs(Template(jinjastring))
        return template.render()
