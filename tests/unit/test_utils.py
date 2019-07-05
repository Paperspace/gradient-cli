import mock
import pytest

from gradient import exceptions
from gradient.utils import PathParser


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

        with pytest.raises(exceptions.WrongPathError):
            PathParser.parse_path(path_str)
