import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app
from QP.auth.models import User
from QP.car.models import Car
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint
from sqlalchemy import desc


srt = Blueprint('sort', __name__)


class SortHandler():
    def __init__(self):
        pass

    @staticmethod
    @srt.route('/cars/<field>/<int:ascending>', methods=["GET"])
    @login_required
    def sort_car(field, ascending):
        if field == 'year':
            if ascending == 1:
                cars = Car.query.filter(Car.year.isnot(None)).order_by(Car.year).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.year.isnot(None)).order_by(desc(Car.year)).all()
            else:
                response = ResponseObject.ResponseObject(obj=None, status='wrong input!')
                return jsonify(response.serialize())
        elif field == 'price':
            if ascending == 1:
                cars = Car.query.filter(Car.price.isnot(None)).order_by(Car.price).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.price.isnot(None)).order_by(desc(Car.price)).all()
            else:
                response = ResponseObject.ResponseObject(obj=None, status='wrong input!')
                return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=None, status='wrong field!')
            return jsonify(response.serialize())
        if cars is None:
            response = ResponseObject.ResponseObject(obj=None, status='no cars in the database!')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=cars, status='OK')
        return jsonify(response.serialize())
