from QP import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    token = db.Column(db.String)

    def __repr__(self):
        return "<Token '{}'>".format(self.user_id)

