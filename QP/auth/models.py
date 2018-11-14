from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from QP import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(80))
    lastName = db.Column(db.String(20))
    age = db.Column(db.Integer)
    identificationId = db.Column(db.Integer)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(20))
    postalCode = db.Column(db.String(21))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String)
    authenticated = db.Column(db.Boolean)
    mobile_num = db.Column(db.String(15))
    phone_num = db.Column(db.String(15))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email = email).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def serialize(self):
        return {
            'name' : self.name,
            'password' : self.password_hash,
            'lastName' : self.lastName,
            'age' : self.age,
            'identificationId' : self.identificationId,
            'address' : self.address,
            'gender' : self.gender,
            'postalCode' : self.postalCode,
            'username': self.username,
            'email': self.email,
            'mobile_num': self.mobile_num,
            'phone_num': self.mobile_num
        }
