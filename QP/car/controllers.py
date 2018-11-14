import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app
from QP.auth.models import User
from QP.car.models import Car
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint

car = Blueprint('car', __name__)


class CarHandler():
    def __init__(self):
        pass

    @car.route('/', methods=["POST"])
    @login_required
    def add_car():
        req = request.get_json()
        if req.get("user_id") is None:
            error = 'user_id field cannot be empty!'
            response = ResponseObject.ResponseObject(obj=None, status=error)
            return jsonify(response.serialize())
        elif User.query.filter_by(id=req.get("user_id")).first() is None:
            error = 'invalid user_id!'
            response = ResponseObject.ResponseObject(obj=None, status=error)
            return jsonify(response.serialize())
        else:
            carr = Car(name=req.get("name"),
                       factory=req.get("factory"),
                       kilometer=req.get("kilometer"),
                       year=req.get("year"),
                       color=req.get("color"),
                       description=req.get("description"),
                       automate=req.get("automate"),
                       price=req.get("price"),
                       user_id=req.get("user_id"))
            db.session.add(carr)
            db.session.commit()
            print("car added")
            response = ResponseObject.ResponseObject(obj=car, status='OK')
            return jsonify(response.serialize())

    @app.route('/<int:car_id>', methods=["DELETE"])
    @login_required
    def delete_car(car_id):
        if car_id is None:
            response = ResponseObject.ResponseObject(obj=None, status='car_id cannot be empty!')
            return jsonify(response.serialize())
        carr = Car.query.filter_by(id=car_id).first()
        if carr is None:
            response = ResponseObject.ResponseObject(obj=None, status='invalid car_id!')
            return jsonify(response.serialize())
        db.session.delete(carr)
        db.session.commit()
        response = ResponseObject.ResponseObject(obj=None, status='OK')
        return jsonify(response.serialize())
