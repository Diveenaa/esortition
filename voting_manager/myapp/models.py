from . import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    age = db.Column(db.Integer)