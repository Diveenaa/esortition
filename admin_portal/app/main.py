from flask import Blueprint, render_template, url_for, session, request, make_response
from flask_login import login_required, current_user

from flask import flash, redirect, Response
import csv
from datetime import datetime
from io import StringIO
from .forms import ElectionForm, QuestionForm, OptionForm
import requests
from . import ADMIN_MGMT_API_GATEWAY_URL, ELECTION_MGMT_API_GATEWAY_URL
import logging

main = Blueprint('main', __name__)

@main.route('/')
def index():
    verified = is_authenticated()
    logging.info(verified)
    return render_template('index.html', is_authenticated=verified)

# API Gateway
@main.route('/profile')
def profile():
    token = session.get('token')
    logging.info(token)
    if not token:
        return redirect(url_for('auth.login'))  # Redirect to login if token is not found
    
    microservice_url = f'{ADMIN_MGMT_API_GATEWAY_URL}profile'
    # Pass the token in the request headers when making the request
    response = make_request(microservice_url, token)
    if response and response.status_code == 200:
        data = response.json()
        name = data.get('name', 'Unknown')  # Default to 'Unknown' if 'name' key is missing
        return render_template('profile.html', name=name, is_authenticated=True)
    else:
        flash('Failed to fetch profile data')
        return redirect(url_for('auth.login'))

# @main.route('/myvotes')
# @login_required # only logged in user can see this
# def myvotes():
#     return render_template('myvotes.html', name=current_user.name)

@main.route('/create_election', methods=['GET', 'POST'])
def create_election():
    form = ElectionForm()
    while len(form.question.options) < 6:
        form.question.options.append_entry()

    if form.validate_on_submit():
        end_date_str = form.end_date.data.strftime('%Y-%m-%d %H:%M:%S')

        form_data = {
            'title': form.title.data,
            'description': form.description.data,
            'end_date': end_date_str,
            'question': form.question.question_text.data,
            'options': [option_form.data['option'] for option_form in form.question.options.entries],
            'voter_file': form.voter_file.data.stream.read().decode("utf-8") if form.voter_file.data else None
        }

        if send_data_to_election_microservice(form_data):
            logging.info('Election created successfully!')
            return redirect(url_for('main.my_elections'))
        
        else:
            logging.info('connection failed') #TO-DO - print the correct error

    else:
        logging.info(form.errors)
    
    return render_template('create_election.html', form=form, is_authenticated=True)


# API gateway needed to send data to backend
def send_data_to_election_microservice(form_data):

    ######################## here we want to change to api gateway ##################
    token = session.get('token')
    logging.info(token)
    
    microservice_url = f'{ELECTION_MGMT_API_GATEWAY_URL}create-election'

    try:
        response = requests.post(microservice_url, json=form_data, headers={'Authorization': token})
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            logging.info("Data sent successfully to microservice!")
            return True
        else:
            logging.info(f"Failed to send data to microservice. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        logging.info(f"Error sending data to microservice: {e}")
        return False


# API gateway needed to get data from backend
@main.route('/my_elections')
def my_elections():
    token = session.get('token')
    logging.info(token)
    
    microservice_url = f'{ELECTION_MGMT_API_GATEWAY_URL}fetch-elections'
    
    try:
        response = make_request(microservice_url, token)
        
        # Check if the response object is not None and status code is 200
        if response and response.status_code == 200:
            logging.info(response.content)
            elections = response.json()
            return render_template('my_elections.html', elections=elections, is_authenticated=True)
        else:
            # Log detailed error information
            if response:
                logging.info(f"Failed to fetch user elections. Status code: {response.status_code}, Content: {response.content}")
            else:
                logging.info("Failed to fetch user elections. No response received.")
            return make_response("Error fetching user elections", 500)
    except requests.RequestException as e:
        logging.info(f"Error fetching user elections: {e}")
        return make_response("Error fetching user elections", 500)


# API gateway needed to get data from backend
@main.route('/download_voters/<int:election_id>')
def download_voters(election_id):
    token = session.get('token')

    microservice_url = f'{ELECTION_MGMT_API_GATEWAY_URL}election_voters/{election_id}'

    response = make_request(microservice_url, token)    
    si = StringIO()
    cw = csv.writer(si)
    # cw.writerow(['Email', 'Name'])
    
    voters = response.json()
    logging.info(voters)
    if response.status_code == 200:
        for voter in voters:
            cw.writerow([voter['email'], voter['name']])
    
        output = si.getvalue()
        si.close()
        
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-disposition":
                    "attachment; filename=voters_election.csv".format(election_id)})
    else:
        logging.info(f"Failed to fetch voters. Status code: {response.status_code}")
        return []
    

def make_request(url, token=None):
    headers = {
        'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
        'Access-Control-Allow-Headers': 'Content-Type',  # Specify allowed headers
    }
    if token:
        headers['Authorization'] = token  # Include the token in the Authorization header

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response
    except requests.RequestException as e:
        logging.info(f"Error making request to {url}: {e}")
        return None

# API Gateway
def is_authenticated():
    token = session.get('token')
    logging.info(token)
    if not token:
        return False
    
    microservice_url = ADMIN_MGMT_API_GATEWAY_URL
    # Pass the token in the request headers when making the request
    try:
        response = make_request(microservice_url, token)
        data = response.json()
        is_authenticated = data['is_authenticated']
        logging.info('value', is_authenticated)
        return is_authenticated
    except requests.RequestException as e:
        logging.info(f"Error making request: {e}")
        return None