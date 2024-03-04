from flask_login import UserMixin
from . import db
from sqlalchemy import DateTime
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())