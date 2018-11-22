import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app
from QP.auth.models import User
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint

auth = Blueprint('auth', __name__)


class UserController():
    def __init__(self):
        pass

    @staticmethod
    @auth.route('/signup', methods=["POST"])
    def signup():
        error = None
        req = request.get_json()
        if req.get("username") is None:
            error = 'username field cannot be empty!'
        else:
            x = User.query.filter_by(username=req.get("username")).first()
            if x is not None:
                error = 'user with this username already exists!'
        if req.get("identificationId") is None:
            error = 'identificationId field cannot be empty!'
        else:
            x = User.query.filter_by(id=req.get("identificationId")).first()
            if x is not None:
                error = 'user with this id already exists!'
        if req.get("email") is None:
            error = 'email field cannot be empty!'
        else:
            x = User.query.filter_by(email=req.get("email")).first()
            if x is not None:
                error = 'user with this email already exists!'
        if req.get("password") is None:
            error = 'password field cannot be empty!'
        if error is None:
            user = User(name=req.get("name"),
                        username=req.get("username"),
                        password=req.get("password"),
                        lastName=req.get("lastName"),
                        age=req.get("age"),
                        identificationId=req.get("identificationId"),
                        address=req.get("address"),
                        gender=req.get("gender"),
                        postalCode=req.get("postalCode"),
                        mobile_num=req.get("mobile_num"),
                        phone_num=req.get("phone_num"),
                        email=req.get("email"),
                        role="user")
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['user_id'] = user.id
            session['role'] = "user"
            print("signed in")
            response = ResponseObject.ResponseObject(obj=user, status='OK')
            return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=User(), status=error)
            return jsonify(response.serialize())

    @staticmethod
    @auth.route('/login', methods=["POST"])
    def login():
        req = request.get_json()
        username = req.get("username")
        password = req.get("password")
        error = None
        if username is None or password is None:
            error = 'username and password fields cannot be empty!'
            response = ResponseObject.ResponseObject(obj=User(), status=error)
            return jsonify(response.serialize())
        u = User.get_by_username(username=username)
        if u is None or not u.check_password(password):
            error = 'invalid credentials!'
            response = ResponseObject.ResponseObject(obj=User(), status=error)
            return jsonify(response.serialize())
        login_user(u)
        session['user_id'] = u.id
        session['role'] = u.role
        response = ResponseObject.ResponseObject(obj=u, status='OK')
        return jsonify(response.serialize())

    @staticmethod
    @login_required
    @auth.route('/logout', methods=["GET"])
    def logout():
        logout_user()
        session.pop('user_id', None)
        session.pop('role', None)
        response = ResponseObject.ResponseObject(obj=User(), status='OK')
        return jsonify(response.serialize())

