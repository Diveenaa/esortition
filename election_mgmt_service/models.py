from flask_login import UserMixin
from . import db
from sqlalchemy import DateTime
from datetime import datetime


class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    # start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(DateTime))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    voters = db.relationship('Voter', backref='election', lazy='dynamic')

    @property
    def status(self):
        current_datetime = datetime.utcnow()
        if current_datetime < self.end_date:
            return 'active'
        else:
            return 'closed'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    election = db.relationship('Election', backref=db.backref('questions', lazy=True))

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)  # Option text
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('options', lazy=True))

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    token = db.Column(db.String(100), unique=True, nullable=True)
    has_voted = db.Column(db.Boolean, default=False, nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))

    def __repr__(self):
        return '<Voter {}>'.format(self.email)