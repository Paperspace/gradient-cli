import os
import shutil
import tempfile
import zipfile

import mock

import gradient.api_sdk.archivers
import gradient.api_sdk.s3_uploader


def create_file(dir_path, filename):
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "w") as h:
        h.write("keton")


def create_test_dir_tree(dir_path=None):
    if dir_path is None:
        dir_path = tempfile.mkdtemp()

    create_file(dir_path, "file1.txt")
    create_file(dir_path, "file2.jpg")

    dot_git_path = os.path.join(dir_path, ".git")
    os.mkdir(dot_git_path)
    create_file(dot_git_path, "some_file")

    subdir_path = os.path.join(dir_path, "subdir1")
    os.mkdir(subdir_path)
    create_file(subdir_path, "file2.jpg")
    create_file(subdir_path, "file3.txt")

    subdir2_path = os.path.join(dir_path, "subdir2")
    os.mkdir(subdir2_path)
    create_file(subdir2_path, "file4")
    subdir21_path = os.path.join(subdir2_path, "subdir21")
    os.mkdir(subdir21_path)
    create_file(subdir21_path, "file5")

    subdir3_path = os.path.join(dir_path, "subdir3")
    os.mkdir(subdir3_path)
    create_file(subdir3_path, "file4")
    subdir31_path = os.path.join(subdir3_path, "subdir31")
    os.mkdir(subdir31_path)
    create_file(subdir31_path, "file5")

    return dir_path


class TestZipArchiver(object):
    def test_should_get_valid_excluded_paths_when_empty_list_was_passed_to_get_excluded_paths(self):
        archiver = gradient.api_sdk.archivers.ZipArchiver()

        excluded = archiver.get_excluded_paths()

        assert excluded == {
            os.path.join(".git", "*"),
            os.path.join(".idea", "*"),
            os.path.join(".pytest_cache", "*"),
        }

    def test_should_get_valid_excluded_paths_when_list_of_files_was_passed_to_get_excluded_paths(self):
        archiver = gradient.api_sdk.archivers.ZipArchiver()

        excluded = archiver.get_excluded_paths(["some_file", "some_dir/some_other_file"])

        assert excluded == {
            os.path.join(".git", "*"),
            os.path.join(".idea", "*"),
            os.path.join(".pytest_cache", "*"),
            "some_file",
            os.path.join("some_dir", "some_other_file"),
        }

    def test_should_get_a_dictionary_of_file_paths_in_a_dir(self):
        test_dir = create_test_dir_tree()
        expected_paths = {
            "file1.txt": os.path.join(test_dir, "file1.txt"),
            "file2.jpg": os.path.join(test_dir, "file2.jpg"),
            os.path.join(".git", "some_file"): os.path.join(test_dir, ".git", "some_file"),
            os.path.join("subdir1", "file2.jpg"): os.path.join(test_dir, "subdir1", "file2.jpg"),
            os.path.join("subdir1", "file3.txt"): os.path.join(test_dir, "subdir1", "file3.txt"),
            os.path.join("subdir2", "subdir21", "file5"): os.path.join(test_dir, "subdir2", "subdir21", "file5"),
        }

        try:
            paths = gradient.api_sdk.archivers.ZipArchiver.get_file_paths(
                test_dir,
                excluded_paths=["file2",
                                os.path.join("subdir2", "file4"),
                                os.path.join("subdir3", "*"),
                                ],
            )

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
            "file1.txt",
            "file2.jpg",
            os.path.join("subdir1", "file2.jpg"),
            os.path.join("subdir1", "file3.txt"),
            os.path.join("subdir2", "subdir21", "file5"),
        }

        try:
            archiver = gradient.api_sdk.archivers.ZipArchiver()
            archiver.archive(temp_input_dir, archive_file_path,
                             exclude=["file2", os.path.join("subdir2", "file4"), os.path.join("subdir3", "*")])

            zip_file = zipfile.ZipFile(archive_file_path)
            zip_file.extractall(temp_dir_for_extracted_files)
            archiver2 = gradient.api_sdk.archivers.ZipArchiver()
            archiver2.default_excluded_paths = []
            paths_in_extracted_dir = archiver2.get_file_paths(temp_dir_for_extracted_files)

        finally:
            shutil.rmtree(temp_dir)

        assert set(paths_in_extracted_dir.keys()) == expected_paths


class TestS3FileUploader(object):
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_upload_file_to_s3_and_get_bucket_url_when_upload_was_executed(self, post_patched):
        _, file_path = tempfile.mkstemp()
        uploader = gradient.api_sdk.s3_uploader.S3FileUploader()

        uploader.upload(file_path, "s3://some.url", {"key": "some_key"})

        post_patched.assert_called_once()


class TestExperimentWorkspaceDirectoryUploader(object):
    WORKSPACE_DIR_PATH = "/some/workspace/dir/path/"
    TEMP_DIR_PATH = "/some/temp/dir/path/"

    @mock.patch("gradient.api_sdk.s3_uploader.ExperimentFileUploader")
    @mock.patch("gradient.api_sdk.s3_uploader.ZipArchiver")
    def test_class_with_default_params(self, zip_archiver_cls, s3_project_file_uploader_cls):
        zip_archiver = mock.MagicMock()
        zip_archiver_cls.return_value = zip_archiver
        s3_project_file_uploader = mock.MagicMock()
        s3_project_file_uploader.upload.return_value = "s3://url/to/bucket"
        s3_project_file_uploader_cls.return_value = s3_project_file_uploader
        archive_path = os.path.join(tempfile.gettempdir(), "temp.zip")

        uploader = gradient.ExperimentWorkspaceDirectoryUploader("some_api_key", ps_client_name="some_client_name")
        bucket_url = uploader.upload(self.WORKSPACE_DIR_PATH, "some_project_id")

        s3_project_file_uploader_cls.assert_called_once_with("some_api_key", ps_client_name="some_client_name")
        zip_archiver.archive.assert_called_once_with(self.WORKSPACE_DIR_PATH, archive_path, exclude=None)
        s3_project_file_uploader.upload.assert_called_once_with(archive_path, "some_project_id")
        assert bucket_url == "s3://url/to/bucket"

    def test_should_run_upload_(self):
        zip_archiver = mock.MagicMock()
        s3_project_file_uploader = mock.MagicMock()
        s3_project_file_uploader.upload.return_value = "s3://url/to/bucket"
        temp_file_name = "some_temp_file_name.zip"
        archive_path = os.path.join(self.TEMP_DIR_PATH, temp_file_name)

        uploader = gradient.ExperimentWorkspaceDirectoryUploader(
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
