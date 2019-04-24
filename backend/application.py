"""
Main application.
"""
import bottle
import routes
import settings

application = bottle.Bottle()
application.catchall = True

bottle.debug(settings.DEBUG)

# Set up routes for app.
routes.setup_routing(application)

if __name__ == "__main__":
    bottle.run(
        application,
        server=settings.SERVER,
        reloader=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT
    )
