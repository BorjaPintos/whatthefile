from flask import Flask
from settings import DevConfig
import routes

def addHeaders(app, config_object):
    @app.after_request
    def add_headers(resp):
        if resp.headers['Content-Type'] is None:
            resp.headers['Content-Type'] = 'application/json'
        resp.headers['Server'] = config_object.SERVERNAME
        if (config_object.PROTOCOL is 'https'):
            resp.headers['Strict-Transport-Security'] = 'max-age=31536000; \
                includeSubDomains'
        return resp


def create_app(config_object=DevConfig):
    """Create flask app."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    """Customize headers response"""
    addHeaders(app, config_object)

    """Add routes to app."""
    routes.importRoutes("/", app, config_object)

    """Run the app"""
    app.run(host=config_object.HOST, port=config_object.PORT)


if __name__== "__main__":
    app = create_app()