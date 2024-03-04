from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from flask import flash, redirect, Response
import csv
from datetime import datetime
from io import StringIO
from .models import Election, Question, Option, Voter
from .forms import ElectionForm, QuestionForm, OptionForm
import requests

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required # only logged in user can see this
def profile():
    return render_template('profile.html', name=current_user.name)

# @main.route('/myvotes')
# @login_required # only logged in user can see this
# def myvotes():
#     return render_template('myvotes.html', name=current_user.name)

@main.route('/create_election', methods=['GET', 'POST'])
@login_required
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
            'creator_id': current_user.id,
            'question': form.question.question_text.data,
            'options': [option_form.data['option'] for option_form in form.question.options.entries],
            'voter_file': form.voter_file.data.stream.read().decode("utf-8") if form.voter_file.data else None
        }

        if send_data_to_election_microservice(form_data):
            flash('Election created successfully!')
            return redirect(url_for('main.my_elections'))
        
        else:
            print(form.errors) #TO-DO - print the correct error

    else:
        print(form.errors)
    
    return render_template('create_election.html', form=form)


# API gateway needed to send data to backend
def send_data_to_election_microservice(form_data):
    microservice_url = 'http://127.0.0.1:3000/create-election'

    try:
        response = requests.post(microservice_url, json=form_data)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data sent successfully to microservice!")
            return True
        else:
            print(f"Failed to send data to microservice. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error sending data to microservice: {e}")
        return False


# API gateway needed to get data from backend
@main.route('/my_elections')
@login_required
def my_elections():
    microservice_url = f'http://127.0.0.1:3000/fetch-elections/{current_user.id}'
    try:
        response = requests.get(microservice_url)
        elections = response.json()
        if response.status_code == 200:
            return render_template('my_elections.html', elections=elections)
        else:
            print(f"Failed to fetch user elections. Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching user elections: {e}")
        return []


# API gateway needed to get data from backend
@main.route('/download_voters/<int:election_id>')
@login_required
def download_voters(election_id):
    microservice_url = f'http://127.0.0.1:3000/election_voters/{current_user.id}/{election_id}'
    
    si = StringIO()
    cw = csv.writer(si)
    # cw.writerow(['Email', 'Name'])
    
    response = requests.get(microservice_url)
    voters = response.json()
    print(voters)
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
        print(f"Failed to fetch voters. Status code: {response.status_code}")
        return []