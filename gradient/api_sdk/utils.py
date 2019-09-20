from collections import OrderedDict

import six


class MessageExtractor(object):
    def get_message_from_response_data(self, response_data, sep="\n"):
        """
        :type response_data: None|dict|list|str
        :type sep: str
        :rtype: str
        """
        messages = list(self.get_error_messages(response_data))
        msg = sep.join(messages)

        return msg

    def get_error_messages(self, data, add_prefix=False):
        if isinstance(data, dict):
            for key, value in sorted(data.items()):
                if key in ("error", "errors", "message", "messages", "title", "description"):
                    for message in self.get_error_messages(value):
                        yield message

                # when key == "details" and value is a dict then values should be prefixed with key
                if add_prefix:
                    for message in self.get_error_messages(value):
                        # there is some useless message in data["context"]
                        if key != "context":
                            yield key + ": " + message
                if key == "details":
                    for message in self.get_error_messages(value, add_prefix=True):
                        yield message

        if isinstance(data, list):
            for element in data:
                for message in self.get_error_messages(element):
                    yield message

        if isinstance(data, six.string_types):
            yield data


def print_dict_recursive(input_dict, logger, indent=0, tabulator="  "):
    for key, val in input_dict.items():
        logger.log("%s%s:" % (tabulator * indent, key))
        if type(val) is dict:
            print_dict_recursive(OrderedDict(val), logger, indent + 1)
        else:
            logger.log("%s%s" % (tabulator * (indent + 1), val))
