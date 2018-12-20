from QP import db


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    user = db.relationship("User", backref=db.backref("renter", uselist=False), foreign_keys=[user_id])
    cost = db.Column(db.Integer, nullable=False)
    kilometer = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship("User", backref=db.backref("owner", uselist=False), foreign_keys=[owner_id])
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = db.relationship("Car", backref=db.backref("rent", uselist=False))
    start = db.Column(db.String, nullable=False)
    end = db.Column(db.String, nullable=False)
    source = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Rent '{}'>".format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'car_id': self.car_id,
            'start': self.start,
            'end': self.end,
            'source': self.source,
            'destination': self.destination,
            'cost': self.cost,
            'kilometer': self.kilometer
        }
