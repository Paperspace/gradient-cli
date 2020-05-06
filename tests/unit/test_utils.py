from collections import OrderedDict

import mock
import pytest

import gradient.api_sdk.utils
from gradient import cliutils, exceptions
from gradient.api_sdk.sdk_exceptions import WrongPathError
from gradient.api_sdk.utils import PathParser
from gradient.cli.common import validate_comma_split_option

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

        gradient.api_sdk.utils.print_dict_recursive(OrderedDict(input_dict), logger_)

        assert output_response == expected_string


class TestPathParser(object):
    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.path.isdir", return_value=True)
    def test_should_return_local_dir_type_when_given_directory_exists(self, _, __):
        path_str = "/home/usr/some/path"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.LOCAL_DIR

    @mock.patch("os.path.exists", return_value=True)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=True)
    def test_should_return_local_archive_type_when_archive_exists(self, _, __, ___):
        path_str = "/home/usr/some/path.zip"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.LOCAL_FILE

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=False)
    def test_should_return_git_url_type_when_git_ssh_url_was_given(self, _, __, ___):
        path_str = "git@github.com:Paperspace/gradient-cli.git"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.GIT_URL

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=False)
    def test_should_return_git_url_type_when_git_http_url_was_given(self, _, __, ___):
        path_str = "https://github.com/Paperspace/gradient-cli.git"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.GIT_URL

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=False)
    def test_should_return_git_url_type_when_git_http_url_was_given_with_git_prefix_and_no_extension(self, _, __, ___):
        path_str = "GIT:https://github.com/Paperspace/gradient-cli"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.GIT_URL

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=False)
    def test_should_return_s3_type_when_s3_url_was_given(self, _, __, ___):
        path_str = "S3:some/path"

        path_type = PathParser.parse_path(path_str)

        assert path_type == PathParser.S3_URL

    @mock.patch("os.path.exists", return_value=False)
    @mock.patch("os.path.isdir", return_value=False)
    @mock.patch("os.path.isfile", return_value=False)
    def test_should_raise_exception_when_local_path_was_given_but_does_not_exist(self, _, __, ___):
        path_str = "/home/usr/some/path.zip"

        with pytest.raises(WrongPathError):
            PathParser.parse_path(path_str)


class TestValidateAuthOptions(object):
    def test_should_not_raise_exception_when_only_generate_auth_was_set(self):
        kwargs = {"auth_username": None, "auth_password": None, "generate_auth": True}
        cliutils.validate_auth_options(kwargs)

    def test_should_not_raise_exception_when_username_and_password_was_set(self):
        kwargs = {"auth_username": "username", "auth_password": "password", "generate_auth": False}
        cliutils.validate_auth_options(kwargs)

    def test_should_not_raise_exception_when_username_was_set_but_no_password(self):
        kwargs = {"auth_username": "username", "auth_password": None, "generate_auth": False}
        pytest.raises(exceptions.ApplicationError, cliutils.validate_auth_options, kwargs)

    def test_should_not_raise_exception_when_all_values_were_set(self):
        kwargs = {"auth_username": "username", "auth_password": "password", "generate_auth": True}
        pytest.raises(exceptions.ApplicationError, cliutils.validate_auth_options, kwargs)


class TestCommonFunction(object):
    @pytest.mark.parametrize("comma_value, value, expected_result", [
        pytest.param(None, None, None, id="None passed in both argument"),
        pytest.param(None, ['test'], ['test'], id="None passed as comma separated value"),
        pytest.param("test", None, ['test'], id="None passed as list value"),
        pytest.param("test0", ["test1"], ["test0", "test1"], id="Pass single values for arguments"),
        pytest.param(
            "test0,test1", ["test2"], ["test0", "test1", "test2"],
            id="Pass more values separated by comma and single element in list"
        ),
        pytest.param(
            "test0 ,test1, test2 , test3", ["test4"], ["test0", "test1", "test2", "test3", "test4"],
            id="Pass more values separated by comma in different style and single element in list"
        ),
        pytest.param(
            "test0\t,test1,\ntest2\t,\ttest3\n", ["test4"], ["test0", "test1", "test2", "test3", "test4"],
            id="Pass more values separated by comma with more type of white chars and single element in list"
        ),
    ])
    def test_validate_comma_split_option(self, comma_value, value, expected_result):
        if expected_result:
            expected_result.sort()
        result = validate_comma_split_option(comma_value, value)
        if result:
            result.sort()
        assert result == expected_result
