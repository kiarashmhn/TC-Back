import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app
from QP.user.models import User
from QP.car.models import Car
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint
from sqlalchemy import desc


srt = Blueprint('sort', __name__)


class SortHandler():
    def __init__(self):
        pass

    def sort_car(self, field, ascending):
        cars = None
        if field == 'year':
            if ascending == 1:
                cars = Car.query.filter(Car.year.isnot(None)).filter(Car.is_rented.isnot(True)).order_by(Car.year).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.year.isnot(None)).filter(Car.is_rented.isnot(True)).order_by(desc(Car.year)).all()
        elif field == 'price':
            if ascending == 1:
                cars = Car.query.filter(Car.price.isnot(None)).filter(Car.is_rented.isnot(True)).order_by(Car.price).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.price.isnot(None)).filter(Car.is_rented.isnot(True)).order_by(desc(Car.price)).all()
        return cars


class SortApiHandler():
    sort_handler = SortHandler()

    def __init__(self):
        pass

    @staticmethod
    @srt.route('/cars/<field>/<int:ascending>', methods=["GET"])
    def sort_car(field, ascending):
        """
        This is the SortCars API
        Call this api passing the field you want to sort cars by in the path, and 1 to sort it ascending or 0 otherwise.
        ---
        tags:
          - SortCars API
        parameters:
          - name: field
            in: path
            type: string
            required: true
            description: the field you want to sort by.
          - name: ascending
            in: path
            type: integer
            required: true
            description: ascending or descending.
        responses:
          200:
            description: Ok.
            schema:
                type: object
                properties:
                  object:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                            example: i8
                            type: string
                        factory:
                            type: string
                            example: bmw
                        kilometer:
                            type: integer
                            example: 1000
                        year:
                            type: integer
                            example: 2018
                        color:
                            type: string
                            example: white
                        description:
                            type: string
                            example: bmw-i8
                        automate:
                            type: integer
                            example: 1
                        price:
                            type: integer
                            example: 1500000
                        user_id:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 3
          400,status="wrong input!":
            description: invalid ascending field!
          400,status="wrong field!":
            description: invalid field of car!
          400,status="no cars in the database!":
            description: empty database!
          401:
            description: You aren't logged in.
        """
        sort_handler = SortApiHandler.sort_handler
        if ascending != 0 and ascending != 1:
            out = {'status': 'wrong input!'}
            return jsonify(out), 400
        elif field != 'year' and field != 'price':
            out = {'status': 'wrong field!'}
            return jsonify(out), 400
        try:
            cars = sort_handler.sort_car(field, ascending)
            c = []
            for car in cars:
                c.append(car.serialize())
            out = {'object': c}
            return jsonify(out), 200
        except:
            out = {'status': 'no cars in the database!'}
            return jsonify(out), 400
