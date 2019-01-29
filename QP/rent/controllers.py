import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app, auth_manager
from QP.car.controllers import CarHandler
from QP.rent.models import Rent
from QP.user.models import User
from QP.car.models import Car
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint

rnt = Blueprint('rnt', __name__)


class RentHandler():
    def __init__(self):
        pass

    def add(self, req):
        rent = Rent(user_id=req.get("user_id"),
                    owner_id=req.get("owner"),
                    car_id=req.get("car_id"),
                    cost=req.get("cost"),
                    kilometer=req.get("kilometer"),
                    start=req.get("start"),
                    end=req.get("end"),
                    source=req.get("source"),
                    destination=req.get("destination"))
        db.session.add(rent)
        db.session.commit()
        return rent

    def delete(self, rent_id):
        r = Rent.query.filter_by(id=rent_id).first()
        db.session.delete(r)
        db.session.commit()

    def get(self, rent_id):
        r = Rent.query.filter_by(id=rent_id).first()
        return r

    def update(self, rent_id, req):
        r = Rent.query.filter_by(id=rent_id).first()
        r.source = req.get("source")
        r.destination = req.get("destination")
        r.start = req.get("start")
        r.end = req.get("end")
        r.cost = req.get("cost")
        r.kilometer = req.get("kilometer")
        db.session.commit()

    def get_all(self):
        r = Rent.query.all()
        return r


class RentApiHandler():
    rent_handler = RentHandler()
    car_handler = CarHandler()

    def __init__(self):
        pass

    @staticmethod
    @rnt.route('', methods=["POST"])
    @auth_manager.authenticate
    def rent_car(user):
        """
            This is the RentCar API
            Call this api passing a rent model in request body to add it.
            ---
            tags:
                - RentCar API
            consumes:
                - application/json
            parameters:
                - in: body
                  name: rent
                  description: The rent model to add to database.
                  schema:
                    type: object
                    required:
                        - car_id
                    properties:
                        car_id:
                            example: 1
                            type: integer
                        kilometer:
                            type: integer
                            example: 1000
                        start:
                            type: string
                            example: 21 Jan 2018, 7:30:12 PM
                        end:
                            type: string
                            example: 25 Jan 2018, 12:35:07 PM
                        cost:
                            type: integer
                            example: 2000000
                        source:
                            type: integer
                            example: 1
                        destination:
                            type: integer
                            example: 2
            responses:
                200:
                    description: OK.
                    schema:
                    type: object
                    properties:
                        object:
                          type: object
                          properties:
                            car_id:
                                example: 1
                                type: integer
                            user_id:
                                type: integer
                                example: 1
                            owner_id:
                                type: integer
                                example: 1
                            kilometer:
                                type: integer
                                example: 1000
                            start:
                                type: string
                                example: 21 Jan 2018, 7:30:12 PM
                            end:
                                type: string
                                example: 25 Jan 2018, 12:35:07 PM
                            cost:
                                type: integer
                                example: 2000000
                            source:
                                type: integer
                                example: 1
                            destination:
                                type: integer
                                example: 2
                            id:
                                type: integer
                                example: 1
                400,status="Bad request":
                    description: rent wasn't added.
                400,status="car not found":
                    description: Car not found!
                401:
                    description: You aren't logged in
                """
        try:
            req = request.get_json()
            car = RentApiHandler.car_handler.get(req.get("car_id"))
            if not car:
                out = {'status': 'car not found!'}
                return jsonify(out), 400
            req["owner"] = car.user_id
            req["user_id"] = user.id
            car.is_rented = True
            db.session.commit()
            rent = RentApiHandler.rent_handler.add(req)
            out = {'object': rent.serialize()}
            return jsonify(out), 200
        except:
            out = {'status': 'Bad Request'}
            return jsonify(out), 400

    @staticmethod
    @rnt.route('/<int:id>', methods=["DELETE"])
    @auth_manager.authenticate
    def delete_rent(user, id):
        """
            This is the DeleteRent API
            Call this api passing a rent_id to delete it.
            ---
            tags:
                - DeleteRentAPI
            consumes:
                - application/json
            parameters:
                - name: rent_id
                  in: path
                  type: integer
                  required: true
                  description: id of the rent you want to delete
            responses:
                200:
                    description: OK.
                    schema:
                    type: object
                    properties:
                        status:
                            type: string
                            example: OK
                400:
                    description: Access Denied!
                404:
                    description: Rent not found!
                401:
                    description: You aren't logged in
        """
        if user.role == "user":
            out = {'status': 'Access Denied!'}
            return jsonify(out), 400
        r = RentApiHandler.rent_handler.get(id)
        if r is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        car_id = r.car_id
        RentApiHandler.rent_handler.delete(id)
        car = RentApiHandler.car_handler.get(car_id)
        car.is_rented = False
        db.session.commit()
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @rnt.route('/<int:id>', methods=["PUT"])
    @auth_manager.authenticate
    def update_rent(user, id):
        """
                This is the UpdateRent API
                Call this api passing a rent model in request body to update it.
                ---
                tags:
                    - UpdateRentAPI
                consumes:
                    - application/json
                parameters:
                    - name: rent_id
                      in: path
                      type: integer
                      required: true
                      description: id of the rent you want to update
                    - in: body
                      name: rent
                      description: The rent model to update.
                      schema:
                        type: object
                        required:
                            - car_id
                        properties:
                            kilometer:
                                type: integer
                                example: 1000
                            start:
                                type: string
                                example: 21 Jan 2018, 7:30:12 PM
                            end:
                                type: string
                                example: 25 Jan 2018, 12:35:07 PM
                            cost:
                                type: integer
                                example: 2000000
                            source:
                                type: integer
                                example: 1
                            destination:
                                    type: integer
                                    example: 2
                responses:
                        200:
                            description: OK.
                            schema:
                            type: object
                            properties:
                                status:
                                  type: string
                                  example: OK
                        400,status="Bad request":
                            description: rent wasn't updated.
                        400,status="car not found":
                            description: Car not found!
                        401:
                            description: You aren't logged in
        """
        req = request.get_json()
        if user.role == "user":
            out = {'status': 'Access Denied!'}
            return jsonify(out), 400
        r = RentApiHandler.rent_handler.get(id)
        if r is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        RentApiHandler.rent_handler.update(id, req)
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @rnt.route('/owner', methods=["GET"])
    @auth_manager.authenticate
    def get_by_owner(user):
        """
        This is the GetRentsByOwner API
        Call this api to get your rents.
        ---
        tags:
            - GetRentsByOwnerAPI
        consumes:
            - application/json
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
                                car_id:
                                    example: 1
                                    type: integer
                                user_id:
                                    type: integer
                                    example: 1
                                owner_id:
                                    type: integer
                                    example: 1
                                kilometer:
                                    type: integer
                                    example: 1000
                                start:
                                    type: string
                                    example: 21 Jan 2018, 7:30:12 PM
                                end:
                                    type: string
                                    example: 25 Jan 2018, 12:35:07 PM
                                cost:
                                    type: integer
                                    example: 2000000
                                source:
                                    type: integer
                                    example: 1
                                destination:
                                    type: integer
                                    example: 2
                                id:
                                    type: integer
                                    example: 1

            404:
                description: no Rents found!
            401:
                description: You aren't logged in
                """
        r = RentApiHandler.rent_handler.get_all()
        r1 = []
        for rent in r:
            if rent.owner_id == user.id:
                r1.append(rent.serialize())
        if r1 is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        out = {'object': r1}
        return jsonify(out), 200

    @staticmethod
    @rnt.route('/user', methods=["GET"])
    @auth_manager.authenticate
    def get_by_user(user):
        """
        This is the GetRentByUser API
        Call this api to get your rent.
        ---
        tags:
            - GetRentByUserAPI
        consumes:
            - application/json
        responses:
            200:
                description: OK.
                schema:
                type: object
                properties:
                    object:
                        type: object
                        properties:
                                car_id:
                                    example: 1
                                    type: integer
                                user_id:
                                    type: integer
                                    example: 1
                                owner_id:
                                    type: integer
                                    example: 1
                                kilometer:
                                    type: integer
                                    example: 1000
                                start:
                                    type: string
                                    example: 21 Jan 2018, 7:30:12 PM
                                end:
                                    type: string
                                    example: 25 Jan 2018, 12:35:07 PM
                                cost:
                                    type: integer
                                    example: 2000000
                                source:
                                    type: integer
                                    example: 1
                                destination:
                                    type: integer
                                    example: 2
                                id:
                                    type: integer
                                    example: 1

            404:
                description: no Rents found!
            401:
                description: You aren't logged in
        """
        r = RentApiHandler.rent_handler.get_all()
        r1 = None
        for rent in r:
            if rent.user_id == user.id:
                r1 = rent.serialize()
                out = {'object': r1}
                return jsonify(out), 200
        out = {'status': 'Not Found!'}
        return jsonify(out), 404


    @staticmethod
    @rnt.route('locations', methods=["GET"])
    def get_locations():
        return jsonify({'object': ["TehranPars", "Sepah Sq.", "Hafte-Tir Sq.",  "Imam Khomeini Airport",
                        "Mehrabad Airport", "Valiasr Sq."]}), 200
