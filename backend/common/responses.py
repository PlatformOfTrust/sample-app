"""
Responses the API uses can be defined here.
"""
from bottle import HTTPResponse


class JSONResponse(HTTPResponse):
    """JSONResponse class.

    Content-Type defaults to application/json.
    This class should be used by default when returning data from the API.
    """

    def __init__(self, body='', status=None, headers=None, **more_headers):
        if headers is None:
            headers = dict()

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'

        super(JSONResponse, self).__init__(body, status, headers,
                                           **more_headers)
