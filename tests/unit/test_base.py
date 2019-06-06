from collections import OrderedDict

import mock

from gradient.commands.common import CommandBase

output_response = ""


class TestBaseClass(object):
    def test_json_print(self):
        global output_response
        output_response = ""

        def log_to_var(message):
            global output_response
            output_response = "{}{}\n".format(output_response, message)

        logger_ = mock.MagicMock()
        logger_.log = log_to_var

        input_dict = {
            "foo": {
                'bar': {
                    "baz": "faz"
                }
            }
        }
        expected_string = """foo:
  bar:
    baz:
      faz
"""

        command = CommandBase(logger_=logger_)
        command._print_dict_recursive(OrderedDict(input_dict))

        assert output_response == expected_string
