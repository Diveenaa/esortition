from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('ADMIN_DATABASE_URL')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

    db.init_app(app)

    with app.app_context():
        from . import models

    return app