from collections import OrderedDict

from paperspace import logger


class CommandBase(object):
    def __init__(self, api=None, logger_=logger):
        self.api = api
        self.logger = logger_

    def _print_dict_recursive(self, input_dict, indent=0, tabulator="  "):
        for key, val in input_dict.items():
            self.logger.log("%s%s:" % (tabulator * indent, key))
            if type(val) is dict:
                self._print_dict_recursive(OrderedDict(val), indent + 1)
            else:
                self.logger.log("%s%s" % (tabulator * (indent + 1), val))
