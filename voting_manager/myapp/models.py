from . import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer)
    question = db.Column(db.Integer)
    option = db.Column(db.Integer)
    election_id = db.Column(db.Integer)
