import os
import flask
import flask_restful

from src.server.berry_stats import BerryStats

DEBUG = eval(os.environ.get("DEBUG", "False"))


def run():
    """Add the required server resources and starts the server."""
    app = flask.Flask(__name__)
    api = flask_restful.Api(app)
    api.add_resource(BerryStats, "/allBerryStats")
    app.run(debug=DEBUG)
