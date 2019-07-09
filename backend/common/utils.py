"""
Generic helper functions are defined in this file.
"""
import base64
import hashlib
import hmac
import json
import time

from datetime import datetime, timezone
from binascii import hexlify


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
    :return: The generated base64 encoded signature
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
    payload = get_signature_payload(body)

    # Create the HMAC digest with SHA-256.
    return hmac.new(secret.encode('utf-8'),
                    payload.encode('utf-8'),
                    hashlib.sha256).digest()


def get_signature_payload(body) -> str:
    """Returns the signature payload as a string.

    The body of the payload may be a dict or a string.

    :param body: The body to be hashed.
    :type body: str|dict
    :return: JSON formatted string.
    :rtype: str
    :raise RuntimeError: IF the body is not a string or dict.
    """
    if not isinstance(body, (str, dict)):
        raise RuntimeError(
            f'Invalid body type. Must be `str` or `dict`, got {type(body)}')

    # Create the hash from the body dict.
    if isinstance(body, dict):
        json_str = json.dumps(
            body,
            sort_keys=True,
            indent=None,
            separators=(',', ': ')
        ).strip()
    else:
        json_str = body.strip()  # Strip white space from start and end.

    return json_str


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


def generate_state(data: dict, salt: str) -> str:
    """Generate oauth state base64 encoded string out of arbitrary data

    :param data: Data to be encrypted
    :type data: dict
    :param salt: Salt for randomized hashing
    :type salt: str
    :return: Base64 encoded string
    :rtype: str
    """
    data_bytes = json.dumps(data).encode()
    hash = hash_sha1(salt, data_bytes)

    state = {
        'd': data,
        'h': hash
    }

    return encode_base64_dict(state)


def validate_state(encoded_state: str, salt: str, expires_in: int) -> bool:
    """Validate oauth state

    :param encoded_state: Base64 encoded state
    :type encoded_state: str
    :param salt: Salt for randomized hashing
    :type salt: str
    :param expires_in: Validate timestamp against current time
    :type expires_in: int
    :return: True or False
    :rtype: bool
    """
    state = decode_base64_dict(encoded_state)
    state_data = state.get('d', {})

    ts = state_data.get('ts', None)
    now = get_ts()

    if ts and ts + expires_in < now:
        return False

    if generate_state(state_data, salt) != encoded_state:
        return False

    return True


def decode_base64_dict(base64_str: str) -> dict:
    """Decode Base64 string

    :param base64_str: Base64 encoded data
    :type base64_str: str
    :return: Data
    :rtype: dict
    """
    return json.loads(base64.b64decode(base64_str))


def encode_base64_dict(data: dict) -> str:
    """Encode dict into base64

    :param base64_str: Base64 encoded data
    :type base64_str: str
    :return: Data
    :rtype: dict
    """
    encode_data = base64.b64encode(json.dumps(data).encode())
    encode_data = encode_data.decode()

    return encode_data


def hash_sha1(salt: str, data_bytes: bytes) -> str:
    """Hash data and return decoded string

    :param salt: Salt for hashing
    :type salt: str
    :param data_bytes: Data in bytes
    :type data_bytes: bytes
    :return: Hash
    :rtype: str
    """
    hash = hmac.new(salt.encode(), data_bytes, hashlib.sha1).digest()
    return hexlify(hash).decode()
