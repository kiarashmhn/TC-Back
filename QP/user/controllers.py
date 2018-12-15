import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from QP import db, app, auth_manager
from QP.user.models import User
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
        token = auth_manager.generate_token(u.id)
        return jsonify(obj=token, status='OK'), 200

    @staticmethod
    @usr.route('/logout', methods=["GET"])
    @auth_manager.authenticate
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
        auth_manager.expire_token()
        response = ResponseObject.ResponseObject(obj=User(), status='OK')
        return jsonify(response.serialize())

    @staticmethod
    @usr.route('', methods=["GET"])
    @auth_manager.authenticate
    def list_users():
        """
        This is the ListUsers API
        Call this api to get the list of users.
        ---
        tags:
            - ListUsers API
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
                            username:
                                default: ali
                                type: string
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

            200,status="OK":
                description: Successfully returned the list of users.
            200,status="there are no users in the database!":
                description: No cars!
            200,status="this url is not accessible for you!":
                description: You are not an admin!
            401:
                description: You haven't logged in!
        """
        if 'role' not in session:
            response = ResponseObject.ResponseObject(obj=[User()], status='this url is not accessible for you!')
            return jsonify(response.serialize())
        if session['role'] == "super_admin" or session['role'] == "admin":
            users = User.query.all()
            if users is None:
                response = ResponseObject.ResponseObject(obj=[User()], status='there are no users in the database!')
                return jsonify(response.serialize())
            response = ResponseObject.ResponseObject(obj=users, status='OK')
            return jsonify(response.serialize())
        response = ResponseObject.ResponseObject(obj=[User()], status='this url is not accessible for you!')
        return jsonify(response.serialize())

    @staticmethod
    @usr.route('/<int:user_id>', methods=["DELETE"])
    @auth_manager.authenticate
    def delete_user(user_id):
        """
        This is the DeleteUser API
        Call this api passing a user_id in the path to delete it.
        ---
        tags:
            - DeleteUser API
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
              description: id of the user you want to delete
        responses:
            200:
                description: All responses have 200 status code; check the status field.
            200,status="OK":
                description: User successfully deleted.
            200,status="user_id cannot be empty!":
                description: User wasn't deleted because of the message in status.
            200,status="invalid user_id!":
                description: User wasn't deleted because of the message in status.
            200,status="this url is not accessible for you!":
                description: User wasn't deleted because you are not an admin.
            200,status="you can not delete this user!":
                description: The user you're trying to remove is an admin!
            401:
                description: You aren't logged in
        """
        if 'role' not in session:
            response = ResponseObject.ResponseObject(obj=User(), status='this url is not accessible for you!')
            return jsonify(response.serialize())
        if session['role'] == "admin" or session['role'] == "super_admin":
            if user_id is None:
                response = ResponseObject.ResponseObject(obj=User(), status='user_id cannot be empty!')
                return jsonify(response.serialize())
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                response = ResponseObject.ResponseObject(obj=User(), status='invalid user_id!')
                return jsonify(response.serialize())
            if user.role == "user" or session['role'] == "super_admin":
                for car in user.cars:
                    db.session.delete(car)
                db.session.delete(user)
                db.session.commit()
                response = ResponseObject.ResponseObject(obj=User(), status='OK')
                return jsonify(response.serialize())
            else:
                response = ResponseObject.ResponseObject(obj=User(), status='you can not delete this user!')
                return jsonify(response.serialize())
        else:
            response = ResponseObject.ResponseObject(obj=User(), status='this url is not accessible for you!')
            return jsonify(response.serialize())
