import flask
import flask_restful

from src.api import berry


class BerryStats(flask_restful.Resource):
    """Class that manages the allBerryStats endpoint."""

    def get(self):
        response: flask.Response = flask.make_response(berry.all_berry_stats())
        response.headers["Content-Type"] = "application/json"
        return response
