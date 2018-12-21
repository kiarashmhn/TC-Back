import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app, auth_manager
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

    @staticmethod
    @rnt.route('', methods=["POST"])
    @auth_manager.authenticate
    def rent_car(user):
        req = request.get_json()
        car = Car.query.filter_by(id=req.get("car_id")).first()
        if not car:
            out = {'status': 'car not found!'}
            return jsonify(out), 400
        owner = car.user_id
        try:
            car.is_rented = True
            db.session.commit()
            rent = Rent(user_id=user.id,
                        owner_id=owner,
                        car_id=car.id,
                        cost=req.get("cost"),
                        kilometer=req.get("kilometer"),
                        start=req.get("start"),
                        end=req.get("end"),
                        source=req.get("source"),
                        destination=req.get("destination"))
            db.session.add(rent)
            db.session.commit()
            out = {'object': rent.serialize()}
            return jsonify(out), 200

        except:
            out = {'status': 'Bad Request'}
            return jsonify(out), 400

    @staticmethod
    @rnt.route('/<int:id>', methods=["DELETE"])
    @auth_manager.authenticate
    def delete_rent(user, id):
        r = Rent.query.filter_by(id=id).first()
        if user.role == "user":
            out = {'status': 'Access Denied!'}
            return jsonify(out), 400
        if r is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        car_id = r.car_id
        db.session.delete(r)
        db.session.commit()
        car = Car.query.filter_by(id=car_id).first()
        car.is_rented = False
        db.session.commit()
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @rnt.route('/<int:id>', methods=["PUT"])
    @auth_manager.authenticate
    def update_rent(user, id):
        req = request.get_json()
        r = Rent.query.filter_by(id=id).first()
        if user.role == "user":
            out = {'status': 'Access Denied!'}
            return jsonify(out), 400
        if r is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        r.source = req.get("source")
        r.destination = req.get("destination")
        r.start = req.get("start")
        r.end = req.get("end")
        r.cost = req.get("cost")
        r.kilometer = req.get("kilometer")
        db.session.commit()
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @rnt.route('/owner', methods=["GET"])
    @auth_manager.authenticate
    def get_by_owner(user):
        r = Rent.query.filter_by(owner_id=user.id).all()
        if r is None:
            out = {'status': 'Not Found!'}
            return jsonify(out), 404
        rents = []
        for rent in r:
            rents.append(rent.serialize())
        out = {'object': rents}
        return jsonify(out), 200
