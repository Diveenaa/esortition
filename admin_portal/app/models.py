from flask_login import UserMixin
from . import db

# what else might we need here?
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    elections = db.relationship('Election', backref='creator', lazy='dynamic')

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    voters = db.relationship('Voter', backref='election', lazy='dynamic')

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))

    def __repr__(self):
        return '<Voter {}>'.format(self.email)