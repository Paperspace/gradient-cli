from src.paperspace.session import Session

# Versioning should follow the PEP 440 scheme
# See also:
# https://setuptools.pypa.io/en/latest/userguide/distribution.html
__version__ = "1.0-alpha1"

global DEFAULT_SESSION
DEFAULT_SESSION = Session()


def session_decorator(func):
    def execute_with_session(session: Session=DEFAULT_SESSION, *args, **kwargs):
        return func(*args, **kwargs, session=session)
    return execute_with_session
