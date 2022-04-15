import abc
import mimetypes
import multiprocessing
import os
import re
import threading
import uuid
import json
try:
    import queue
except ImportError:
    import Queue as queue
from xml.etree import ElementTree
from urllib.parse import urlparse
from ..api_sdk.clients import http_client
from ..api_sdk.config import config
from ..cli_constants import CLI_PS_CLIENT_NAME

import halo
import requests
import six

from gradient import api_sdk
from gradient.api_sdk.sdk_exceptions import ResourceFetchingError
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, DetailsCommandMixin, ListCommandPagerMixin
from gradient.exceptions import ApplicationError

S3_XMLNS = 'http://s3.amazonaws.com/doc/2006-03-01/'


class WorkerPool(object):

    def __init__(self, count=None, min_count=4, max_count=16, cpu_multiplier=1):
        if count is None:
            count = min(max(round(multiprocessing.cpu_count() *
                                  cpu_multiplier), min_count), max_count)

        self._work = queue.Queue(maxsize=count)
        self._threads = [self._create_thread() for _ in range(count)]

        self._exception = None
        self._exception_lock = threading.Lock()

        self._completed_count = 0
        self._completed_lock = threading.Lock()

        self.worker_count = count

    def _create_thread(self):
        t = threading.Thread(target=self._worker)
        t.setDaemon(True)
        return t

    def __enter__(self):
        for thread in self._threads:
            thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._exception:
            raise self._exception

        for _ in range(self.worker_count):
            try:
                self._work.put(None, block=True, timeout=1)
            except queue.Full:
                break

        self._work.join()

        for thread in self._threads:
            thread.join()

    def _worker(self):
        while not self.has_exception():
            try:
                work = self._work.get(block=True, timeout=1)
            except queue.Empty:
                continue

            try:
                if work is None:
                    return

                (func, args, kwargs) = work
                func(*args, **kwargs)

                with self._completed_lock:
                    self._completed_count += 1
            except Exception as e:
                self.set_exception(e)
            finally:
                self._work.task_done()

    def put(self, func, *args, **kwargs):
        while not self.has_exception():
            try:
                return self._work.put((func, args, kwargs), block=True, timeout=1)
            except queue.Full:
                pass

    def set_exception(self, exception):
        with self._exception_lock:
            if not self._exception:
                self._exception = exception

    def has_exception(self):
        with self._exception_lock:
            return self._exception is not None

    def completed_count(self):
        with self._completed_lock:
            return self._completed_count


@six.add_metaclass(abc.ABCMeta)
class BaseDatasetsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        return api_sdk.clients.DatasetsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )


class ListDatasetsCommand(ListCommandPagerMixin, BaseDatasetsCommand):
    def _get_table_data(self, objects):
        data = [('Name', 'ID', 'Storage Provider')]
        for dataset in objects:
            data.append((
                dataset.name,
                dataset.id,
                '{} ({})'.format(
                    dataset.storage_provider.name,
                    dataset.storage_provider.id
                ),
            ))
        return data


class ShowDatasetDetailsCommand(DetailsCommandMixin, BaseDatasetsCommand):
    def _get_table_data(self, instance):
        data = (
            ('Name', instance.name),
            ('ID', instance.id),
            ('Description', instance.description or ''),
            ('StorageProvider', '{} ({})'.format(
                instance.storage_provider.name,
                instance.storage_provider.id
            )),
        )
        return data


class CreateDatasetCommand(BaseDatasetsCommand):
    def execute(self, name, storage_provider_id, description=None):
        dataset_id = self.client.create(
            name=name,
            storage_provider_id=storage_provider_id,
            description=description,
        )
        self.logger.log('Created dataset: {}'.format(dataset_id))


class UpdateDatasetCommand(BaseDatasetsCommand):
    def execute(self, dataset_id, name=None, description=None):
        self.client.update(
            dataset_id=dataset_id,
            name=name,
            description=description,
        )
        self.logger.log('Updated dataset: {}'.format(dataset_id))


class DeleteDatasetCommand(BaseDatasetsCommand):
    def execute(self, dataset_id):
        self.client.delete(dataset_id)
        self.logger.log('Deleted dataset: {}'.format(dataset_id))


@six.add_metaclass(abc.ABCMeta)
class BaseDatasetVersionsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        return api_sdk.clients.DatasetVersionsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )


class ListDatasetVersionsCommand(ListCommandPagerMixin, BaseDatasetVersionsCommand):
    def _get_table_data(self, objects):
        data = [('ID', 'Message', 'Tags')]
        for dataset_version in objects:
            data.append((
                '{}:{}'.format(self._id, dataset_version.version),
                dataset_version.message or '',
                ', '.join([t.name for t in dataset_version.tags])
            ))
        return data

    def execute(self, **kwargs):
        self._id = kwargs['dataset_id']
        return super(ListDatasetVersionsCommand, self).execute(**kwargs)


class ShowDatasetVersionDetailsCommand(DetailsCommandMixin, BaseDatasetVersionsCommand):
    def _get_table_data(self, instance):
        data = (
            ('ID', self._id),
            ('Message', instance.message or ''),
            ('Committed', str(instance.is_committed).lower()),
            ('Tags', ', '.join([t.name for t in instance.tags])),
        )
        return data

    def execute(self, dataset_version_id, **kwargs):
        self._id = dataset_version_id
        return super(ShowDatasetVersionDetailsCommand, self).execute(dataset_version_id, **kwargs)


class CreateDatasetVersionCommand(BaseDatasetVersionsCommand):
    def execute(self, dataset_id, message=None, source_paths=None):
        if source_paths:
            for source_path in source_paths:
                if not os.path.exists(source_path):
                    raise ApplicationError(
                        'Source path not found: {}'.format(source_path))

        version = self.client.create(dataset_id=dataset_id, message=message)
        dataset_version_id = '{}:{}'.format(dataset_id, version)
        self.logger.log(
            'Created dataset version: {}'.format(dataset_version_id))

        if source_paths:
            create = PutDatasetFilesCommand(
                api_key=self.api_key, logger=self.logger)
            create.execute(dataset_version_id,
                           source_paths=source_paths, target_path='/')

            commit = CommitDatasetVersionCommand(
                api_key=self.api_key, logger=self.logger)
            commit.execute(dataset_version_id)


class UpdateDatasetVersionCommand(BaseDatasetVersionsCommand):
    def execute(self, dataset_version_id, message=None):
        self.client.update(dataset_version_id, message=message)
        self.logger.log(
            'Updated dataset version: {}'.format(dataset_version_id))


class CommitDatasetVersionCommand(BaseDatasetVersionsCommand):
    def execute(self, dataset_version_id, message=None):
        dataset_version = self.client.get(dataset_version_id)
        if dataset_version.is_committed:
            self.logger.log('Dataset version already committed')
            return

        self.client.update(dataset_version_id, is_committed=True)
        self.logger.log(
            'Committed dataset version: {}'.format(dataset_version_id))


class DeleteDatasetVersionCommand(BaseDatasetVersionsCommand):
    def execute(self, dataset_version_id):
        self.client.delete(dataset_version_id)
        self.logger.log(
            'Deleted dataset version: {}'.format(dataset_version_id))


@six.add_metaclass(abc.ABCMeta)
class BaseDatasetTagsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        return api_sdk.clients.DatasetTagsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )


class ListDatasetTagsCommand(ListCommandPagerMixin, BaseDatasetTagsCommand):
    def _get_table_data(self, objects):
        data = [('ID', 'Name')]
        for dataset_tag in objects:
            data.append((
                '{}:{}'.format(self._id, dataset_tag.version.version),
                dataset_tag.name,
            ))
        return data

    def execute(self, **kwargs):
        self._id, _, _ = kwargs['dataset_id'].partition(':')
        return super(ListDatasetTagsCommand, self).execute(**kwargs)


class SetDatasetTagCommand(BaseDatasetTagsCommand):
    def execute(self, dataset_version_id, name):
        self.client.set(dataset_version_id, name=name)
        dataset_id, _, _ = dataset_version_id.partition(':')
        self.logger.log('Set dataset tag: {}:{}'.format(dataset_id, name))


class DeleteDatasetTagCommand(BaseDatasetTagsCommand):
    def execute(self, dataset_tag_id):
        self.client.delete(dataset_tag_id)
        self.logger.log('Deleted dataset tag: {}'.format(dataset_tag_id))


@six.add_metaclass(abc.ABCMeta)
class BaseDatasetFilesCommand(BaseDatasetVersionsCommand):
    def __init__(self, *args, **kwargs):
        super(BaseDatasetFilesCommand, self).__init__(*args, **kwargs)
        self.dataset_client = api_sdk.clients.DatasetsClient(
            api_key=self.api_key,
            logger=self.logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )

    def assert_supported(self, dataset_id):
        dataset_id, _, _ = dataset_id.partition(':')

        dataset = self.dataset_client.get(dataset_id)
        if dataset.storage_provider.type != 's3':
            raise ApplicationError(
                '%s storage type not supported' % dataset.storage_provider.type)

    def resolve_dataset_version_id(self, dataset_ref):
        try:
            dataset_ref = self.dataset_client.get_ref(dataset_ref)
            if dataset_ref and dataset_ref.version:
                dataset_ref = '{}:{}'.format(
                    dataset_ref.id, dataset_ref.version.version)
        except ResourceFetchingError:
            pass
        return dataset_ref

    @staticmethod
    def validate_s3_response(response):
        if not response.ok:
            raise ApplicationError('Failed to execute request against storage provider: %s\n\n%s' %
                                   (response.status_code, response.text))

    @staticmethod
    def report_connection_error(exception):
        raise ApplicationError('Failed to execute request against storage provider: %s' %
                               exception)

    @staticmethod
    def normalize_path(path):
        if not path:
            return '/'
        path = re.sub(r'/+', '/', path)
        if not path.startswith('/'):
            path = '/' + path
        return path

    def get_object(self, dataset_version_id, path):
        path = path.lstrip('/')

        if not path:
            return

        pre_signed = self.client.generate_pre_signed_s3_url(
            dataset_version_id,
            method='headObject',
            params={'Key': path},
        )

        try:
            response = requests.head(pre_signed.url)
            if response.status_code == 404:
                return
            self.validate_s3_response(response)

            size = response.headers.get('Content-Length', 0)
            return {'key': path, 'size': size}
        except requests.exceptions.ConnectionError as e:
            return self.report_connection_error(e)

    def list_objects(self, dataset_version_id, recursive=False, path='/', absolute=False, max_keys=20):
        path = self.normalize_path(path)

        if not path.endswith('/'):
            path += '/'

        next_continuation_token = None

        while True:
            params = {'Prefix': path, 'MaxKeys': max_keys}
            if next_continuation_token:
                params['ContinuationToken'] = next_continuation_token
            if recursive:
                params['Delimiter'] = ''

            pre_signed = self.client.generate_pre_signed_s3_url(
                dataset_version_id,
                method='listObjectsV2',
                params=params,
            )

            try:
                response = requests.get(pre_signed.url)
                self.validate_s3_response(response)
            except requests.exceptions.ConnectionError as e:
                self.report_connection_error(e)
                return

            tree = ElementTree.fromstring(response.text)

            prefix = tree.find('{' + S3_XMLNS + '}Prefix').text
            results = []
            next_continuation_token = None

            key_prefix = path[1:] if absolute else ''

            for item in tree:
                name = item.tag.rpartition('}')[2]
                if name == 'Contents':
                    key = item.find('{' + S3_XMLNS + '}Key').text[len(prefix):]
                    is_dir = key.endswith('/')

                    if not key or (recursive and is_dir):
                        continue

                    result = {'key': key_prefix + key}
                    if not is_dir:
                        result['size'] = item.find(
                            '{' + S3_XMLNS + '}Size').text

                    results.append(result)
                elif name == 'NextContinuationToken':
                    next_continuation_token = item.text
                elif name == 'CommonPrefixes':
                    if recursive:
                        continue
                    key = item.find(
                        '{' + S3_XMLNS + '}Prefix').text[len(prefix):]
                    results.append({'key': key_prefix + key})

            yield results, bool(next_continuation_token)

            if not next_continuation_token:
                break


class ListDatasetFilesCommand(ListCommandPagerMixin, BaseDatasetFilesCommand):
    def _get_table_data(self, objects):
        data = [('Name', 'Size')]
        for obj in objects:
            data.append((
                obj['key'],
                obj.get('size', ''),
            ))
        return data

    def _get_instances(self, kwargs):
        self.assert_supported(kwargs['dataset_version_id'])

        kwargs['dataset_version_id'] = self.resolve_dataset_version_id(
            kwargs['dataset_version_id'])

        return self.list_objects(**kwargs)


class GetDatasetFilesCommand(BaseDatasetFilesCommand):

    @classmethod
    def _get(cls, url, path):
        dir_path = os.path.dirname(path)
        tmp_path = path + '.tmp-%s' % uuid.uuid4()

        if os.path.exists(path) and not os.path.isfile(path):
            raise ApplicationError('%s already exists' % path)

        os.makedirs(dir_path, exist_ok=True)

        try:
            with requests.Session() as session:
                try:
                    with session.get(url, stream=True) as r:
                        cls.validate_s3_response(r)
                        with open(tmp_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                except requests.exceptions.ConnectionError as e:
                    return cls.report_connection_error(e)

            os.rename(tmp_path, path)
        finally:
            if os.path.isfile(tmp_path):
                os.remove(tmp_path)

    def execute(self, dataset_version_id, source_paths, target_path):
        self.assert_supported(dataset_version_id)

        dataset_version_id = self.resolve_dataset_version_id(
            dataset_version_id)

        target_path = os.path.abspath(target_path)

        if not source_paths:
            source_paths = ['/']

        status_text = 'Downloading files'

        with halo.Halo(text=status_text, spinner='dots') as status:
            with WorkerPool() as pool:
                for source_path in source_paths:
                    source_path = self.normalize_path(source_path)

                    list_objects = None
                    is_file = False
                    has_trailing_slash = source_path.endswith('/')

                    if not has_trailing_slash:
                        result = self.get_object(
                            dataset_version_id, source_path)
                        if result is not None:
                            list_objects = [([result], False)]
                            is_file = True

                    if not list_objects:
                        list_objects = self.list_objects(
                            dataset_version_id=dataset_version_id,
                            path=source_path,
                            recursive=True,
                            absolute=True,
                            max_keys=max(pool.worker_count * 2, 64)
                        )

                    def update_status():
                        status.text = '{}: {} ({})  '.format(
                            status_text, source_path, pool.completed_count())

                    for results, _ in list_objects:
                        if not results:
                            break

                        pre_signeds = self.client.generate_pre_signed_s3_urls(
                            dataset_version_id,
                            calls=[dict(method='getObject', params=dict(
                                Key=r['key'])) for r in results],
                        )

                        for result, pre_signed in zip(results, pre_signeds):
                            if is_file:
                                path = target_path
                            elif has_trailing_slash:
                                path = os.path.join(
                                    target_path, result['key'][len(source_path)-1:])
                            else:
                                path = os.path.join(target_path, result['key'])

                            update_status()
                            pool.put(self._get, url=pre_signed.url, path=path)


class PutDatasetFilesCommand(BaseDatasetFilesCommand):

    # @classmethod
    def _put(self, path, url, content_type, dataset_version_id=None, key=None):
        size = os.path.getsize(path)
        with requests.Session() as session:
            headers = {'Content-Type': content_type}

            try:
                if size <= 0:
                    headers.update({'Content-Size': '0'})
                    r = session.put(url, data='', headers=headers, timeout=5)
                # for files under half a GB
                elif size <= (10e8) / 2:
                    with open(path, 'rb') as f:
                        r = session.put(
                            url, data=f, headers=headers, timeout=5)
                # # for chonky files, use a multipart upload
                else:
                    # Chunks need to be at least 5MB or AWS throws an
                    # EntityTooSmall error; we'll arbitrarily choose a
                    # 15MB chunksize
                    #
                    # Note also that AWS limits the max number of chunkc
                    # in a multipart upload to 10000, so this setting
                    # currently enforces a hard limit on 150GB per file.
                    #
                    # We can dynamically assign a larger part size if needed,
                    # but for the majority of use cases we should be fine
                    # as-is
                    part_minsize = int(15e6)
                    dataset_id, _, version = dataset_version_id.partition(":")
                    mpu_url = f'/datasets/{dataset_id}/versions/{version}/s3/preSignedUrls'

                    api_client = http_client.API(
                        api_url=config.CONFIG_HOST,
                        api_key=self.api_key,
                        ps_client_name=CLI_PS_CLIENT_NAME
                    )

                    mpu_create_res = api_client.post(
                        url=mpu_url,
                        json={
                            'datasetId': dataset_id,
                            'version': version,
                            'calls': [{
                                'method': 'createMultipartUpload',
                                'params': {'Key': key}
                            }]
                        }
                    )
                    mpu_data = json.loads(mpu_create_res.text)[0]['url']

                    parts = []
                    with open(path, 'rb') as f:
                        # we +2 the number of parts since we're doing floor
                        # division, which will cut off any trailing part
                        # less than the part_minsize, AND we want to 1-index
                        # our range to match what AWS expects for part
                        # numbers
                        for part in range(1, (size // part_minsize) + 2):
                            presigned_url_res = api_client.post(
                                url=mpu_url,
                                json={
                                    'datasetId': dataset_id,
                                    'version': version,
                                    'calls': [{
                                        'method': 'uploadPart',
                                        'params': {
                                            'Key': key,
                                            'UploadId': mpu_data['UploadId'],
                                            'PartNumber': part
                                        }
                                    }]
                                }
                            )

                            presigned_url = json.loads(
                                presigned_url_res.text
                            )[0]['url']

                            chunk = f.read(part_minsize)
                            for attempt in range(0, 5):
                                part_res = session.put(
                                    presigned_url,
                                    data=chunk,
                                    timeout=5)
                                if part_res.status_code == 200:
                                    break

                            if part_res.status_code != 200:
                                # Why do we silence exceptions that get
                                # explicitly raised? Mystery for the ages, but
                                # there you have it I guess...
                                print(f'\nUnable to complete upload of {path}')
                                raise ApplicationError(
                                    f'Unable to complete upload of {path}')
                            etag = part_res.headers['ETag'].replace('"', '')
                            parts.append({'ETag': etag, 'PartNumber': part})
                            # This is a pretty jank way to get about multipart
                            # upload status updates, but we structure the Halo
                            # spinner to report on the number of completed
                            # tasks dispatched to the workers in the pool.
                            # Since it's more of a PITA to properly distribute
                            # this MPU among all workers than I really want to
                            # deal with, that means we can't easily plug into
                            # Halo for these updates. But we can print to
                            # console! Which again, jank and noisy, but arguably
                            # better than a task sitting forever, never either
                            # completing or emitting an error message.
                            if len(parts) % 7 == 0:  # About every 100MB
                                print(
                                    f'\nUploaded {len(parts) * part_minsize / 10e5}MB '
                                    f'of {int(size / 10e5)}MB for '
                                    f'{path}'
                                )

                    r = api_client.post(
                        url=mpu_url,
                        json={
                            'datasetId': dataset_id,
                            'version': version,
                            'calls': [{
                                'method': 'completeMultipartUpload',
                                'params': {
                                    'Key': key,
                                    'UploadId': mpu_data['UploadId'],
                                    'MultipartUpload': {'Parts': parts}
                                }
                            }]
                        }
                    )

                self.validate_s3_response(r)
            except requests.exceptions.ConnectionError as e:
                return self.report_connection_error(e)
            except Exception as e:
                return e

    @staticmethod
    def _list_files(source_path):
        if os.path.isfile(source_path):
            yield True, source_path
            return

        if os.path.isdir(source_path):
            for dir_path, _, names in os.walk(source_path):
                for name in names:
                    yield False, os.path.join(dir_path, name)
            return

        raise ApplicationError('Invalid source path: ' + source_path)

    def _sign_and_put(self, dataset_version_id, pool, results, update_status):
        pre_signeds = self.client.generate_pre_signed_s3_urls(
            dataset_version_id,
            calls=[dict(method='putObject', params=dict(
                Key=r['key'], ContentType=r['mimetype'])) for r in results],
        )

        for pre_signed, result in zip(pre_signeds, results):
            update_status()
            pool.put(
                self._put,
                url=pre_signed.url,
                path=result['path'],
                content_type=result['mimetype'],
                dataset_version_id=dataset_version_id,
                key=result['key'])

    def execute(self, dataset_version_id, source_paths, target_path):
        self.assert_supported(dataset_version_id)

        if not target_path:
            target_path = '/'
        else:
            target_path = self.normalize_path(target_path)
            if not target_path.endswith('/'):
                target_path += '/'

        status_text = 'Uploading files'

        with halo.Halo(text=status_text, spinner='dots') as status:
            with WorkerPool() as pool:
                for source_path in source_paths:
                    has_trailing_slash = source_path.endswith(os.path.sep)
                    source_path = os.path.abspath(source_path)
                    source_name = os.path.basename(source_path)

                    def update_status():
                        status.text = '{}: {} ({})'.format(
                            status_text, source_path, pool.completed_count())

                    results = []

                    for source_path_is_file, path in self._list_files(source_path):
                        path = path.replace(os.path.sep, '/')

                        key = target_path
                        if source_path_is_file:
                            key += source_name
                        else:
                            if not has_trailing_slash:
                                key += source_name + '/'
                            key += path[len(source_path)+1:]

                        mimetype = mimetypes.guess_type(
                            key)[0] or 'application/octet-stream'

                        results.append(
                            dict(key=key, path=path, mimetype=mimetype))

                        if len(results) == pool.worker_count:
                            self._sign_and_put(
                                dataset_version_id, pool, results, update_status)
                            results = []

                    if results:
                        self._sign_and_put(
                            dataset_version_id, pool, results, update_status)


class DeleteDatasetFilesCommand(BaseDatasetFilesCommand):

    @classmethod
    def _delete(cls, url):
        with requests.Session() as session:
            try:
                r = session.delete(url)
                cls.validate_s3_response(r)
            except requests.exceptions.ConnectionError as e:
                return cls.report_connection_error(e)

    def execute(self, dataset_version_id, paths):
        self.assert_supported(dataset_version_id)

        status_text = 'Deleting files'

        with halo.Halo(text=status_text, spinner='dots') as status:
            with WorkerPool() as pool:
                for path in paths:
                    path = self.normalize_path(path)

                    list_objects = None
                    has_trailing_slash = path.endswith('/')

                    def update_status():
                        status.text = '{}: {} ({})'.format(
                            status_text, path, pool.completed_count())

                    if not has_trailing_slash:
                        result = self.get_object(dataset_version_id, path)
                        if result is not None:
                            list_objects = [([result], False)]

                    if not list_objects:
                        list_objects = self.list_objects(
                            dataset_version_id=dataset_version_id,
                            path=path,
                            recursive=True,
                            absolute=True,
                        )

                    for results, _ in list_objects:
                        if not results:
                            break

                        pre_signeds = self.client.generate_pre_signed_s3_urls(
                            dataset_version_id,
                            calls=[dict(method='deleteObject', params=dict(
                                Key=r['key'])) for r in results],
                        )

                        for pre_signed in pre_signeds:
                            update_status()
                            pool.put(self._delete, url=pre_signed.url)
