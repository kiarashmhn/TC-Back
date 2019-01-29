from flask import jsonify

from QP import app, auth_manager, Car
from flask import Blueprint

sea = Blueprint('sea', __name__)


class SearchApiHandler:
    @staticmethod
    @sea.route('/<query>', methods=["GET"])
    @auth_manager.authenticate
    def search(user, query):
        cars, total = Car.search(query, 1, 100)
        c = []
        for car in cars:
            c.append(car.serialize())
        out = {'object': c}
        return jsonify(out), 200
