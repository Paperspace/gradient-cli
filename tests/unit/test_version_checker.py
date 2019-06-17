import mock
import pytest

from gradient import version_checker
from gradient.version import version


@mock.patch("gradient.version_checker.GradientVersionChecker._should_check_version")
@mock.patch("gradient.version_checker.VersionChecker.is_up_to_date")
@mock.patch("gradient.version_checker.logger")
def test_should_check_for_new_gradient_version_and_print_proper_warning_when_current_version_is_old(
        logger_patched, is_up_to_date_patched, should_check_patched):
    should_check_patched.return_value = True
    is_up_to_date_patched.return_value = (False, "1.2.3")

    version_checker.GradientVersionChecker.look_for_new_version()

    is_up_to_date_patched.assert_called_once()
    logger_patched.warning.assert_called_once_with(
        "Warning: this version of the Gradient CLI ({}) is out of date. "
        "Some functionality might not be supported until you upgrade. \n\n"
        "Run `pip install -U gradient` to upgrade\n".format(version))


@mock.patch("gradient.version_checker.GradientVersionChecker._should_check_version")
@mock.patch("gradient.version_checker.VersionChecker.is_up_to_date")
@mock.patch("gradient.version_checker.logger")
def test_should_check_for_new_gradient_version_and_not_print_anything_when_current_version_is_latest(
        logger_patched, is_up_to_date_patched, should_check_patched):
    should_check_patched.return_value = True
    is_up_to_date_patched.return_value = (True, "1.2.3")

    version_checker.GradientVersionChecker.look_for_new_version()

    is_up_to_date_patched.assert_called_once()
    logger_patched.warning.assert_not_called()


@mock.patch("gradient.version_checker.xmlrpclib.ServerProxy")
def test_should_return_package_version_when_get_version_was_run(sever_proxy_class_patched):
    pypi_patched = mock.MagicMock()
    pypi_patched.package_releases.return_value = ["1.2.3"]
    sever_proxy_class_patched.return_value = pypi_patched

    vc = version_checker.VersionChecker()
    latest_version = vc.get_version_from_repository("some_module_name")

    sever_proxy_class_patched.assert_called_with("http://pypi.python.org/pypi")
    assert latest_version == "1.2.3"


@mock.patch("gradient.version_checker.xmlrpclib.ServerProxy")
def test_should_raise_proper_exception_when_get_version_was_run_and_package_was_not_found(sever_proxy_class_patched):
    pypi_patched = mock.MagicMock()
    pypi_patched.package_releases.return_value = []
    sever_proxy_class_patched.return_value = pypi_patched

    vc = version_checker.VersionChecker()
    with pytest.raises(version_checker.PackageNotFoundError):
        vc.get_version_from_repository("some_module_name")

    sever_proxy_class_patched.assert_called_with("http://pypi.python.org/pypi")


@mock.patch("gradient.version_checker.VersionChecker.get_version_from_repository")
def test_should_return_true_when_current_version_equals_latest_from_pypi(get_version_patched):
    get_version_patched.return_value = "1.2.3"

    vc = version_checker.VersionChecker()
    up_to_date, version_in_repository = vc.is_up_to_date("some_module_name", "1.2.3")

    assert up_to_date
    assert version_in_repository == "1.2.3"


@mock.patch("gradient.version_checker.VersionChecker.get_version_from_repository")
def test_should_return_true_when_current_version_is_higher_than_latest_from_pypi(get_version_patched):
    get_version_patched.return_value = "1.2.3"

    vc = version_checker.VersionChecker()
    up_to_date, version_in_repository = vc.is_up_to_date("some_module_name", "1.2.4a0")

    assert up_to_date
    assert version_in_repository == "1.2.3"


@mock.patch("gradient.version_checker.VersionChecker.get_version_from_repository")
def test_should_return_false_when_current_version_is_lower_than_latest_from_pypi(get_version_patched):
    get_version_patched.return_value = "1.2.3"

    vc = version_checker.VersionChecker()
    up_to_date, version_in_repository = vc.is_up_to_date("some_module_name", "1.2.1")

    assert not up_to_date
    assert version_in_repository == "1.2.3"
