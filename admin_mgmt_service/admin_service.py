from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from . import create_app

app = create_app()

@app.route('/')
def hello_microservice():
    return "hello"


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
       
        print("User added successfully to the database")
        return jsonify({'name': name})
    
    except Exception as e:
        # Handle errors (e.g., database errors)
        db.session.rollback()
        print(f"Error adding user data to the database: {e}")


@app.route('/authenticate', methods=['POST'])
def auth_user():
    # Get data
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    print(user.is_active)

    # check if user  exists
    # take the  password hash it and compare it to the hashed password in the db
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Incorrect email or password'}), 401
    
    else:
        return jsonify({'user': {'id': user.id, 'email': user.email, 'is_active': user.is_active}}), 200