"""
Generic helper functions are defined in this file.
"""
import base64
import hashlib
import hmac
import json
import time

from datetime import datetime, timezone


def rfc3339() -> str:
    """Gets the current datetime in UTC iso formatted string.

    E.g. "2019-01-01T12:00:00+00:00"

    :return: The current UTC datetime in ISO format.
    :rtype: str
    """
    return str(datetime.now(timezone.utc).isoformat(timespec='seconds'))


def generate_signature(secret: str, body: dict) -> str:
    """Returns the HMAC-SHA256 signature of the body.

    :param secret: The shared secret.
    :type secret: str
    :param body: The body to sign.
    :type body: dict
    :return: The generated signature.
    :rtype: str
    """
    digest = get_digest(secret, body)
    return base64.b64encode(digest).decode()


def get_digest(secret: str, body) -> str:
    """Returns the HMAC-SHA256 digest for the given body.

    :param secret: The shared secret.
    :type secret: str
    :param body: The body to generate the digest for.
    :type body: str|dict
    :return: The digest.
    :rtype: str
    :raise RuntimeError: If the body is not a string or dictionary.
    """
    body_hash = get_signature_payload(body)

    # Create the HMAC digest with SHA-256.
    return hmac.new(secret.encode('utf-8'),
                    body_hash.encode('utf-8'),
                    hashlib.sha256).digest()


def get_signature_payload(body) -> str:
    """Returns the signature payload as a string.

    The body of the payload may be a dict or a string.

    :param body: The body to be hashed.
    :type body: str|dict
    :return: The body hash.
    :rtype: str
    :raise RuntimeError: IF the body is not a string or dict.
    """
    if not isinstance(body, (str, dict)):
        raise RuntimeError(
            f'Invalid body type. Must be `str` or `dict`, got {type(body)}')

    # Create the hash from the body dict.
    if isinstance(body, dict):
        body_hash = json.dumps(
            body,
            sort_keys=True,
            indent=None,
            separators=(',', ': ')
        ).strip()
    else:
        body_hash = body.strip()  # Strip white space from start and end.

    return body_hash


def request_args(args):
    """Decorator for request arguments.

    Defines fields that should be passed to the controller action.

    :param args: The arguments of the request.
    :type args: dict
    :return: The decorator.
    :rtype:
    """

    def _decorator(f):
        f.args = args
        return f

    return _decorator


def get_ts() -> int:
    """Return current time in milliseconds

    :return: Current time in ms.
    :rtype: int
    """
    return int(time.time())
