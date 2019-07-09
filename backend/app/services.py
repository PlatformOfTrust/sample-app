"""
Application services are found in this file.
"""
import requests
import settings


class Request(object):
    """Handles request forwarding to LE APIs."""

    def __init__(self, api: str):
        """Initialise Request class.

        :param api: Defined API endpoint by api's name
        :type api: str
        :raise KeyError: If given API doesn't exist
        """
        self._apis = {
            'login': settings.LOGIN_APP_API_URL,
            'identity': settings.IDENTITY_API_URL,
            'broker': settings.BROKER_API_URL
        }

        self._api_url = self._apis[api]

    def get(self, path: str, headers: dict = None,
            authorization_token: str = None) -> requests.Response:
        """Send GET request to API.

        :param path: API endpoint
        :type path: str
        :param headers: HTTP headers
        :type path: dict
        :param authorization_token: Authorization token
        :type authorization_token: str
        :return: 'GET' HTTP response
        :rtype: dict
        """

        if not headers:
            headers = {}

        if authorization_token:
            headers['Authorization'] = authorization_token

        return requests.get(f'{self._api_url}{path}', headers=headers)

    def post(self, path: str, data: dict,
             headers: dict = None,
             authorization_token: str = None) -> requests.Response:
        """Send POST request to API.

        :param path: API endpoint
        :type path: str
        :param data: List of arguments for POST request.
        :type data: dict
        :param headers: List of headers
        :type headers: dict
        :param authorization_token: Authorization token
        :type authorization_token: str
        :return: 'POST' HTTP response
        :rtype: dict
        """

        if not headers:
            headers = {}

        if authorization_token:
            headers['Authorization'] = authorization_token

        return requests.post(f'{self._api_url}{path}', json=data,
                             headers=headers)
