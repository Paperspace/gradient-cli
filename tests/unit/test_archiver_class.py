import os
import shutil
import tempfile
import zipfile

import mock

import gradient.api_sdk.s3_uploader


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
        archiver = gradient.api_sdk.s3_uploader.ZipArchiver()

        excluded = archiver.get_excluded_paths()

        assert excluded == {".git", ".idea", ".pytest_cache"}

    def test_should_get_valid_excluded_paths_when_list_of_files_was_passed_to_get_excluded_paths(self):
        archiver = gradient.api_sdk.s3_uploader.ZipArchiver()

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

        paths = gradient.api_sdk.s3_uploader.ZipArchiver.get_file_paths(test_dir, excluded_paths=["file2", "subdir2/file4"])

        assert paths == expected_paths

    def test_should_get_a_dictionary_of_file_paths_in_a_dir_when_list_of_excluded_files_was_passed(self):
        test_dir = create_test_dir_tree()
        expected_paths = {
            "file1": os.path.join(test_dir, "file1"),
            ".git": os.path.join(test_dir, ".git"),
            "subdir1/file2": os.path.join(test_dir, "subdir1/file2"),
        }

        try:
            paths = gradient.api_sdk.s3_uploader.ZipArchiver.get_file_paths(test_dir, excluded_paths=["file2", "subdir1/file3", "subdir2"])

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
            archiver = gradient.api_sdk.s3_uploader.ZipArchiver()
            archiver.archive(temp_input_dir, archive_file_path, exclude=["file2", "subdir1/file3", "subdir2"])

            zip_file = zipfile.ZipFile(archive_file_path)
            zip_file.extractall(temp_dir_for_extracted_files)
            archiver2 = gradient.api_sdk.s3_uploader.ZipArchiver()
            archiver2.default_excluded_paths = []
            paths_in_extracted_dir = archiver2.get_file_paths(temp_dir_for_extracted_files)

        finally:
            shutil.rmtree(temp_dir)

        assert paths_in_extracted_dir.keys() == expected_paths.keys()


class TestS3FileUploader(object):
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_upload_file_to_s3_and_get_bucket_url_when_upload_was_executed(self, post_patched):
        _, file_path = tempfile.mkstemp()
        uploader = gradient.api_sdk.s3_uploader.S3FileUploader()

        bucket_url = uploader.upload(file_path, "s3://some.url", "some_bucket_name", {"key": "some_key"})

        post_patched.assert_called_once()
        assert bucket_url == "s3://some_bucket_name/some_key"


class TestS3WorkspaceDirectoryUploader(object):
    WORKSPACE_DIR_PATH = "/some/workspace/dir/path/"
    TEMP_DIR_PATH = "/some/temp/dir/path/"

    @mock.patch("gradient.api_sdk.s3_uploader.S3ProjectFileUploader")
    @mock.patch("gradient.api_sdk.s3_uploader.ZipArchiver")
    def test_class_with_default_params(self, zip_archiver_cls, s3_project_file_uploader_cls):
        zip_archiver = mock.MagicMock()
        zip_archiver_cls.return_value = zip_archiver
        s3_project_file_uploader = mock.MagicMock()
        s3_project_file_uploader.upload.return_value = "s3://url/to/bucket"
        s3_project_file_uploader_cls.return_value = s3_project_file_uploader
        archive_path = os.path.join(tempfile.gettempdir(), "temp.zip")

        uploader = gradient.S3WorkspaceDirectoryUploader("some_api_key")
        bucket_url = uploader.upload(self.WORKSPACE_DIR_PATH, "some_project_id")

        zip_archiver.archive.assert_called_once_with(self.WORKSPACE_DIR_PATH, archive_path, exclude=None)
        s3_project_file_uploader.upload.assert_called_once_with(archive_path, "some_project_id")
        assert bucket_url == "s3://url/to/bucket"

    def test_should_run_upload_(self):
        zip_archiver = mock.MagicMock()
        s3_project_file_uploader = mock.MagicMock()
        s3_project_file_uploader.upload.return_value = "s3://url/to/bucket"
        temp_file_name = "some_temp_file_name.zip"
        archive_path = os.path.join(self.TEMP_DIR_PATH, temp_file_name)

        uploader = gradient.S3WorkspaceDirectoryUploader(
            "some_api_key",
            temp_dir=self.TEMP_DIR_PATH,
            archiver=zip_archiver,
            project_uploader=s3_project_file_uploader,
        )
        bucket_url = uploader.upload(
            self.WORKSPACE_DIR_PATH,
            "some_project_id",
            exclude=["file1", "dir/file2"],
            temp_file_name=temp_file_name,
        )

        zip_archiver.archive.assert_called_once_with(
            self.WORKSPACE_DIR_PATH,
            os.path.join(self.TEMP_DIR_PATH, temp_file_name),
            exclude=["file1", "dir/file2"],
        )
        s3_project_file_uploader.upload.assert_called_once_with(archive_path, "some_project_id")
        assert bucket_url == "s3://url/to/bucket"
