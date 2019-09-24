import os
import shutil
import tempfile
import zipfile

from gradient import api_sdk


def create_file(dir_path, filename):
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "w") as h:
        h.write("keton")


def create_test_dir_tree(dir_path=None):
    if dir_path is None:
        dir_path = tempfile.mkdtemp()

    create_file(dir_path, "file1")
    create_file(dir_path, "file2")
    create_file(dir_path, ".git")

    subdir_path = os.path.join(dir_path, "subdir1")
    os.mkdir(subdir_path)
    create_file(subdir_path, "file2")
    create_file(subdir_path, "file3")

    subdir2_path = os.path.join(dir_path, "subdir2")
    os.mkdir(subdir2_path)
    create_file(subdir2_path, "file4")
    create_file(subdir2_path, "file5")

    return dir_path


class TestZipArchiver(object):
    def test_should_get_valid_excluded_paths_when_empty_list_was_passed_to_get_excluded_paths(self):
        archiver = api_sdk.ZipArchiver()

        excluded = archiver.get_excluded_paths()

        assert excluded == {".git", ".idea", ".pytest_cache"}

    def test_should_get_valid_excluded_paths_when_list_of_files_was_passed_to_get_excluded_paths(self):
        archiver = api_sdk.ZipArchiver()

        excluded = archiver.get_excluded_paths(["some_file", "some_dir/some_other_file"])

        assert excluded == {".git", ".idea", ".pytest_cache", "some_file", "some_dir/some_other_file"}

    def test_should_get_a_dictionary_of_file_paths_in_a_dir(self):
        test_dir = create_test_dir_tree()
        expected_paths = {
            "file1": os.path.join(test_dir, "file1"),
            ".git": os.path.join(test_dir, ".git"),
            "subdir1/file2": os.path.join(test_dir, "subdir1/file2"),
            "subdir1/file3": os.path.join(test_dir, "subdir1/file3"),
            "subdir2/file5": os.path.join(test_dir, "subdir2/file5"),
        }

        paths = api_sdk.ZipArchiver.get_file_paths(test_dir, excluded_paths=["file2", "subdir2/file4"])

        assert paths == expected_paths

    def test_should_get_a_dictionary_of_file_paths_in_a_dir_when_list_of_excluded_files_was_passed(self):
        test_dir = create_test_dir_tree()
        expected_paths = {
            "file1": os.path.join(test_dir, "file1"),
            ".git": os.path.join(test_dir, ".git"),
            "subdir1/file2": os.path.join(test_dir, "subdir1/file2"),
        }

        try:
            paths = api_sdk.ZipArchiver.get_file_paths(test_dir, excluded_paths=["file2", "subdir1/file3", "subdir2"])

            assert paths == expected_paths
        finally:
            shutil.rmtree(test_dir)

    def test_should_add_files_to_archive_when_zip_archiver_was_used(self):
        temp_dir = tempfile.mkdtemp()
        temp_input_dir = os.path.join(temp_dir, "temp_dir")
        os.mkdir(temp_input_dir)
        create_test_dir_tree(temp_input_dir)

        archive_file_path = os.path.join(temp_dir, "archive.zip")
        create_file(temp_dir, "archive.zip")

        temp_dir_for_extracted_files = os.path.join(temp_dir, "output_dir")
        os.mkdir(temp_dir_for_extracted_files)

        expected_paths = {
            "file1": os.path.join(temp_input_dir, "file1"),
            # .git is not here because it's in DEFAULT_EXCLUDED_PATHS
            "subdir1/file2": os.path.join(temp_input_dir, "subdir1/file2"),
        }

        try:
            archiver = api_sdk.ZipArchiver()
            archiver.archive(temp_input_dir, archive_file_path, exclude=["file2", "subdir1/file3", "subdir2"])

            zip_file = zipfile.ZipFile(archive_file_path)
            zip_file.extractall(temp_dir_for_extracted_files)
            archiver2 = api_sdk.ZipArchiver()
            archiver2.default_excluded_paths = []
            paths_in_extracted_dir = archiver2.get_file_paths(temp_dir_for_extracted_files)

        finally:
            shutil.rmtree(temp_dir)

        assert paths_in_extracted_dir.keys() == expected_paths.keys()
