# One place to change the environment names.
ENV_DEVELOPMENT = 'development'

SUPPORTED_ENVIRONMENTS = [
    ENV_DEVELOPMENT,
]

ENV = ENV_DEVELOPMENT

# server backend (cherrypy, gunicorn, waitress, tornado, wsgiref, ...)
# if set to '', a default server backend will be used
SERVER = 'wsgiref'

# define host
HOST = '0.0.0.0'
# define port
PORT = 8080

# debug error messages
DEBUG = True

# auto-reload
RELOAD = True

GRANT_TYPES = {
    'authorization': 'authorization',
    'exchange_token': 'authorization_code'
}
RESPONSE_TYPE = 'code'

SSL_ENABLED = False

LOGIN_APP_URL = 'https://login-sandbox.oftrust.net'

BROKER_API_URL = 'https://api-sandbox.oftrust.net/broker/v1'
IDENTITY_API_URL = 'https://api-sandbox.oftrust.net/identities/v1'
LOGIN_APP_API_URL = 'https://login-sandbox.oftrust.net/api'

APP_HOST = 'sample-app.local:32600'

APP_URL = f'{"https" if SSL_ENABLED else "http"}://{APP_HOST}'
REDIRECT_URL = f'{APP_URL}/api/exchangeToken'

# You can get all values listed below after creating an application.
# Go to https://world-sandbox.oftrust.net/

ACCESS_TOKENS = [
    '',
    ''
]

CLIENT_SECRET = ''
CLIENT_ID = ''
