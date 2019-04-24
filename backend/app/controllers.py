"""
Application controllers are found in this file.

One controller per model to handle creating, updating and deleting.
All controllers should be derived from the Base class.
The Base contains attributes and functions common to all controllers.
"""
import bottle
import common.responses as responses
from common.utils import request_args, \
    get_ts, rfc3339, generate_signature
import settings
from app import services
from webargs import fields
from http.cookies import Morsel


class Base(object):
    """Base controller class.

    All controllers should derive from this class.
    """
    _app = None

    def __init__(self, app: bottle.Bottle = None):
        if app is not None:
            self._app = app

    def set_app(self, app: bottle.Bottle):
        """Sets the Bottle app for the controller.

        :param app: The Bottle application.
        :type app: bottle.Bottle
        :return: None
        :rtype: None
        """
        self._app = app


class Status(Base):
    """Status controller.

    Adds a health check endpoint to the API.
    """

    @staticmethod
    def health_check() -> dict:
        """Returns an empty response.

        Used for API health check endpoint.

        :return: An empty response.
        :rtype: dict
        """
        return responses.JSONResponse({})


class Login(Base):
    """Auth

    Handles Login API requests
    """

    def __init__(self, app: bottle.Bottle = None):
        super().__init__(app)
        self._request = services.Request('login')
        self._login_authorization_uri = f'{settings.LOGIN_APP_URL}' \
            f'?grant_type={settings.GRANT_TYPES["authorization"]}' \
            f'&response_type={settings.RESPONSE_TYPE}' \
            f'&redirect_uri={settings.REDIRECT_URL}' \
            f'&client_id={settings.CLIENT_ID}'

    def exchange_token(self) -> responses.JSONResponse:
        """ Pass request to login app

        :return: Access token data.
        :rtype: responses.JSONResponse
        """

        code = bottle.request.params.get('code', None)

        if code is None:
            return responses.JSONResponse(
                body={'message': 'Authorization failed'},
                status=406
            )

        auth_api_response = self._request.post('/exchangeToken', {
            'client_secret': settings.CLIENT_SECRET,
            'client_id': settings.CLIENT_ID,
            'redirect_uri': settings.REDIRECT_URL,
            'grant_type': settings.GRANT_TYPES['exchange_token'],
            'code': code
        })

        if auth_api_response.ok:
            data = auth_api_response.json()

            response = responses.JSONResponse(
                headers={
                    'Location': settings.APP_URL
                },
                status=303)

            # https://github.com/bottlepy/bottle/blob/master/bottle.py#L1848
            # In bottle starting from 0.13-dev
            Morsel._reserved.setdefault('samesite', 'SameSite')

            response.set_cookie('Authorization',
                                f'Bearer {data["access_token"]}',
                                max_age=data['expires_in'],
                                httponly=True,
                                secure=settings.SSL_ENABLED,
                                samesite='Strict')

            return response
        else:
            return responses.JSONResponse(body=auth_api_response.text,
                                          status=auth_api_response.status_code)

    def me(self) -> responses.JSONResponse:
        """Pass request to login app

        :return: Access token data.
        :rtype: responses.JSONResponse
        """

        response = self._request.get(
            '/me',
            authorization_token=bottle.request.get_cookie(
                'Authorization')
        )

        return responses.JSONResponse(body=response.text,
                                      status=response.status_code)

    def login(self) -> responses.JSONResponse:
        """Generate uri and send it to the client

        :return: Login uri.
        :rtype: responses.JSONResponse
        """

        uri = f'{self._login_authorization_uri}'

        return responses.JSONResponse({'uri': uri})

    def logout(self) -> responses.JSONResponse:
        """Delete authorization cookie(s)

        :return: Logout response.
        :rtype: responses.JSONResponse
        """

        response = responses.JSONResponse(
            body={'message': 'Logout'},
            status=200
        )

        response.delete_cookie('Authorization')

        return response


class Identity(Base):
    """Identity management.

    Handles all identity(vertex/node) related actions.
    """

    def __init__(self, app: bottle.Bottle = None):
        super().__init__(app)
        self._request = services.Request('identity')

    def read(self, id: str) -> responses.JSONResponse:
        """Returns one identity.

        :param id: The identity's ID.
        :type id: str
        :return: The found identity.
        :rtype: responses.JSONResponse
        """

        response = self._request.get(
            f'/{id}',
            authorization_token=bottle.request.get_cookie('Authorization'))

        return responses.JSONResponse(body=response.text,
                                      status=response.status_code)


class Broker(Base):
    """Broker controller.

    Handles data brokering between translators and PoT core.
    """

    def __init__(self, app: bottle.Bottle = None):
        super().__init__(app)
        self._request = services.Request('broker')

    @request_args({
        'productCode': fields.Str(required=True),
        'parameters': fields.Dict(required=True)
    })
    def fetch(self, args: dict) -> responses.JSONResponse:
        """Returns information from PoT translators.

        :param args: The arguments passed.
            parameters: Any additional parameters to be sent to the translator.
        :type args: dict
        :param productCode: Product code
        :type productCode: str
        :return: Data from the translator defined by the product code.
        :rtype: responses.JSONResponse
        """
        json = {
            'timestamp': rfc3339(),
            'productCode': args['productCode'],
            'parameters': args['parameters']
        }

        access_token = settings.ACCESS_TOKENS[0]

        headers = {
            'x-pot-app': settings.CLIENT_ID,
            'x-pot-signature': generate_signature(access_token, json)
        }

        response = self._request.post(f'/fetch-data-product', data=json,
                                      headers=headers)

        return responses.JSONResponse(body=response.text,
                                      status=response.status_code)
