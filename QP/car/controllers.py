import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app, auth_manager
from QP.user.models import User
from QP.car.models import Car
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint

car = Blueprint('car', __name__)


class CarHandler():
    def __init__(self):
        pass

    def add(self, req):
        carr = Car(name=req.get("name"),
                   factory=req.get("factory"),
                   kilometer=req.get("kilometer"),
                   year=req.get("year"),
                   color=req.get("color"),
                   description=req.get("description"),
                   automate=req.get("automate"),
                   price=req.get("price"),
                   user_id=req.get("user_id"),
                   is_rented=False)
        db.session.add(carr)
        db.session.commit()
        return carr

    def delete(self, car_id):
        carr = Car.query.filter_by(id=car_id).first()
        db.session.delete(carr)
        db.session.commit()

    def get(self, car_id):
        return Car.query.filter_by(id=car_id).first()

    def get_all(self):
        return Car.query.filter_by(is_rented=False).all()
    #def update(self):


class CarApiHandler():
    car_handler = CarHandler()

    def __init__(self):
        pass

    @staticmethod
    @car.route('', methods=["POST"])
    @auth_manager.authenticate
    def add_car(user):
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
                    example: 2000000
                user_id:
                    type: integer
                    example: 1
        responses:
            200:
              description: OK.
              schema:
                type: object
                properties:
                  object:
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
                            example: 2000000
                        user_id:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 1
            400,status="user_id field cannot be empty!":
              description: Car wasn't added because of the message in status.
            400,status="invalid user_id!":
              description: Car wasn't added because of the message in status.
            401:
              description: You aren't logged in
        """
        car_handler = CarApiHandler.car_handler
        req = request.get_json()
        if user.role == "admin" or user.role == "super_admin":
            if req.get("user_id") is None:
                out = {'status': 'user_id field cannot be empty!'}
                return jsonify(out), 400
            elif User.query.filter_by(id=req.get("user_id")).first() is None:
                out = {'status': 'invalid user_id!'}
                return jsonify(out), 400
        else:
            req["user_id"] = user.id
        try:
            carr = car_handler.add(req)
            print("car added")
            out = {'object': carr.serialize()}
            return jsonify(out), 200
        except:
            out = {'status': 'Bad Request'}
            return jsonify(out), 400

    @staticmethod
    @car.route('/<int:car_id>', methods=["DELETE"])
    @auth_manager.authenticate
    def delete_car(user, car_id):
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
            description: OK.
            schema:
                type: object
                properties:
                  status:
                    type: string
                    example: OK
          400,status="car_id cannot be empty!":
            description: Car_id cannot be empty.
          400,status="invalid car_id!":
            description: Car wasn't found.
          400,status="you can not delete this car!":
            description: You can not delete this car because this car isn't yours or it is rented.
          401:
            description: You aren't logged in
        """
        car_handler = CarApiHandler.car_handler
        if car_id is None:
            out = {'status': 'car_id cannot be empty!'}
            return jsonify(out), 400
        carr = car_handler.get(car_id)
        if carr is None:
            out = {'status': 'invalid car_id!'}
            return jsonify(out), 400
        if (user.role == "user") and (carr not in user.cars or carr.is_rented):
            out = {'status': 'you can not delete this car!'}
            return jsonify(out), 400
        car_handler.delete(car_id)
        out = {'status': 'OK'}
        return jsonify(out), 200

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
            description: OK.
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
                            example: 2000000
                        user_id:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 1
          400,status="there are no cars in the database!":
            description: No cars!
        """
        cars = CarApiHandler.car_handler.get_all()
        if cars is None:
            out = {'status': 'there are no cars in the database!'}
            return jsonify(out), 400
        c = []
        for car in cars:
            c.append(car.serialize())
        out = {'object': c}
        return jsonify(out), 200

    @staticmethod
    @car.route('/<int:car_id>', methods=["PUT"])
    @auth_manager.authenticate
    def update_car(user, car_id):
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
            description: OK.
            schema:
                type: object
                properties:
                  status:
                    type: string
                    example: OK
          400,status="Car not found!":
            description: Car not found!
          400,status="you can not update this car!":
            description: You can't update this car because it is'nt yours or it's rented.
          401:
            description: You aren't logged in
        """
        req = request.get_json()
        carr = Car.query.filter_by(id=car_id).first()
        if carr is None:
            out = {'status': 'car not found!'}
            return jsonify(out), 400
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
        if (user.role == "user") and (carr not in user.cars or carr.is_rented):
            out = {'status': 'you can not update this car!'}
            return jsonify(out), 400
        db.session.commit()
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @car.route('/<int:car_id>', methods=["GET"])
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
            description: OK.
            schema:
                type: object
                properties:
                  object:
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
                            example: 10000
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
                            example: 2000000
                        user_id:
                            type: integer
                            example: 1
                        id:
                            type: integer
                            example: 1
          400,status="Car not found!":
            description: Car wasn't returned because of the message in status.
          401:
            description: You aren't logged in
        """

        carr = Car.query.filter_by(id=car_id).first()
        if carr is None:
            out = {'status': 'car not found!'}
            return jsonify(out), 400
        out = {'object': carr.serialize()}
        return jsonify(out), 200

    @staticmethod
    @car.route('/user', methods=["GET"])
    @auth_manager.authenticate
    def get_user_cars(user):
        """
                This is the GetUser'sCars API
                Call this api to get the list of your cars.
                ---
                tags:
                  - GetUser'sCars API
                responses:
                    200:
                        description: OK.
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
                                                example: 1000
                                                type: integer
                                            year:
                                                example: 2018
                                                type: integer
                                            color:
                                                example: white
                                                type: string
                                            description:
                                                type: string
                                                example: bmw-i8
                                            automate:
                                                type: integer
                                                example: 1
                                            price:
                                                type: integer
                                                example: 2000000
                                            user_id:
                                                type: integer
                                                example: 1
                                            id:
                                                type: integer
                                                example: 1
                    400,status="Invalid user_id!":
                        description: Invalid user_id!
                    401:
                        description: You are not logged in!
        """
        c = []
        for car in user.cars:
            c.append(car.serialize())
        out = {'object': c}
        return jsonify(out), 200
