import progressbar

from gradient.api_sdk.workspace import S3WorkspaceHandler, MultipartEncoder


class MultipartEncoderWithProgressbar(MultipartEncoder):
    @staticmethod
    def _create_callback(encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            if monitor.bytes_read == bar.max_value:
                bar.finish()
            else:
                bar.update(monitor.bytes_read)

        return callback


class S3WorkspaceHandlerWithProgressbar(S3WorkspaceHandler):
    DEFAULT_MULTIPART_ENCODER_CLS = MultipartEncoderWithProgressbar

    def _zip_files(self, zip_file, file_paths):
        self.bar = progressbar.ProgressBar(max_value=len(file_paths))
        super(S3WorkspaceHandlerWithProgressbar, self)._zip_files(zip_file, file_paths)
        self.bar.finish()

    def _zip_files_iterate_callback(self, i):
        self.bar.update(i)
