from flask_login import UserMixin
from . import db
from sqlalchemy import DateTime


# what else might we need here?
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    elections = db.relationship('Election', backref='creator', lazy='dynamic')

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    # start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(DateTime))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    voters = db.relationship('Voter', backref='election', lazy='dynamic')

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))

    def __repr__(self):
        return '<Voter {}>'.format(self.email)