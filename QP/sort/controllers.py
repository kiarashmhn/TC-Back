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
            description: All responses have 200 status code; check the status field.
            schema:
                type: object
                properties:
                  object:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                            default: ali
                            type: string
                        factory:
                            type: string
                            default: bmw
                        kilometer:
                            type: integer
                        year:
                            type: integer
                        color:
                            type: string
                        description:
                            type: string
                        automate:
                            type: integer
                        price:
                            type: integer
                        user_id:
                            type: integer
                        id:
                            type: integer
                  status:
                    type: string
          200,status="OK":
            description: Cars successfully sorted; and returned in response.
          200,status="wrong input!":
            description: invalid ascending field!
          200,status="wrong field!":
            description: invalid field of car!
          200,status="no cars in the database!":
            description: empty database!
          401:
            description: You aren't logged in.
        """
        if field == 'year':
            if ascending == 1:
                cars = Car.query.filter(Car.year.isnot(None)).order_by(Car.year).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.year.isnot(None)).order_by(desc(Car.year)).all()
            else:
                response = ResponseObject.ResponseObject(obj=[Car()], status='wrong input!')
                return jsonify(response.serialize())
        elif field == 'price':
            if ascending == 1:
                cars = Car.query.filter(Car.price.isnot(None)).order_by(Car.price).all()
            elif ascending == 0:
                cars = Car.query.filter(Car.price.isnot(None)).order_by(desc(Car.price)).all()
            else:
                response = ResponseObject.ResponseObject(obj=[Car()], status='wrong input!')
                return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=[Car()], status='wrong field!')
            return jsonify(response.serialize())
        if cars is None:
            response = ResponseObject.ResponseObject(obj=[Car()], status='no cars in the database!')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=cars, status='OK')
        return jsonify(response.serialize())
