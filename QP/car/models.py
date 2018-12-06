from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from QP import db
from QP.user.models import User


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    factory = db.Column(db.String(20))
    kilometer = db.Column(db.Integer)
    year = db.Column(db.Integer)
    color = db.Column(db.String(20))
    description = db.Column(db.String(100))
    automate = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Integer)
    image_url = db.Column(db.String)

    def __repr__(self):
        return "<Car '{}'>".format(self.name)

    @staticmethod
    def get_by_owner(user_id):
        return User.query.filter_by(user_id=user_id)

    def serialize(self):
        return {
            'name' : self.name,
            'factory' : self.factory,
            'kilometer' : self.kilometer,
            'year' : self.year,
            'color' : self.color,
            'description' : self.description,
            'automate' : self.automate,
            'user_id' : self.user_id,
            'price' : self.price,
            'id' : self.id,
            'image_url' : self.image_url
        }
