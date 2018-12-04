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

car = Blueprint('car', __name__)


class CarHandler():
    def __init__(self):
        pass

    @staticmethod
    @car.route('', methods=["POST"])
    @login_required
    def add_car():
        """
        This is the AddCar API
        Call this api passing a car in request body to add it.
        ---
        tags:
          - AddCar API
        consumes:
          - application/json
        parameters:
          - in: body
            name: car
            description: The car to add to database.
            schema:
              type: object
              required:
                - user_id
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
        responses:
            200:
              description: All responses have 200 status code; check the status field.
              schema:
                type: object
                properties:
                  object:
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
              description: Car successfully added; And is returned in response.
            200,status="user_id field cannot be empty!":
              description: Car wasn't added because of the message in status.
            200,status="invalid user_id!":
              description: Car wasn't added because of the message in status.
            401:
              description: You aren't logged in
        """
        req = request.get_json()
        if req is None:
            response = ResponseObject.ResponseObject(obj=Car(), status='request body can not be empty!')
            return jsonify(response.serialize())
        if session['role'] == "admin" or session['role'] == "super_admin":
            if req.get("user_id") is None:
                error = 'user_id field cannot be empty!'
                response = ResponseObject.ResponseObject(obj=Car(), status=error)
                return jsonify(response.serialize())
            elif User.query.filter_by(id=req.get("user_id")).first() is None:
                error = 'invalid user_id!'
                response = ResponseObject.ResponseObject(obj=Car(), status=error)
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
                response = ResponseObject.ResponseObject(obj=carr, status='OK')
                return jsonify(response.serialize())
        elif session['role'] == "user":
            if User.query.filter_by(id=session['user_id']).first() is None:
                error = 'invalid user_id in session!'
                response = ResponseObject.ResponseObject(obj=Car(), status=error)
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
                           user_id=session['user_id'])
                db.session.add(carr)
                db.session.commit()
                print("car added")
                response = ResponseObject.ResponseObject(obj=carr, status='OK')
                return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=Car(), status='this url is not accessible for you!')
            return jsonify(response.serialize())

    @staticmethod
    @car.route('/<int:car_id>', methods=["DELETE"])
    @login_required
    def delete_car(car_id):
        """
        This is the DeleteCar API
        Call this api passing a car_id in the path to delete it.
        ---
        tags:
          - DeleteCar API
        parameters:
          - name: car_id
            in: path
            type: integer
            required: true
            description: id of the car you want to delete
        responses:
          200:
            description: All responses have 200 status code; check the status field.
            schema:
                type: object
                properties:
                  object:
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
            description: Car successfully deleted.
          200,status="car_id cannot be empty!":
            description: Car wasn't deleted because of the message in status.
          200,status="invalid car_id!":
            description: Car wasn't deleted because of the message in status.
          200,status="this url is not accessible for you!":
            description: Car wasn't deleted because you are not an admin.
          401:
            description: You aren't logged in
        """
        if car_id is None:
            response = ResponseObject.ResponseObject(obj=Car(), status='car_id cannot be empty!')
            return jsonify(response.serialize())
        carr = Car.query.filter_by(id=car_id).first()
        if carr is None:
            response = ResponseObject.ResponseObject(obj=Car(), status='invalid car_id!')
            return jsonify(response.serialize())
        if session['role'] == "user" and carr not in current_user.cars:
            response = ResponseObject.ResponseObject(obj=Car(), status='you can not delete this car!')
            return jsonify(response.serialize())
        db.session.delete(carr)
        db.session.commit()
        response = ResponseObject.ResponseObject(obj=Car(), status='OK')
        return jsonify(response.serialize())

    @staticmethod
    @car.route('', methods=["GET"])
    def list_car():
        """
        This is the ListCar API
        Call this api to get the list of cars.
        ---
        tags:
          - ListCar API
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
            description: Successfully returned the list of cars.
          200,status="there are no cars in the database!":
            description: No cars!
        """
        cars = Car.query.all()
        if cars is None:
            response = ResponseObject.ResponseObject(obj=Car(), status='there are no cars in the database!')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=cars, status='OK')
        return jsonify(response.serialize())

    @staticmethod
    @car.route('/<int:car_id>', methods=["PUT"])
    @login_required
    def update_car(car_id):
        """
        This is the UpdateCar API
        Call this api passing a car_id in the path to update it.
        ---
        tags:
          - UpdateCar API
        parameters:
          - name: car_id
            in: path
            type: integer
            required: true
            description: id of the car you want to update
        responses:
          200:
            description: All responses have 200 status code; check the status field.
            schema:
                type: object
                properties:
                  object:
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
            description: Car successfully updated.
          200,status="Car not found!":
            description: Car wasn't updated because of the message in status.
          200,status="this url is not accessible for you!":
            description: Car wasn't updated because you are not an admin.
          401:
            description: You aren't logged in
        """
        req = request.get_json()
        if session['role'] == "admin" or session['role'] == "super_admin":
            carr = Car.query.filter_by(id=car_id).first()
            if carr is None:
                response = ResponseObject.ResponseObject(obj=Car(), status='car not found!')
                return jsonify(response.serialize())
            if req.get("factory") is not None:
                carr.factory = req.get("factory")
            if req.get("kilometer") is not None:
                carr.kilometer = req.get("kilometer")
            if req.get("year") is not None:
                carr.year = req.get("year")
            if req.get("color") is not None:
                carr.color = req.get("color")
            if req.get("automate") is not None:
                carr.automate = req.get("automate")
            if req.get("description") is not None:
                carr.description = req.get("description")
            if req.get("price") is not None:
                carr.price = req.get("price")
            db.session.commit()
            response = ResponseObject.ResponseObject(obj=Car(), status='OK')
            return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=Car(), status='this url is not accessible for you!')
            return jsonify(response.serialize())

    @staticmethod
    @car.route('/<int:car_id>', methods=["GET"])
    @login_required
    def get_car(car_id):
        """
        This is the GetCar API
        Call this api passing a car_id in the path to get it.
        ---
        tags:
          - GetCar API
        parameters:
          - name: car_id
            in: path
            type: integer
            required: true
            description: id of the car you want to get
        responses:
          200:
            description: All responses have 200 status code; check the status field.
            schema:
                type: object
                properties:
                  object:
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
            description: Car successfully returned.
          200,status="Car not found!":
            description: Car wasn't returned because of the message in status.
          401:
            description: You aren't logged in
        """

        carr = Car.query.filter_by(id=car_id).first()
        if carr is None:
            response = ResponseObject.ResponseObject(obj=Car(), status='car not found!')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=carr, status='OK')
        return jsonify(response.serialize())

    @staticmethod
    @car.route('/user', methods=["GET"])
    def get_user_cars():
        """
                This is the GetUser'sCars API
                Call this api to get the list of your cars.
                ---
                tags:
                  - GetUser'sCars API
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
                    200,status="Invalid user_id!":
                        description: Invalid user_id!
                    401:
                        description: You are not logged in!
        """
        if 'role' not in session or 'user_id' not in session:
            response = ResponseObject.ResponseObject(obj=[Car()], status='this url is not accessible for you!')
            return jsonify(response.serialize())
        u = User.query.filter_by(id=session['user_id']).first()
        if u is None:
            response = ResponseObject.ResponseObject(obj=[Car()], status='invalid user_id!')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=u.cars, status='OK')
        return jsonify(response.serialize())
