from collections import OrderedDict

import mock

from gradient import utils

output_response = ""


class TestPrintDictRecursive(object):
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

        utils.print_dict_recursive(OrderedDict(input_dict), logger_)

        assert output_response == expected_string
