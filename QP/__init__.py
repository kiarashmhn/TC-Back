import os
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

from QP.auth.controllers import auth
from QP.auth.models import User
from QP.car.controllers import car
from QP.car.models import Car

base_url = '/api/v1'

app.register_blueprint(auth, url_prefix=base_url+'/auth')
app.register_blueprint(car, url_prefix=base_url+'/cars')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
