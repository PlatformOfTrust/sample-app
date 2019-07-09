"""
Application routes and configuration are found in this file.

JSONResponse class to send json responses
"""
import app.controllers as controllers
import bottle
from webargs.bottleparser import use_args

# Instantiate the controllers here, for easy mocking.

status = controllers.Status()
login = controllers.Login()
identity = controllers.Identity()
broker = controllers.Broker()


def setup_routing(app: bottle.Bottle):
    status.set_app(app)
    login.set_app(app)
    identity.set_app(app)
    broker.set_app(app)

    # index
    app.route('/health', 'GET', status.health_check)

    # identities
    app.route('/identities/<id>', 'GET', identity.read)

    # login
    app.route('/exchangeToken', 'GET', login.exchange_token)
    app.route('/me', 'GET', login.me)
    app.route('/login', 'GET', login.login)
    app.route('/logout', 'GET', login.logout)

    # broker
    app.route('/fetch-data-product', 'POST', broker.fetch,
              apply=use_args(broker.fetch.args))
