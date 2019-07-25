import json
import os
import random
import shutil

import click
import requests
import six

from gradient import exceptions

MIN_NUM = 100
MAX_NUM = 999
adjs = [
    "autumn", "hidden", "bitter", "misty", "silent", "empty", "dry", "dark",
    "summer", "icy", "delicate", "quiet", "white", "cool", "spring", "winter",
    "patient", "twilight", "dawn", "crimson", "wispy", "weathered", "blue",
    "billowing", "broken", "cold", "damp", "falling", "frosty", "green", "long",
    "late", "lingering", "bold", "little", "morning", "muddy", "old", "red",
    "rough", "still", "small", "sparkling", "throbbing", "shy", "wandering",
    "withered", "wild", "black", "young", "holy", "solitary", "fragrant",
    "aged", "snowy", "proud", "floral", "restless", "divine", "polished",
    "ancient", "purple", "lively", "nameless"
]
nouns = [
    "waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning",
    "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter",
    "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook",
    "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly",
    "feather", "grass", "haze", "mountain", "night", "pond", "darkness",
    "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder",
    "violet", "water", "wildflower", "wave", "water", "resonance", "sun",
    "wood", "dream", "cherry", "tree", "fog", "frost", "voice", "paper", "frog",
    "smoke", "star"
]


def random_name_generator():
    return random.choice(adjs) + '-' + random.choice(nouns) + '-' + str(
        random.randint(MIN_NUM, MAX_NUM))


def get_terminal_lines(fallback=48):
    if six.PY3:
        return shutil.get_terminal_size().lines

    return fallback


def print_json_pretty(res):
    print(json.dumps(res, indent=2, sort_keys=True))


def response_error_check(res):
    if ('error' not in res
            and 'status' in res
            and (res['status'] < 200 or res['status'] > 299)):
        res['error'] = True
    return res


def requests_exception_to_error_obj(e):
    return {'error': True, 'message': str(e)}


def status_code_to_error_obj(status_code):
    message = 'unknown'
    if status_code in requests.status_codes._codes:
        message = requests.status_codes._codes[status_code][0]
    return {'error': True, 'message': message, 'status': status_code}


def validate_workspace_input(input_data):
    workspace_url = input_data.get('workspaceUrl')
    workspace_path = input_data.get('workspace')
    workspace_archive = input_data.get('workspaceArchive')

    if (workspace_archive and workspace_path) \
            or (workspace_archive and workspace_url) \
            or (workspace_path and workspace_url):
        raise click.UsageError("Use either:"
                               "\n\t--workspace https://path.to/git/repository.git  - to point to a repository URL"
                               "\n\t--workspace /path/to/local/directory            - to point to a project directory"
                               "\n\t--workspace /path/to/local/archive.zip          - to point to a .zip archive"
                               "\n\t--workspace none                                - to use no workspace"
                               "\n or neither to use current directory")


class PathParser(object):
    LOCAL_DIR = 0
    LOCAL_FILE = 1
    GIT_URL = 2
    S3_URL = 3

    @classmethod
    def parse_path(cls, path):
        if cls.is_local_dir(path):
            return cls.LOCAL_DIR

        if cls.is_local_zip_file(path):
            return cls.LOCAL_FILE

        if cls.is_git_url(path):
            return cls.GIT_URL

        if cls.is_s3_url(path):
            return cls.S3_URL

        raise exceptions.WrongPathError("Given path is neither local path, nor valid URL")

    @staticmethod
    def is_local_dir(path):
        return os.path.exists(path) and os.path.isdir(path)

    @staticmethod
    def is_local_zip_file(path):
        return os.path.exists(path) and os.path.isfile(path) and path.endswith(".zip")

    @staticmethod
    def is_git_url(path):
        return not os.path.exists(path) and path.endswith(".git") or path.lower().startswith("git:")

    @staticmethod
    def is_s3_url(path):
        return not os.path.exists(path) and path.lower().startswith("s3:")
