import os
from flask import Flask, request, jsonify, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasgger import Swagger
from flask_cors import CORS


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder='/Users/kiarash/Desktop/TC-Back')
Swagger(app)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(resources={r"/api/*": {"origins": "*"}})
cors.init_app(app)

from QP.user.models import User
from QP.auth.auth_manager import Auth
auth_manager = Auth(app)
from QP.user.controllers import usr
from QP.car.controllers import car
from QP.car.models import Car
from QP.sort.controllers import srt
from QP.image.controllers import img
from QP.rent.controllers import rnt

base_url = '/api/v1'

app.register_blueprint(usr, url_prefix=base_url + '/users')
app.register_blueprint(car, url_prefix=base_url+'/cars')
app.register_blueprint(srt, url_prefix=base_url+'/sort')
app.register_blueprint(img, url_prefix=base_url+'/images')
app.register_blueprint(rnt, url_prefix=base_url+'/rent')
