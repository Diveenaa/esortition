from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import requests
from . import ADMIN_MGMT_API_GATEWAY_URL

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', is_authenticated = False)

# API gaetway needed - to check data in microservice
@auth.route('/login', methods=['POST'])
def login_post():

    data = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'remember': True if request.form.get('remember') else False
    }

    microservice_url = ADMIN_MGMT_API_GATEWAY_URL + 'authenticate'

    try:
        response = requests.post(microservice_url, json=data)
        # Check if the request was successful (status code 200)
        if response.status_code == 401:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # reload the page for wrong pw/not registeredd
        elif response.status_code == 200:
            # if the above check passes user gets redirected to profile
            user_info = response.json().get('user')
            token = response.json().get('token')
            session['token'] = token
            return redirect(url_for('main.profile'))       
        else:
            flash('An error occurred while processing your request.')
            return redirect(url_for('auth.login'))

    except requests.RequestException as e:
        # Handle any errors that occur during the request
        flash('An error occurred while processing your request.')
        return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


# API gaetway needed - to send data to microservice
@auth.route('/signup', methods=['POST'])
def signup_post():
    data = {
            'email': request.form.get('email'),
            'name': request.form.get('name'),
            'password': request.form.get('password')
        }
    
    microservice_url = ADMIN_MGMT_API_GATEWAY_URL + 'signup'

    try:
        response = requests.post(microservice_url, json=data)
        # Check if the request was successful (status code 200)
        if response.status_code == 409:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        if response.status_code == 200:
            print("Data sent successfully to microservice!")
            return redirect(url_for('auth.login'))
        else:
            print(f"Failed to send data to microservice. Status code: {response.status_code}")
            flash('Please try again')
            return redirect(url_for('auth.signup'))
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error sending data to microservice: {e}")
        flash('Please try again')
        return redirect(url_for('auth.signup'))


@auth.route('/logout')
def logout():
    token = session.get('token')
    
    microservice_url = ADMIN_MGMT_API_GATEWAY_URL + 'logout'

    response = requests.get(microservice_url, headers={'Authorization': token})
    if response.status_code == 200:
        print("Logout successful")
        session.pop('token', None)
        return redirect(url_for('main.index'))

    else:
        print("Logout failed")
        return redirect(url_for('main.index'))