from . import create_app
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS module
import jwt
from flask_migrate import Migrate
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from .models import User
from . import db
import os
import logging

app = create_app()
CORS(app) 
migrate = Migrate(app, db)

login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('ADMIN_DATABASE_URL')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)  # Set session lifetime to 1 year

@login_manager.user_loader
def load_user(user_id):
    # user_id is the primary key
    return User.query.get(int(user_id))

@app.route('/')
def index():
    token = request.headers.get('Authorization')
    logging.info(token)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    try:
        # Decode the JWT token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        is_authenticated = payload['is_authenticated']

        # Return the user profile information
        return jsonify({'is_authenticated': is_authenticated})
    
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


@app.route('/authenticate', methods=['POST'])
def auth_user():
    # Get data
    data = request.json
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember')

    user = User.query.filter_by(email=email).first()

    # check if user  exists
    # take the  password hash it and compare it to the hashed password in the db
    if not user or not check_password_hash(user.password, password):
        logging.info("invalid creds")
        return jsonify({'error': 'Incorrect email or password'}), 401
    
    else:
        logging.info("authenticated")
        login_user(user, remember=remember, duration=timedelta(days=365))
        logging.info(current_user.name)
        logging.info(current_user.is_authenticated)
        token_payload = {
            'user_id': user.id,
            'is_authenticated': current_user.is_authenticated  # Include the authentication status in the payload
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        logging.info(token)
        response_data = {
            'user': {'id': user.id, 'email': user.email, 'is_active': user.is_active, 'name': user.name},
            'token': token
        }
        return jsonify(response_data), 200


@app.route('/profile')
#@login_required # only logged in user can see this
def profile():
    token = request.headers.get('Authorization')
    logging.info(token)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401

    try:
        # Decode the JWT token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']

        # Get the user details from the database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Return the user profile information
        return jsonify({'name': user.name})

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/signup', methods=['POST'])
def add_user_info():
    # Get data
    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # checks if email is already registered
        return jsonify({'error': 'User exits'}), 409
        
    try:
        # create a new user with the form data and hash the password so we don't save the plain text ver to db
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the db
        db.session.add(new_user)
        db.session.commit()
       
        logging.info("User added successfully to the database")
        return jsonify({'name': name})
    
    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        logging.info(f"Error adding user data to the database: {e}")

@app.route('/logout')
def logout():
    token = request.headers.get('Authorization')
    logging.info(token)
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200