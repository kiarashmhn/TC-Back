import os
from datetime import datetime
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from QP import db, app, auth_manager
from QP.user.models import User
from QP import ResponseObject
from flask import Blueprint

usr = Blueprint('usr', __name__)


class UserHandler():
    def __init__(self):
        pass

    def add(self, req):
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
                    role=req.get("role"))
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_name(self, name):
        u = User.get_by_username(username=name)
        return u


class UserApiHandler():
    user_handler = UserHandler()

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
                        example: ali
                        type: string
                    password:
                        type: string
                        example: 123456789
                    email:
                        type: string
                        example: ali@gmail.com
                    identificationId:
                        type: string
                        example: 0020738528
            responses:
              200:
                    description: User successfully created!
                    schema:
                        type: object
                        properties:
                            object:
                                type: object
                                properties:
                                    username:
                                        example: ali
                                        type: string
                                    password:
                                        type: string
                                        example: 123456789
                                    email:
                                        type: string
                                        example: ali@gmail.com
                                    identificationId:
                                        type: string
                                        example: 0020738528
                                    address:
                                        type: string
                                        example: tehran
                                    age:
                                        type: integer
                                        example: 27
                                    gender:
                                        type: string
                                        example: male
                                    id:
                                        type: integer
                                        example: 2
                                    lastName:
                                        type: string
                                        example: erf
                                    mobile_num:
                                        type: string
                                        example: 09102998841
                                    phone_num:
                                        type: string
                                        example: 02188461197
                                    name:
                                        type: string
                                        example: ali
                                    postalCode:
                                        type: integer
                                        example: 1565935871
                                    role:
                                        type: string
                                        example: user

              400,status="username field cannot be empty!":
                    description: User wasn't created because of the message in status.
              400,status="user with this username already exists!":
                    description: User wasn't created because of the message in status.
              400,status="identificationId field cannot be empty!":
                    description: User wasn't created because of the message in status.
              400,status="user with this id already exists!":
                    description: User wasn't created because of the message in status.
              400,status="email field cannot be empty!":
                    description: User wasn't created because of the message in status.
              400,status="user with this email already exists!":
                    description: User wasn't created because of the message in status.
              400,status="password field cannot be empty!":
                    description: User wasn't created because of the message in status.
        """
        error = None
        req = request.get_json()
        user_handler = UserApiHandler.user_handler
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
            try:
                req["role"] = "user"
                user = user_handler.add(req)
                print("signed in")
                out = {'object': user.serialize()}
                return jsonify(out), 200
            except:
                out = {'status': 'Bad Request!'}
                return jsonify(out), 400
        else:
            out = {'status': error}
            return jsonify(out), 400

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
                  example: ali
                  type: string
                password:
                  type: string
                  example: 123456789
        responses:
          200:
            description: OK
            schema:
                type: object
                properties:
                    object:
                        type: object
                        properties:
                            username:
                                example: ali
                                type: string
                            password:
                                type: string
                                example: 123456789
                            email:
                                type: string
                                example: ali@gmail.com
                            identificationId:
                                type: string
                                example: 0020738528
                            address:
                                type: string
                                example: tehran
                            age:
                                type: integer
                                example: 27
                            gender:
                                type: string
                                example: male
                            id:
                                type: integer
                                example: 2
                            lastName:
                                type: string
                                example: erf
                            mobile_num:
                                type: string
                                example: 09102998841
                            phone_num:
                                type: string
                                example: 02188461197
                            name:
                                type: string
                                example: ali
                            postalCode:
                                type: integer
                                example: 1565935871
                            role:
                                type: string
                                example: user
                    token:
                        type: string
                        example: ea0632d8-d254-4773-93df-e9f19e589ce
          400,status="username and password fields cannot be empty!":
            description: User wasn't logged in because of the message in status.
          400,status="invalid credentials!":
            description: User wasn't logged in because of the message in status.
                """
        req = request.get_json()
        user_handler = UserApiHandler.user_handler
        username = req.get("username")
        password = req.get("password")
        error = None
        if username is None or password is None:
            error = 'username and password fields cannot be empty!'
            out = {'status': error}
            return jsonify(out), 400
        u = user_handler.get_by_name(username)
        if u is None or not u.check_password(password):
            error = 'invalid credentials!'
            out = {'status': error}
            return jsonify(out), 400
        token = auth_manager.generate_token(u.id)
        out = {'object': u.serialize(), 'token': token}
        return jsonify(out), 200

    @staticmethod
    @usr.route('/logout', methods=["GET"])
    @auth_manager.authenticate
    def logout(user):
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
            description: User successfully logged out.
            schema:
            type: object
            properties:
                status:
                    type: string
                    example: OK
          401:
            description: You aren't logged in
        """
        auth_manager.expire_token()
        out = {'status': 'OK'}
        return jsonify(out), 200

    @staticmethod
    @usr.route('', methods=["GET"])
    @auth_manager.authenticate
    def list_users(user):
        """
        This is the ListUsers API
        Call this api to get the list of users.
        ---
        tags:
            - ListUsers API
        responses:
            200:
              description: OK
              schema:
              type: object
              properties:
                object:
                    type: array
                    items:
                        type: object
                        properties:
                            username:
                                example: ali
                                type: string
                            email:
                                type: string
                                example: ali@gmail.com
                            identificationId:
                                type: string
                                example: 0020738528
                            address:
                                type: string
                                example: tehran
                            age:
                                type: integer
                                example: 27
                            gender:
                                type: string
                                example: male
                            id:
                                type: integer
                                example: 2
                            lastName:
                                type: string
                                example: erf
                            mobile_num:
                                type: string
                                example: 09102998841
                            phone_num:
                                type: string
                                example: 02188461197
                            name:
                                type: string
                                example: ali
                            postalCode:
                                type: integer
                                example: 1565935871
                            role:
                                type: string
                                example: user

            400,status="there are no users in the database!":
                description: No cars!
            400,status="this url is not accessible for you!":
                description: You are not an admin!
            401:
                description: You haven't logged in!
        """
        if user.role == "super_admin" or user.role == "admin":
            users = User.query.all()
            if users is None:
                out = {'status': 'there are no users in the database!'}
                return jsonify(out), 400
            u = []
            for user in users:
                u.append(user.serialize())
            out = {'object': u}
            return jsonify(out), 200
        out = {'status': 'this url is not accessible for you!'}
        return jsonify(out), 400

    @staticmethod
    @usr.route('/<int:user_id>', methods=["DELETE"])
    @auth_manager.authenticate
    def delete_user(user, user_id):
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
                description: Ok.
            400,status="user_id cannot be empty!":
                description: User wasn't deleted because of the message in status.
            400,status="invalid user_id!":
                description: User wasn't deleted because of the message in status.
            400,status="this url is not accessible for you!":
                description: User wasn't deleted because you are not an admin.
            400,status="you can not delete this user!":
                description: The user you're trying to remove is an admin!
            401:
                description: You aren't logged in
        """
        if user.role == "admin" or user.role == "super_admin":
            if user_id is None:
                out = {'status': 'user_id cannot be empty!'}
                return jsonify(out), 400
            user2 = User.query.filter_by(id=user_id).first()
            if user2 is None:
                out = {'status': 'invalid user_id!'}
                return jsonify(out), 400
            if user2.role == "user" or user.role == "super_admin":
                for car in user2.cars:
                    db.session.delete(car)
                db.session.delete(user2)
                db.session.commit()
                out = {'status': 'OK'}, 200
                return jsonify(out)
            else:
                out = {'status': 'you can not delete this user!'}
                return jsonify(out), 400
        else:
            out = {'status': 'this url is not accessible for you!'}
            return jsonify(out), 400
