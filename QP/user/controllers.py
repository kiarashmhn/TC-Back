import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user
from QP import db, app
from QP.user.models import User
from flask_login import login_required, login_user, logout_user, current_user
from QP import ResponseObject
from flask import Blueprint

usr = Blueprint('usr', __name__)


class UserController():
    def __init__(self):
        pass

    @staticmethod
    @usr.route('/signup', methods=["POST"])
    def signup():
        """
            This is the Signup API
            Call this api passing username,email,password,identificationId in request body and signup a new user
            ---
            tags:
              - SignUp API
            consumes:
              - application/json
            parameters:
              - in: body
                name: user
                description: The User to create.
                schema:
                  type: object
                  required:
                    - username
                    - password
                    - email
                    - identificationId
                  properties:
                    username:
                        default: ali
                        type: string
                    password:
                        type: string
                        default: 123456789
                    email:
                        type: string
                        default: ali@gmail.com
                    identificationId:
                        type: string
                        default: 0020738528
            responses:
              200:
                    description: All responses have 200 status code; check the status field.
                    schema:
                        type: object
                        properties:
                            object:
                                type: object
                                properties:
                                    username:
                                        default: ali
                                        type: string
                                    password:
                                        type: string
                                        default: 123456789
                                    email:
                                        type: string
                                        default: ali@gmail.com
                                    identificationId:
                                        type: string
                                        default: 0020738528
                                    address:
                                        type: string
                                        default: tehran
                                    age:
                                        type: integer
                                        default: 27
                                    gender:
                                        type: string
                                        default: male
                                    id:
                                        type: integer
                                        default: 2
                                    lastName:
                                        type: string
                                        default: erf
                                    mobile_num:
                                        type: string
                                        default: 09102998841
                                    phone_num:
                                        type: string
                                        default: 02188461197
                                    name:
                                        type: string
                                        default: ali
                                    postalCode:
                                        type: integer
                                        default: 1565935871
                                    role:
                                        type: string
                                        default: user
                            status:
                                type: string
                                default: OK

              200,status="OK":
                    description: User successfully created; And is returned in response.
              200,status="username field cannot be empty!":
                    description: User wasn't created because of the message in status.
              200,status="user with this username already exists!":
                    description: User wasn't created because of the message in status.
              200,status="identificationId field cannot be empty!":
                    description: User wasn't created because of the message in status.
              200,status="user with this id already exists!":
                    description: User wasn't created because of the message in status.
              200,status="email field cannot be empty!":
                    description: User wasn't created because of the message in status.
              200,status="user with this email already exists!":
                    description: User wasn't created because of the message in status.
              200,status="password field cannot be empty!":
                    description: User wasn't created because of the message in status.
        """
        error = None
        req = request.get_json()
        if req is None:
            response = ResponseObject.ResponseObject(obj=User(), status='request body can not be empty!')
            return jsonify(response.serialize())
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
            if 'role' in session:
                if session['role'] == "super_admin":
                    user.role = req.get("role")
            db.session.add(user)
            db.session.commit()
            print("signed in")
            response = ResponseObject.ResponseObject(obj=user, status='OK')
            return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=User(), status=error)
            return jsonify(response.serialize())

    @staticmethod
    @usr.route('/login', methods=["POST"])
    def login():
        """
        This is the Login API
        Call this api passing username,password in request body to login.
        ---
        tags:
          - Login API
        consumes:
          - application/json
        parameters:
          - in: body
            name: user
            description: The username and password fields of the user.
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  default: ali
                  type: string
                password:
                  type: string
                  default: 123456789
        responses:
          200:
            description: All responses have 200 status code; check the status field.
            schema:
                type: object
                properties:
                    object:
                        type: object
                        properties:
                            username:
                                default: ali
                                type: string
                            password:
                                type: string
                                default: 123456789
                            email:
                                type: string
                                default: ali@gmail.com
                            identificationId:
                                type: string
                                default: 0020738528
                            address:
                                type: string
                                default: tehran
                            age:
                                type: integer
                                default: 27
                            gender:
                                type: string
                                default: male
                            id:
                                type: integer
                                default: 2
                            lastName:
                                type: string
                                default: erf
                            mobile_num:
                                type: string
                                default: 09102998841
                            phone_num:
                                type: string
                                default: 02188461197
                            name:
                                type: string
                                default: ali
                            postalCode:
                                type: integer
                                default: 1565935871
                            role:
                                type: string
                                default: user
                    status:
                        type: string
                        default: OK
          200,status="OK":
            description: User successfully logged in; And is returned in response.

          200,status="username and password fields cannot be empty!":
            description: User wasn't logged in because of the message in status.
          200,status="invalid credentials!":
            description: User wasn't logged in because of the message in status.
                """
        req = request.get_json()
        if req is None:
            response = ResponseObject.ResponseObject(obj=User(), status='request body can not be empty!')
            return jsonify(response.serialize())
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
    @usr.route('/logout', methods=["GET"])
    def logout():
        """
        This is the LogOut API
        Call this api to logout.
        ---
        tags:
          - LogOut API
        consumes:
          - application/json
        responses:
          200:
            description: All responses have 200 status code; check the status field.
            schema:
            type: object
            properties:
                object:
                    type: none
                status:
                    type: string
                    default: OK
          200,status="OK":
            description: User successfully created; And is returned in response.
          401:
            description: You aren't logged in
        """
        logout_user()
        session.pop('user_id', None)
        session.pop('role', None)
        response = ResponseObject.ResponseObject(obj=User(), status='OK')
        return jsonify(response.serialize())
