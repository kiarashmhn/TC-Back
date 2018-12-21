from functools import wraps
from flask import request, abort, g, session
from uuid import uuid4
from QP import db, User
from QP.auth.token_store import Token


class Auth(object):
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.token_expire_time = 100000

    def generate_token(self, user_id):
        token = str(uuid4())
        t = Token(token=token, user_id=user_id)
        db.session.add(t)
        db.session.commit()
        user = User.query.filter_by(id=user_id).first()
        session['role'] = user.role
        return token

    def expire_token(self):
        token = Token.query.filter_by(token=request.headers['Access-Token']).first()
        db.session.delete(token)
        db.session.commit()

    def authenticate(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):

            if not 'Access-Token' in request.headers:
                return abort(401, "Set token to access protected routes")

            token = request.headers['Access-Token']
            user_token = Token.query.filter_by(token=token).first()
            if not user_token:
                return abort(401, "Token is invalid or has expired")
            user_id = user_token.user_id
            print(user_id)
            if not user_id:
                return abort(401, "Token is invalid or has expired")
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return abort(401, "Token is invalid or has expired")
            g.user_id = user_id
            return f(user, *args, **kwargs)

        return decorated
